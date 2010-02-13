"""
Core for the ImageGenerator - Implementation for Linux.

The main idea for this implementation is to pass the request for imaging 
to the Linux command C{dd}.

This module registers itself with the L{CoreManager} as a core.

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



@var NAME_IMPL: Name of this implementation
@type NAME_IMPL: C{String}
@var PARAM_INPUTFILE: Name of the parameter for specifying the input file for the dd command
@type PARAM_INPUTFILE: C{String}
@var PARAM_OUTPUTFILE: Name of the parameter for specifying the input file for the dd command
@type PARAM_OUTPUTFILE: C{String}
@var PARAM_BLOCKSIZE: Name of the parameter for specifying the blocksize for the dd command
@type PARAM_BLOCKSIZE: C{String}
@var FSTAB_LOCATION: Location for the file system table within the local file system. Required for 
determing possible sources for the imaging.
@type FSTAB_LOCATION: C{String}
@var PROC_LOCATION: Location of the file holding partition information inside the proc file system
@type PROC_LOCATION: C{String}
@var DEFAULT_PATH_DD: Default location for the dd command
@type DEFAULT_PATH_DD: C{String}

"""
import GeneratorCoreAbstract
import Runtime
import os
import CoreManager
import FESettings
import ImageSettings

NAME_IMPL = "Linux"
PARAM_INPUTFILE = "if"
PARAM_OUTPUTFILE = "of"
PARAM_BLOCKSIZE="bs"

FSTAB_LOCATION = "/etc/fstab"
PROC_LOCATION = "/proc/partitions"
FDISK_LOCATION = "/sbin/fdisk"
DEV_PREFIX = "/dev/"
DEFAULT_PATH_DD = "/bin/dd"
TMP_FDISK_FILE = ImageSettings.PATH_TMP_FDISK
FILE_TYPES = ImageSettings.PATH_FILETYPES

class GeneratorCore(GeneratorCoreAbstract.CoreInterface):
    """
    Class for implementing the core for Linux systems.
    
    @ivar _settings: Settings for the execution
    @type _settings: L{Runtime.Settings}
    """
    def __init__(self, settings):
        """
        Initialises the core. 
        
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
        ret = os.system(command)
        
        status.setFinished()
        if ret != 0:
            st = "Check log file '%s'." %(self._settings.getRedirectOutputBuffer())
            try:
                file = open(self._settings.getRedirectOutputBuffer(), 'r')
                msg = file.read()
                file.close()
                st = msg
            except Error, msg:
                pass
            status.setError("Linux Core: \nError whilst imaging\nErrorCode: %s\n%s" %(str(ret), st))
        return ret
        
    def _assembleCommand(self):
        """
        Assembles the command as it would be used in a Shell environment.
        
        Puts together the command C{dd} with the parameters for source file, destination
        file and blocksize and, if enabled, finishes with the bits for the output redirection. If
        redirection is enabled, both buffers will be redirected (standard output as well as 
        standard error output).
        
        @return: Command String as used on a shell
        @rtype: C{String}
        """
        command = self._settings.getPathDD()
        bs = str(self._settings.getBlocksize())
        source = self._settings.getSource()
        dest = self._settings.getDestination()
        
        st = "\"" + command + "\"" + " " + PARAM_BLOCKSIZE + "=" + bs + " " + PARAM_INPUTFILE + "="  + \
            "\"" + source + "\"" + " " + PARAM_OUTPUTFILE + "=" + "\"" + dest + "\""
            
        if self._settings.getRedirectOutputBuffer() != None:
            st = st + " > " + self._settings.getRedirectOutputBuffer() + " 2> " + self._settings.getRedirectOutputBuffer()
        
        # we need to be root
        sudo = FESettings.getSettings().getValue('command_sudo')
        st = sudo + " " + st
        return st

    def getPossibleSources(self):
        """
        Returns a list of possible sources for the machine.
        
        The request is passed to the private function L{_getListFromFstab}, which
        examines the File System Table file of the machine (/etc/fstab) and attempts
        to extract the devices.
        
        @return: Return Values of the function L{_getListFromFstab}
        @rtype: C{List} of C{Strings}; C{List} of {String}
        """
        try:
            list = self._getListFromProc()
            if list:
                return list
            else:
                return self._getListFromFstab()
        except IOError, msg:
            return self._getListFromFstab()
    
    def getSourceInfo(self):
        """
        Info on List of possible sources
        
        Provides some information about how the list of possible sources is assembled
        and how to deal with the provided information.
        
        @return: Info text - several lines
        @rtype: C{String}
        """
        return "\nHow to find your device\n" + "\n" \
                "Firstly, ImageGenerator attempts to process proc \nfilesystem information in" \
                "order to gather \ninformation about the available devices (path, size, type); \n" \
                "if thise fails, a list is assembles using the Linux \nfilesystem table (fstab)\n\n" \
                "Some experiences:\n" \
                "\tFloppy Disk: \t/dev/fd?\n" \
                "\tMemory Stick: \t/dev/sda1\n" \
                "\tHard disk: \t/dev/hda \n" \
                "\tHD partition: \t/dev/hdc1\n" \
                "\tCDROM drive:\t/dev/hdc\n" \
                "Also check the commands 'fdisk -l' or 'mount' for more information."
    
    def _getListFromProc(self):
        """
        An implementation to get suggestions for imagable resourses.
        
        Information from the proc file system tree is evaluated.
        
        @return: List of names with some more information; List of names for devices extracted form the fstab file
        @rtype: C{List} of C{String}; C{List} of C{String}
        """
        global DEV_PREFIX, PROC_LOCATION
        
        ret = []
        ret_detail = []
        try:
            partitions = open(PROC_LOCATION)
        except Error, msg:
            return None
        
        types = self._getTypesFromFdisk()
        
        line = " "
        linecount = 0
        columnName = 3
        columnBlocks = None
        while line != "":
            line = partitions.readline()
            if line.strip() == "":
                continue
            entries = line.split()
            if linecount == 0:
                columnName = entries.index('name')
                try:
                    columnBlocks = entries.index('#blocks')
                except Error, msg:
                    pass
            else:
                path = DEV_PREFIX + entries[columnName].strip()
                ret.append(path)
                if columnBlocks:    # if size information available
                    details = path + "  (%d MB)" % (int(entries[columnBlocks].strip()) / 1024)  
                else:
                    details = path
                if types:   # if information about partition type available
                    if types.has_key(path):
                        details += "  [%s]" %(types[path])
                ret_detail.append(details)
        
            linecount += 1
        partitions.close()
        return ret_detail, ret
        
    def _getTypesFromFdisk(self):
        global DEV_PREFIX
        command = FDISK_LOCATION + " -l > " + TMP_FDISK_FILE
        ret = os.system(command)
        if ret != 0:
            print "Partition type determination failed on fdisk execution"
            return None
        
        tmpFile = open(TMP_FDISK_FILE, 'r')
        posId = None
        ret = {}
        while 1:
            line = tmpFile.readline()
            if not line:
                break
            if line.strip().startswith('Device'):   # header of the table
                posId = line.index('Id')
            
            if line.startswith(DEV_PREFIX):      # that's our entry
                if posId:
                    partName = line.split()[0].strip()
                    typeId = line[posId:posId+2]
                    ret[partName] = self._getNameForType(typeId)
        tmpFile.close()
        return ret
        
    def _getNameForType(self, typeId):
        import os
        import os.path
        import sys
        f = open(FILE_TYPES, 'r')
        while 1:
            line = f.readline()
            if not line:
                break
            if line.startswith(typeId.strip()):
                startPosString = line.split()[1]
                startPos = line.index(startPosString)
                name = line[startPos:].strip()
                return name
        f.close()
        
        return typeId
    
    def getSizeEstimationForPartition(self, partitionName):
        """
        Extracts information from the proc file system to determine filesize.
        
        We can only read block size; we assume block size of 1024 Bytes to determine size in Byte.
        """
        global DEV_PREFIX, PROC_LOCATION
        
        try:
            partitions = open(PROC_LOCATION)
        except Error, msg:
            return None

        if not partitionName.startswith(DEV_PREFIX):
            return None # estimation impossible - we assume, we are under /dev
        name = partitionName[len(DEV_PREFIX):]
        print name
        
        line = " "
        linecount = 0
        columnName = 3
        columnBlocks = None
        while line != "":
            line = partitions.readline()
            if line.strip() == "":
                continue
            entries = line.split()
            if linecount == 0:
                columnName = entries.index('name')
                try:
                    columnBlocks = entries.index('#blocks')
                except Error, msg:
                    return None         # we need this here
            else:
                if entries[columnName] == name:
                    return int(entries[columnBlocks]) * 1024

            linecount += 1

        return None
    
    def _getListFromFstab(self):
        """
        An implementation to get suggestions for imagable resourses.
        
        The file for File System talbe on the machine is processed and it is attempted to
        extract information about devices from it. In fact, all the lines, which do not start
        with a slash are skipped. Afterwards, always the first column of a line is taken
        and a list of all them together is assembled.
        
        @return: List of names with some more information; List of names for devices extracted form the fstab file
        @rtype: C{List} of C{String}; C{List} of C{String}
        """
        fstab = open(FSTAB_LOCATION)
        ret = []
        
        line = " "
        while line != "":
            line = fstab.readline()
            if line == "":      # skip if EOF
                continue
            if line[0] != "/":      # skip lines with comments and other stuff
                continue
            vals = line.split()
            ret.append(vals[0])
        
        fstab.close()
        return ret, ret

    def getDefaultDDLocation(self):
        """
        Gives a location for the dd command which is very likely to be used with this
        implementation.
        """
        return DEFAULT_PATH_DD    
        
CoreManager.getInstance().registerCore(NAME_IMPL, GeneratorCore)
