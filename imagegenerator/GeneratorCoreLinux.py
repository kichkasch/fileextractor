"""
Core for the ImageGenerator - Implementation for Linux.

The main idea for this implementation is to pass the request for imaging 
to the Linux command C{dd}.

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
@var FSTAB_LOCATION: Location for the file system table within the local file system. Required for 
determing possible sources for the imaging.
@type FSTAB_LOCATION: C{String}
@var DEFAULT_PATH_DD: Default location for the dd command
@type DEFAULT_PATH_DD: C{String}

"""
import GeneratorCoreAbstract
import Runtime
import os
import CoreManager

NAME_IMPL = "Linux"
PARAM_INPUTFILE = "if"
PARAM_OUTPUTFILE = "of"
PARAM_BLOCKSIZE="bs"

FSTAB_LOCATION = "/etc/fstab"
DEFAULT_PATH_DD = "/bin/dd"

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
                "Assembled List from File Systems table (fstab)\n" \
                "Each entry represents one line in the fstab file, always\n" \
                "the first entry is taken - should be the device.\n\n" \
                "Some experiences:\n" \
                "\tFloppy Disk: \t/dev/fd?\n" \
                "\tMemory Stick: \t/dev/sda1\n" \
                "\tHard disk: \t/dev/hda \n" \
                "\tHD partition: \t/dev/hdc1\n" \
                "\tCDROM drive:\t/dev/hdc\n" \
                "Also check the commands 'fdisk -l' or 'mount' for more information."
    
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
