#!/usr/bin/python

import sys
import time
import VL53L0X
import OSC
import numpy
import mido
import ConfigParser


class Ibuki:
    def __init__(self):
        # OSC params
        self.osc = OSC.OSCClient()
        self.osc_port = 3333
        self.osc_address = '33.33.33.255'

        # MIDI params
        self.note_offset = 60
        self.midi_channel = 15
        self.midi_port = 'Teensy MIDI:Teensy MIDI MIDI 1 20:0'

        # Sensor params
        self.num_sensors = 4
        self.long_range = False
        self.sensors = []
        self.noteon = []
        self.noteoff = []

        self.bottom_cutoff = 0
        self.top_cutoff = 8000
        self.sensor_range = [self.bottom_cutoff, self.top_cutoff]
        self.midi_range = [0,127]

        # Sensor debouncing
        self.debounce_times = 3
        self.sensor_debounce = []

    def startup(self):
        # Configuration
        self.load_config()

        # Intialize services
        try:
            self.osc.connect((self.osc_address, self.osc_port))
        except Exception as e:
            print('osc exception')
            print(e)
        try:
            self.midi_out = mido.open_output(self.midi_port)
            self.midi_out.panic()
        except Exception as e:
            print('midi exception')
            print(e)
        self.init_arrays()
        self.activate_sensors()

    def load_config(self):
        configuration = ConfigParser.RawConfigParser()
        configuration.read('ibuki.conf')

        self.osc_port = configuration.getint('osc_config', 'osc_port')
        self.osc_address = configuration.get('osc_config', 'osc_address')

        self.note_offset = configuration.getint('midi_config', 'note_offset')
        self.midi_channel = configuration.getint('midi_config', 'midi_channel')
        self.midi_port = configuration.get('midi_config', 'midi_port')

        self.num_sensors = configuration.getint('sensor_config', 'num_sensors')
        self.long_range = configuration.getboolean('sensor_config', 'long_range')
        self.bottom_cutoff = configuration.getint('sensor_config', 'bottom_cutoff')
        self.top_cutoff = configuration.getint('sensor_config', 'top_cutoff')
        self.debounce_times = configuration.getint('sensor_config', 'debounce_times')

    def init_arrays(self):
        for sensor_num in range(self.num_sensors):
            self.noteon.append(True)
            self.noteoff.append(False)
            self.sensor_debounce.append([self.top_cutoff]* self.debounce_times)
            # Create a VL53L0X object for each device
            self.sensors.append(VL53L0X.VL53L0X(TCA9548A_Num=sensor_num, TCA9548A_Addr=0x70))

    def activate_sensors(self):
        for sensor in self.sensors:
            # Start ranging on each sensor
	    if self.long_range:
                sensor.start_ranging(VL53L0X.VL53L0X_LONG_RANGE_MODE)
            else:
                sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        print("\n----------------")
        print("sensors ranging")
        print("----------------\n")

    def deactivate_sensors(self):
        for sensor in self.sensors:
            sensor.stop_ranging();
            print("sensors deactivated")

    def send_osc(self, address, msg):
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress(address)
        for value in msg:
            oscmsg.append(value)
        try:
            self.osc.send(oscmsg)
        except:
            pass

    def release_osc(self):
        self.osc.close()
        print("osc released")

    def send_midi(self, msg):
    #   print(msg)
        try:
            self.midi_out.send(msg)
        except e:
            print(e)

    def release_midi(self):
        self.midi_out.panic()
        self.midi_out.close()
        print("midi released")

    def read_sensors(self):
        for index, sensor in enumerate(self.sensors):
            # Get distance from VL53L0X
            distance = sensor.get_distance()

            #debounce the value by taking the last 'n' readings
            #and returning the minimum value
            self.sensor_debounce[index].append(distance)
            self.sensor_debounce[index].pop(0)
            if(self.noteon[index]):
                out_distance = distance
            else:
                out_distance = numpy.nanmin(self.sensor_debounce[index])



            if(out_distance < self.top_cutoff):
                self.send_osc("/sensor", [\
                    "aftertouch", index,\
                    numpy.interp(out_distance, self.sensor_range, self.midi_range),\
                    out_distance])

                if(self.noteon[index]):
                    self.send_osc("/sensor", ["noteon", index])
                    self.send_midi(mido.Message('note_on', note=index + self.note_offset, channel=self.midi_channel))
                    self.noteoff[index] = True
                    self.noteon[index] = False


            else:
                # only send this if out_distance is above top_cutoff and we're ready for a note_off
                if(self.noteoff[index]):
                    self.send_osc("/sensor", ["noteoff", index])
                    self.send_midi(mido.Message('note_off', note=index + self.note_offset, channel=self.midi_channel))
                    self.noteon[index] = True
                    self.noteoff[index] = False

def main():
    laser_harp = Ibuki()
    laser_harp.startup()

    while True:
        laser_harp.read_sensors()

    print('shutting down')
    laser_harp.deactivate_sensors()
    laser_harp.release_osc()
    laser_harp.release_midi()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        sys.exit(0)
