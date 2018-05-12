import mido
import OSC
import random
import sys
import threading
import time
from numpy import interp

delay = 0.1
num_chans = 4
offset = 60

class IbukiInterpreter:
    """

    """

    def __init__(self, ip=0, port=0):
        # OSC
        self.osc_ip = ip
        self.osc_port = port
        self.osc = OSC.OSCServer(('0.0.0.0', 3333))
        self.osc.addMsgHandler('/sensor', self.interpret)
        # self.osc.addMsgHandler('default',self.defaultOsc)
        self.client = OSC.OSCClient()
        self.client.connect(('33.33.33.35', 3333))
        self.osc.addDefaultHandlers()

        # MIDI
        self.midi_port = mido.open_output('ibuki', virtual=True)

    def sendMidi(self, _type, _channel, _note):
        msg = mido.Message(_type, channel=_channel, note = _note)
        print(msg)
        self.midi_port.send(msg)

    def sendAfter(self, _type, _channel, _value):
        msg = mido.Message(_type, channel=_channel, value = _value)
        print(msg)
        self.midi_port.send(msg)

    def interpret(self, path, tags, args, source):
        try:
            msg = OSC.OSCMessage("/sensor")
            msg.append(args)
            self.client.send(msg)
        except:
            pass
        # print(path, tags, args)
        if args[0] == 'noteon':
            self.sendMidi('note_on', args[1], args[1]+offset)
        elif args[0] == 'noteoff':
            self.sendMidi('note_off', args[1], args[1]+offset)
        elif args[0] == 'aftertouch':
            self.sendAfter('aftertouch', args[1], int(interp(args[2], [0.0,35.0], [20,127])))

    def defaultOsc(self, path, tags, args, source):
        print(path, tags, args)

    def startOsc(self):
        print("starting threaded OSC server")
        self.st = threading.Thread(target=self.osc.serve_forever())
        self.st.start()




def main():
    ibuki = IbukiInterpreter()
    ibuki.startOsc()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        ibuki.osc.close()
        ibuki.st.join()

    sys.exit(0)

if __name__ == '__main__':
    main()
