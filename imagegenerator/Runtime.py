"""
Runtime classes for the ImageGenerator. Contains a settings class for static information 
and a status class for dynamic information about a generation respectively.

@author: Michael Pilgermann
@contact: mailto:kichkasch@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)

@var DEF_PATH_DD: Default path to the dd command
@type DEF_PATH_DD: C{String}
@var DEF_SOURCE: Default value for the source to be imaged
@type DEF_SOURCE: C{String}
@var DEF_DEST: Default value for the image file
@type DEF_DEST: C{String}
@var DEF_FILESIZECHECK_DELAY: Default value for the delay for the FileSizeObserver for checking next time
@type DEF_FILESIZECHECK_DELAY: C{int}

"""
import time, threading
import Tools

DEF_PATH_DD = None
DEF_SOURCE = None
DEF_DEST = "/tmp/image"
DEF_BLOCKSIZE = 512

DEF_FILESIZECHECK_DELAY = 1  #  seconds

class Settings:
    """
    Maintains static information for a generation.
    
    @ivar path_dd: Path to the command dd
    @type path_dd: C{String}
    @ivar source: Source to be imaged
    @type source: C{String}
    @ivar destination: Filename of the image file to be created
    @type destination: C{String}
    @ivar blocksize: Blocksize for reading and writing
    @type blocksize: C{int}
    @ivar redirectOutput: Buffer, to which the output of the OS command shall be redirected to. (might be a file)
    @type redirectOutput: C{Buffer}
    """
    def __init__(self, path_dd = DEF_PATH_DD, source = DEF_SOURCE, destination = DEF_DEST,
            blocksize = DEF_BLOCKSIZE, redirectOutput = None):
        """
        Initialises the settings instance. All parameters have default values. Check the
        instance variables in this module.
        
        @param path_dd: Path to the command dd
        @type path_dd: C{String}
        @param source: Source to be imaged
        @type source: C{String}
        @param destination: Filename of the image file to be created
        @type destination: C{String}
        @param blocksize: Blocksize for reading and writing
        @type blocksize: C{int}
        @param redirectOutput: Buffer, to which the output of the OS command shall be redirected to. (might be a file)
        @type redirectOutput: C{Buffer}
        """
        self.path_dd = path_dd
        self.source = source
        self.destination = destination
        self.blocksize = blocksize
        self.redirectOutput = redirectOutput
        
    def getPathDD(self):
        """
        GETTER
        
        @return: Value of the instance variable for the path to the command dd
        @rtype: C{String}
        """
        return self.path_dd

    def setPathDD(self, path):
        """
        SETTER
        
        @param path: Path to the command dd
        @type path: C{String}
        """
        self.path_dd = path
        
    def getSource(self):
        """
        GETTER
        
        @return: Value of the instance variable for the source to be imaged
        @rtype: C{String}
        """
        return self.source
        
    def setSource(self, source):
        """
        SETTER
        
        @param source: Name of the device / file to be imaged
        @type source: C{String}
        """
        self.source = source
        
    def getDestination(self):
        """
        GETTER
        
        @return: Value of the instance variable for the destination image file
        @rtype: C{String}
        """
        return self.destination
        
    def setDestination(self, destination):
        """
        SETTER
        
        @param destination: Name of the image file to be created
        @type destination: C{String}
        """
        self.destination = destination
        
    def getBlocksize(self):
        """
        GETTER
        
        @return: Value of the instance variable for the blocksize for reading and writing
        @rtype: C{String}
        """
        return self.blocksize
        
    def getRedirectOutputBuffer(self):
        """
        Getter
        
        @return: None, if redirecting not enabled; otherwise the buffer
        @rtype: C{Buffer}
        """
        return self.redirectOutput
    
class Status:
    """
    Maintains dynamic information about a generation

    @ivar _dest_filesize: File size of the destination image file
    @type _dest_filesize: C{int}
    @ivar _isFinished: Indicated, whether the image generation has been finished
    @type _isFinished: C{Boolean}
    @ivar _starttime: Start time of the generation.
    @type _starttime: C{Float}
    @ivar _endtime: End time of the generation.
    @type _endtime: C{Float}
    @ivar _error: Error message for any error occured during exectution.
    @type _error: C{String}
    """
    def __init__(self):
        """
        Initialises the status instance. 
        """
        self._dest_filesize = 0
        self._isFinished = 0
        self._starttime = None
        self._endtime = None
        self._error = None
        self._end_filesize = None       # final file size estimation
    
    def updateDestinationFileSize(self, value):
        """
        Updates the instance variable L{_dest_filesize} with the given value.
        """
        self._dest_filesize = value
    
    def getDestinationFileSize(self):
        """
        Getter
        
        @return: The value of the instance variable L{_dest_filesize}
        @rtype: C{int}
        """
        return self._dest_filesize
        
    def isFinished(self):
        """
        Provides the information whether the image generation has been completed.
        
        @return: TRUE, if generation has completed, otherwise false (the value of the instance variable)
        @rtype: C{Boolean}
        """
        return self._isFinished
    
    def setFinished(self, value = 1):
        """
        Sets the status object to status completed generation.
        
        If value is true, the endtime is given the value of the current time.
        
        @param value: Value to be assigned to the instance variable for completed generation.
        @type value: C{Boolean}
        """
        self._isFinished = value
        if value:
            self._endtime = time.time()
        
    def setStarted(self, value = 1):
        """
        Inform the status that the generation is started.
        
        The start time is given the value of the current time.
        
        @param value: Is the generation started?
        @type value: C{Boolean}
        """
        self._starttime = time.time()
        
    def getElapsedTime(self, forceCurrent = 0):
        """
        How much time has elapsed since the status was set to started?
        
        Compares the start time stored in this object with the end time if the
        execution is finished or with the current time elsewhise. If L{forceCurrent}
        is true, it is always compared with the current time.
        
        If the execution wasn't started yet, 0 is returned.
        
        @param forceCurrent: Force comparing against current time. 
        @type forceCurrent: C{Boolean}
        
        @return: Elapsed time in seconds
        @rtype: C{float}
        """
        if self._starttime == None:
            return 0
        if forceCurrent or not self.isFinished():
            now = time.time()
            return now - self._starttime
        else:
            return self._endtime - self._starttime
    
    def getStartTime(self):
        """
        GETTER
        
        @return: Value of the instance varialbe L{_starttime}; 0 if L{_starttime} is C{None}.
        @rtype: C{Flaot}
        """
        if self._starttime == None:
            return 0
        return self._starttime
        
    def setError(self, error):
        """
        SETTER
        
        Sets the value for an error for the status instance.
        
        @param error: Error message for the execution.
        @type error: C{String}
        """
        self._error = error
    
    def getError(self):
        """
        GETTER
        
        @return: Value for the L{_error}, stored for this execution; could be C{None}
        @rtype: C{String}
        """
        return self._error
        
    def setEndFilesize(self, value):
        """
        SETTER
        
        Sets the value for the size estimation of the image file for the status instance.
        
        @param error: Error message for the execution.
        @type error: C{String}
        """
        self._end_filesize = value
        
    def getEndFilesize(self):
        """
        GETTER
        
        @return: Value for the file size estimation of the image file.
        @rtype: C{int}
        """
        return self._end_filesize

class FileSizeObserver(threading.Thread):
    """
    Responsible for observing a file and updating its file size to the given status instance.
    
    This class inherits from thread. After initialising with the parameters start the thread
    with instance.start(). The observing will be started this way.
    """
    def __init__(self, filename, status, delay = DEF_FILESIZECHECK_DELAY):
        """
        @param filename: Name of the file to be observed
        @type filename: C{String}
        @param status: Status instance to assign the updated information to
        @type status: L{Status}
        @param delay: Idle time between two updates in seconds
        @type delay: L{float}
        """
        threading.Thread.__init__(self)
        self.filename = filename
        self.status = status
        self.delay = delay
        
    def run(self):
        """
        Overwritten from the Thread class. 
        
        Only invokes the private function L{_observe}.
        """
        self._observe()
        
    def _observe(self):
        """
        Once invoked this function checks the file size of the given file each <delay> seconds. The
        process is interrupted as soon as the function L{Status.isFinished()} in the status instance
        returns C{true}.
        """
        while not self.status.isFinished():
            time.sleep(self.delay)
            if Tools.isFileExistent(self.filename):
                size = Tools.getFileSize(self.filename)
                self.status.updateDestinationFileSize(size)
        # update for a last time
        if Tools.isFileExistent(self.filename):
            size = Tools.getFileSize(self.filename)
            self.status.updateDestinationFileSize(size)
        
