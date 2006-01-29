"""
Core for the ImageGenerator - Implementation for Windows 32 bit operating systems.

The open source implemention of dd for Win32 (by John Newbigin) systems is required for this module.
You may find more information on its webpage http://uranus.it.swin.edu.au/~jn/linux/rawwrite/dd.htm.
Passes the request for imaging to the command C{dd} provided.

This module registers itself with the L{CoreManager} as a core.

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)

@var NAME_IMPL: Name of this implementation
@type NAME_IMPL: C{String}
@var PARAM_INPUTFILE: Name of the parameter for specifying the input file for the dd command
@type PARAM_INPUTFILE: C{String}
@var PARAM_OUTPUTFILE: Name of the parameter for specifying the input file for the dd command
@type PARAM_OUTPUTFILE: C{String}
@var PARAM_BLOCKSIZE: Name of the parameter for specifying the blocksize for the dd command
@type PARAM_BLOCKSIZE: C{String}
@var DEFAULT_PATH_DD: Default location for the dd command
@type DEFAULT_PATH_DD: C{String}
@var DD_LIST_PARAMETER: Parameter for the DD command to show available devices
@type DD_LIST_PARAMETER: C{String}
@var TMP_FILE_NAME: Name for the file used for temporarly store the list of device - output of the dd --list command
@type TMP_FILE_NAME: C{String}
"""
import GeneratorCoreAbstract
import Runtime
import os
import os.path
import CoreManager

NAME_IMPL = "Win32"
PARAM_INPUTFILE = "if"
PARAM_OUTPUTFILE = "of"
PARAM_BLOCKSIZE="bs"

DEFAULT_PATH_DD = "dd\dd.exe"
DD_LIST_PARAMETER = "--list"
TMP_FILE_NAME = "./devicelist.tmp"

class GeneratorCore(GeneratorCoreAbstract.CoreInterface):
    """
    Class for implementing the core for Windows systems.
    
    @ivar _settings: Settings for the execution
    @type _settings: L{Runtime.Settings}
    """
    def __init__(self, settings):
        """
        The parameters are assigned to instance variables and the super constructor
        (L{GeneratorCoreAbstract.CoreInterface.__init__}) is called for initialising the name of the
        implementation.
        """
        GeneratorCoreAbstract.CoreInterface.__init__( self, NAME_IMPL)
        self._settings = settings
    
    def createImage(self, status):
        """
        Invokes the OS command for the image generation.
        
        The filesize observer (L{Runtime.FileSizeObserver}) is started and after assembling the command
        it is started using the L{os.system} method. Afterwards, the status object is set to finished.
        Corrosponging to the return value of the system call, the error field in the status instance
        is set.
        
        @param status: Reference to the status object used for this execution
        @type status: L{Runtime.Status}
        @return:  Return value of the OS command C{dd}
        @rtype: C{int}
        """
        filesize_observer = Runtime.FileSizeObserver(self._settings.getDestination(), status)
        filesize_observer.start()
        
        command = self._assembleCommand()
        print command
        ret = os.system(command)
        
        status.setFinished()
        if ret != 0:
            status.setError("Error whilst imaging")
        return ret
        
    def _assembleCommand(self):
        """
        Assembles the command as it would be used in a Shell environment.
        
        Puts together the command C{dd} with the parameters for source file, destination
        file and blocksize and, if enabled, finishes with the bits for the output redirection. If
        redirection is enabled, both buffers will be redirected (standard output as well as 
        standard error output). Loads of efforts have been put on the correct use of quotations for
        this command; however, a solution was found and it's really worth to have a look in the code.
        
        @return: Command String as used on a shell
        @rtype: C{String}
        """
        command = self._settings.getPathDD()
        bs = str(self._settings.getBlocksize())
        source = self._settings.getSource()
        dest = self._settings.getDestination()
        
        st = '"\"' + command + '\"' + ' ' + PARAM_BLOCKSIZE + '=' + bs + ' ' + PARAM_INPUTFILE + '='  + \
            '\"' + source + '\"' + ' ' + PARAM_OUTPUTFILE + '='  + '\"' + dest + '\"' 
            
        if self._settings.getRedirectOutputBuffer() != None:
            st = st + ' > ' + '\"' + self._settings.getRedirectOutputBuffer() + '\"' #+ " %2> " + self._settings.getRedirectOutputBuffer()
        st = st + '"'
        return st

    def getPossibleSources(self):
        """
        Returns a list of possible source devices for imaging.
        
        Passes the request to the private function L{_getSourcesFromDDOutput}, which uses the 
        listing option for devices of the dd command.
        
        @return: Output of the private function L{_getSourcesFromDDOutput}
        @rtype: C{List} of C{String}
        """
        return self._getSourcesFromDDOutput()
    
    def getSourceInfo(self):
        """
        Info on List of possible sources
        
        Provides some information about how the list of possible sources is assembled
        and how to deal with the provided information.
        
        @return: Info text - several lines
        @rtype: C{String}
        """
        return "\nHow to find your device\n" + "\n" \
                "Assembled List from the output of the dd command with the --list option.\n" \
                "Some information added from win32api - you need to install this module.\n" \
                "\nAlso check the command 'dd --list' for more information or\n" \
                "visit the website 'http://uranus.it.swin.edu.au/~jn/linux/rawwrite/dd.htm'"
                
    def _getSourcesFromDDOutput(self):
        """
        Returns a list of possible source devices for images.
        
        The dd command of John Newbigin provides an option for listing possible devices. (--list).
        This one is used and the output is redirected to a file. Afterwards this file is
        processed and the lines containing the devices are extracted.
        
        Two lists are returned; one with output for the user (some drive names and so on) and one
        with the names as to be used as sources for the dd command.
        
        @return: User readable List with possible devices to be imaged; real device list
        @rtype: C{List} of C{String}; C{List} of C{String}
        """
        try:
            import win32api
            win32there = 1
        except Error, msg:
            print "Debug: Win32API is not installed. Size of device cannot be determined"
            win32there = 0


        command = self._settings.getPathDD()
        command = '"\"' + command + '\"' + ' ' + DD_LIST_PARAMETER + ' >' + '\"' + TMP_FILE_NAME + '\"'
        ret = os.system(command)
        
        if ret == 0:
            file = open(TMP_FILE_NAME)
            line = " "
            ret = []
            ret_dev = []               # real device
            while line != "":
                line = file.readline()
                if line == "":          # skip if EOF
                    continue
                if line[0] != "\\":      # proper entires seem to start with doubles back slash
                    continue
                line = line.strip()      # remove white spaces around the entry
                ret_line = line
                if line[2] == ".":      # this is a mounted device - we can get some more infos - check web page
                    link = file.readline()
                    type = file.readline()
                    mount = file.readline()
                    link = link.strip()
                    link = link[8:]
                    type = type.strip()
                    mount = mount.strip()
                    mount = mount[11:]
##                    line = link + " (" + type + ") " + mount
                    line = mount.upper()[0:len(mount)-1] +  "   (" + type + ") " # + link 

                    if win32there:
                        import pywintypes
                        try:
                            sizeList = win32api.GetDiskFreeSpace(mount)
                            size = sizeList[0] * sizeList[1] * sizeList[3]
                            line += " - %d MB" %(size / 1024 / 1024)
                        except pywintypes.error, msg:
                            pass

                    ret_line = link
                else:
                    line = "-- " + line
                ret_dev.append(ret_line)
                ret.append(line)
            file.close()
            return ret, ret_dev
        else:
            l = []
            return l, l
        
        
    def getDefaultDDLocation(self, path_absolute = 1):
        """
        Gives a location for the dd command which is very likely to be used with this
        implementation.
        
        @param path_absolute: Shall the provided path be converted into an absolute path before returning?
        @type path_absolute: C{Boolean}
        """
        if path_absolute:
            return os.path.abspath(DEFAULT_PATH_DD)
        return DEFAULT_PATH_DD
        

    def getSizeEstimationForPartition(self, partitionName):
        """
        Extracts information from the winapi.
        """
        try:
            import win32api
        except Error, msg:
            print "Debug: Win32API is not installed. Size of device cannot be determined"
            return None
        
        # firstly, we need the letter for the drive
        command = self._settings.getPathDD()
        command = '"\"' + command + '\"' + ' ' + DD_LIST_PARAMETER + ' >' + '\"' + TMP_FILE_NAME + '\"'
        ret = os.system(command)
        
        if ret == 0:
            file = open(TMP_FILE_NAME)
            line = " "
            ret = []
            ret_dev = []               # real device
            while line != "":
                line = file.readline()
                if line == "":          # skip if EOF
                    continue
                if line[0] != "\\":      # proper entires seem to start with doubles back slash
                    continue
                line = line.strip()      # remove white spaces around the entry
                if line[2] == ".":      # this is a mounted device - we can get some more infos - check web page
                    link = file.readline()
                    type = file.readline()
                    mount = file.readline()
                    link = link.strip()
                    link = link[8:]
                    if not link == partitionName and not line == partitionName:
                        continue
                    
                    type = type.strip()
                    mount = mount.strip()
                    mount = mount[11:]
                    
                    sizeList = win32api.GetDiskFreeSpace(mount)
                    size = sizeList[0] * sizeList[1] * sizeList[3]
                    return size
                    
        return None
    
CoreManager.getInstance().registerCore(NAME_IMPL, GeneratorCore)
