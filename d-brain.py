#!/usr/bin/env python

import app
import agent_joystick
import agent_keusb24r

if __name__ == '__main__':
    e = app.App(
        (425, 190),
        'D-Brain'
    )
    e.run([
        agent_joystick.Agent(),
        agent_keusb24r.Agent()
    ])
