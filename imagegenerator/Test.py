#!/usr/bin/env python
"""
Test procedures for the Image Generator.

This module can start the application. It is checking for the call of the __main__ function and
will in case of start the simple Application.

FileExtractor is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
FileExtractor is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with FileExtractor. If not, see <http://www.gnu.org/licenses/>.
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
