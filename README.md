# WCRL-Pico-Platform
Software for the newly designed Raspberry Pi Pico hardware platform.


This code is to be integrated with the newly designed and work-in-progress WCRL Raspberry Pi Pico hardware platform. This platform integrates a Raspberry Pi Pico W, dc motors, stepper motor drivers, an ESC, and a BLDC motor for the battle bot. A separate ESP8266 module (coded in C) generates a soft access network for the Pico to connect to. The python code defines functions for motor and ESC movement, creates a network connection between the Pico and the ESP, and generates a UI at the Pico's IP address for robot control.


This code is a work in progress and will be updated as improvements are made.



***UPDATE 02/14/2023**

New hardware changes to the PCB are as follows (PCB REV 2):

**Deletion of ESP8266 module - Pico now self-generates soft-access point**
2 ESC channels with respective signals (as opposed to original 1)
4 motor inputs, each set in parallel
Input for external bot LED


New Pico Motor Driver.py code replaces older Motor Driver.py code. This code reflects the hardware changes as mentioned above. The Pico now generates its own soft-access network with a WPA2 password, assigns itself a local IP, opens a socket, and generates a UI for the control interface. 
