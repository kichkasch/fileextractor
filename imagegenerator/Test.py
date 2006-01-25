#!/usr/bin/env python
"""
Test procedures for the Image Generator.

This module can start the application. It is checking for the call of the __main__ function and
will in case of start the simple Application.

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)
"""

import GeneratorCoreLinux
import Runtime

def checkCoreLinux():   
    settings = Runtime.Settings(source="/home/michael/gitta/HZ\ Petereit.exe")
#    settings = Runtime.Settings(source="/dev/fd0")
    print settings.getSource(), settings.getDestination()
    core = GeneratorCoreLinux.GeneratorCore(settings)
    print core.getImplementationName()
    status = Runtime.Status()
    print core.createImage(status)

def go():
    checkCoreLinux()

if __name__ == "__main__":
    go()
