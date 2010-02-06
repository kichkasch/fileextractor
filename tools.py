"""
Provides certain, reuseable functions (tools) for FileExtractor.

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


@var FALSE: Exactly what you think it is
@type FALSE: C{int}
@var TRUE: Exactly what you think it is
@type TRUE: C{int}
"""
import os.path
import sys

# constants
FALSE = 0
TRUE = 1
        
import signatures

def checkString(st, list):
    """
    Checks whether the entire list L{list} is at the beginning of L{st}.
    
    L{st} is a list of characters, say a C{string}. L{list} however is a list of
    numbers. This function gets the ASCII code for the character and compares it
    with the number in the list.
    
    @param st: String to compare against the list
    @type st: C{String}
    @param list: List, which has to be found in total at the beginning of the string
    @type list: C{List} of C{Int}
    @return: TRUE if the entire list is found at the beginning of the String otherwise false
    @rtype: C{Boolean}
    """
    if len(st) < len(list):
        return FALSE
    i = 0
    for i in range(len(list)):
        x = ord(st[i])
        n = list[i]
        # If value in list is None, then this Byte to be skipped
        if n == None:
            continue
        if x!=n:
            return FALSE
    return TRUE
    
def writeFile(type, counter, extension, filehandle, start, end, folder, showoutput, status):
    """
    Writes a certain chunk from a source file to a new file.
    
    This function assembles a filename regarding to the given settings (digtis, etc.). The old 
    position in the source file is memorised. The part of the source file from start to end
    is stored in the new file. The new file is closed and the position in the source file
    is restored.
    
    @param type: Name of the file type - in fact the start of the new filename
    @type type: C{String}
    @param counter: Running number - in fact the second part of the new filename
    @type counter: C{int}
    @param extension: The file extension of the new file
    @type extension: C{String}
    @param filehandle: Reference to the source file
    @type filehandle: Reference to file
    @param start: Starting position in the source file to copy to the new file
    @type start: C{int}
    @param end: End position in the source file to copy to the new file
    @type end: C{int}
    @param folder: Destination folder for the output file
    @type folder: C{String}
    @param showoutput: Indicates, whether debug output shall be displayed to standard output
    @type showoutput: C{Boolean}
    @param status: Reference to status instance of the current execution
    @type status: L{ExecutionSettings.ExecutionStatus}
    """
    oldPos = filehandle.tell()
    scounter = str(counter)
    scounter = scounter.zfill(status.settings.digits)
    filename = type + '_' + scounter + '.' + extension
    filename = folder + filename
    ofile = open(filename, 'wb')
    filehandle.seek(start)
    val = filehandle.read(end-start+1)
    ofile.write(val)
    ofile.close()
    if showoutput:
        print ("Wrote file with name <%s> from 0x%x to 0x%x (%d Bytes)" %(filename, start, end, end-start))
    filehandle.seek(oldPos)

def checkDestfolder(dest_folder):
    """
    Checks, whether the given folder ends with a slash, if not the slash will be appended.
    
    @param dest_folder: Name of folder to be checked
    @type dest_folder: C{String}
    @return: Adjusted name of folder
    @rtype: C{String}
    """
    dest_folder
    # last argument must be the file name
    if dest_folder[len(dest_folder)-1] != '/':
        dest_folder += '/'
    return dest_folder

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

def determineCoreName(coreNameSetting):
    if coreNameSetting == None or coreNameSetting == "" or coreNameSetting == "auto":
        import os
        osName = os.name
        if osName == "posix":
            return "Linux"
        elif osName == "nt":
            return "Win32"
        return None
    from imagegenerator import CoreManager
    if coreNameSetting in CoreManager.getInstance().getListOfCoreNames():
        return coreNameSetting
    else:
        return None

def determineAbsPath(locationDD):
    if locationDD[0] == ".":
        return os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), locationDD)
    else:
        return locationDD
