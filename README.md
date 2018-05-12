# ibuki_v2
raspberry pi based ibuki laser harp system
May 12, 2018 - This project is incomplete.

Todo:
- finalize installation scripts for each computer
- add hardware lists for each system parts
- add hardware designs for custom PCBs

# Ibuki 2 - Electric Boogaloo
----
This is an update to the Ibuki Laser Harp system. This moves the sensor system from a Teensy/Arduino platform to a Raspberry Pi 3 platform to improve the troubleshooting and update capability of the platform for long term use in performance.

The system consists of 3 parts:

1. Platform:
    - Software: This is the code that lives on each laser harp platform. This usually takes the form of one Raspberry Pi 3 with 8 sensors. The sensor information is transmitted in an OSC format. A static platform may use a wired network connection. A moveable platform may use use an XBee radio to talk back to the synthesizer software. The platform may or may not have MIDI controllable lighting built in.
    - Hardware: Design files for the custom PCBs and Enclosure elements; including BOMs.

2. Status GUI:
    - Software: The Status GUI runs on a separate Raspberry Pi 3 with touchscreen. This is used to turn on and off various components of the system as well as monitor any connected platforms for troubleshooting and piece of mind during a performance situation.
    - Hardware: BOMs for Raspberry Pi 3 touchscreen.

3. Synthesizer:
    - Software: This holds all code for making sound. The Laser Harp is a generic instrument and can be used with any system. This will hold any templates or translation scripts for use with sound generators such as Ableton Live, Supercollider, etc.
