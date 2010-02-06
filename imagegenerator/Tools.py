"""
Provides certain, reuseable functions (tools) for ImageGenerator.

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
import os.path

def getFileSize(filename):
    """
    Looks for the file size of the file with the given name.
    
    Passes the request to the function in the os module L{os.path.getsize()}.
    
    @param filename: Name of file the size shall be dertermined for.
    @type filename: C{String}
    @return: Return value of the function in the os module.
    @rtype: C{int}
    """
    return os.path.getsize(filename)

def isFileExistent(filename):
    """
    Looks in the file system whether the file is existent.
    
    Passes the request to the function in the os module L{os.path.exists()}.
    
    @param filename: Name of the file to check for existenz
    @type filename: C{String}
    @return: Return value of teh function in the os module - True if file available, False if not there or synmbolic link broken.
    @rtype: C{Boolean}
    """
    return os.path.exists(filename)

def processTime(ttime, filldigits = 0):
    """
    Puts the information of a time variable in a printable string format.
    
    For user output the time has to be put into a certain format. This function takes a time
    argument given in mili seconds and produces an output in form of a list: The content of the list
    is in order hour, minute, second, millisecond. The list entries are strings. Using the
    parameter filldigits the strings may be filled with leading zeros in order to hit their
    usual number of digits (2 digits for hour, minute and second; 4 digits for millisecond).
    
    @param ttime: Time to be formatted in millisecond
    @type ttime: C{int}
    @param filldigits: Indicates, whether leading zeros shall be filled.
    @type filldigits: C{Boolean}
    @return: List of formatted strings ([HH,MM,SS,MMMM])
    @rtype: C{List} of C{Strings}
    """
    time = []
    ttime = int(ttime*1000)
    ms  = ttime % 1000
    rest = ttime / 1000
    secs = rest % 60
    rest = rest / 60
    mins = rest % 60
    rest = rest / 60
    hours = rest
    time.append(str(hours))
    time.append(str(mins))
    time.append(str(secs))
    time.append(str(ms))
    if filldigits==0:
        for i in range(0,len(time)):
            if len(time[i]) < 2:
                time[i] = "0" + time[i]
    time[3] = "0" * (4 - len(time[3])) + time[3]
    return time
