"""
Module for maintaining runtime information about application execution. 

Both, the settings for configuring executions and status information about 
the current execution are handled by this module.

This class does not provide any notification whenever something has changed
within the class. Insteed, the observing class is supposed to implement a
timer and should check for up-to-date information frequently.

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


@var def_digits: Default value for digits for the numerical part in output file names
@var def_counterstart: Default value for the initial number for the output file names
@var def_folder: Default value for output folder
@var def_output_level: Default value for the amount of output to be generated by the application
@var def_output_frequency: Default value for the frequency output is generated for the CL interface
"""

import signatures
import time

def_digits = 5
def_counterstart = 1
def_folder = "./"
def_output_level = 2
def_output_frequency = 100

class ExecutionSettings:
    """
    Maintains the static information about an execution.
    
    @ivar digits: Number of digits for the numerical part of file names for output files.
    @ivar counterstart_global: Initial number for numerical part of file names for output files.
    @ivar dest_folder: Folder for output files.
    @ivar output_level: Indicator for amount of output to be created for CL interface.
    @ivar output_frequency: Indicator for frequency of output created for the CL interface.
    @ivar disabled_signatures: List of Strings, each entry representing one signature being disabled.
    @ivar sourceFiles: List of source files for searching in.
    @ivar number_sourcefiles: Total number of source files to be processed. (Generated automatically)
    @ivar signatures: Signatures active for this particular Execution.
    """
    def __init__(self, digits = def_digits, counterstart = def_counterstart, 
            dest_folder = def_folder, output_level = def_output_level, output_frequency = def_output_frequency,
            disabled_signatures = [], sourceFiles = [], signatures = None):
        """
        Initialises a new ExecutionSettings Object
        
        @param digits: Number of digits for the numerical part of file names for output files
        @type digits: C{int}
        """
        self.digits = digits
        self.counterstart_global = counterstart
        self.dest_folder = dest_folder
        self.output_level = output_level
        self.output_frequency = output_frequency
        self.disabled_signatures = disabled_signatures
        self.sourceFiles = sourceFiles
        self.number_sourcefiles = len(sourceFiles)
        self.signatures = signatures
        
    def disableSignatureWithNames(self, names):
        """
        Disables the given signatures in the list of this instance L{self.disabled_signatures}.
        
        @param names: List of names of signatures to be disabled
        @type names: C{List} of C{Strings}
        """
        for x in names:
            self.disabled_signatures.append(x)
    
    def getActiveSignatures(self):
        """
        Getter Method for active signatures for this instance.
        
        @return: List of active signatures
        @rtype: C{List} of Signatures
        """
        return self.signatures
        
    
class ExecutionStatus:
    """
    Maintains the dynamic information for an execution.
    
    @ivar settings: Reference to corresponding ExecutionsSettings object
    @ivar finished: Number of finshed source files
    @ivar result_eachfile: List of dictionaries for holding the results of found files within the sourcefiles
    @ivar foundOverall: Number of found files in total for all source files
    @ivar file_start: Location in source file to start the searching from
    @ivar file_end: Location in source file to terminate the searching at
    @ivar size: Filesize of the current file
    @ivar progressWithinCurrent:  Number of bytes gone through in the current source file
    @ivar counter: Dictionary with number of found files for the current source file (each entry one signature)
    @ivar counterr: Dictionary with number of found files in total for all source files (each entry one signature)
    @ivar startTimes: List of start times - each item represents the start time of one source file
    @ivar endTimes: List of end times - each item represents the end time of one source file
    @ivar sum_per_sourcefile: List of found files (each item representing the number of found files for one source file
        and all signatures).
    """
    def __init__(self, executionSettings):
        """
        Initialise the Status object
        
        Instance list attributes are reseted to empty lists, int values to 0 and the remaining ones to C{None}.
        
        @param executionSettings: Corrosponding settings instance for this execution.
        @type executionSettings: L{ExecutionSettings}
        """
        self.settings = executionSettings
        self.finished = 0
        self.result_eachfile = []
        self.foundOverall = 0
        
        self.file_start = None
        self.file_end = None
        self.size = 0
        self.progressWithinCurrent = 0
        
        self.counter = {}   # found files for the current source file
        self.counterr = {}  # found files overall
        for x in self.settings.signatures:
            if x not in self.settings.disabled_signatures:
                self.counterr[x[signatures.name]] = 0
        
        self.startTimes = []
        self.endTimes = []
        self.sum_per_sourcefile = []
        
    def initialisedOne(self):
        """
        Call this function whenever execution for one source file has been initialised.
        
        Empty body.
        """
        pass
    
    def startedOneSourceFile(self, size):
        """
        Call this function whenever the execution for one source file has been started.
        
        A new entry to the list L{sum_per_sourcefile} is added and the size as well as
        the start time is applied to instance variables.
        
        @param size: Size of the source file in bytes.
        @type size: C{int}
        """
        self.sum_per_sourcefile.append(0)
        self.size = size
        self.startTimes.append(time.time())
    
    def finishedOneSourceFile(self):
        """
        Call this function whenever the execution for one source file has been finished.
        
        Values for end time and number of finished files are applied to instance variables.
        L{file_start}, L{file_end} and L{counter} are reseted. The progress for the 
        current file L{progressWithinCurrent} is set to filesize.
        """
        self.progressWithinCurrent = self.size
        self.endTimes.append(time.time())
        self.file_start = None
        self.file_end = None
        self.finished += 1
        self.result_eachfile.append(self.counter)
        self.counter = {}
    
    def updateFineshedForCurrent(self, bytes):
        """
        Call this function whenever there is up-to-date information about the progress within a source file.
        
        @param bytes: Current position in the current source file in bytes.
        @type bytes: C{int}
        """
        self.progressWithinCurrent = bytes
    
    def foundFile(self):
        """
        Call this function whenever there is a new file found within a source file.
        
        
        The values for files found for the current source file as well as for the overall
        process are updated.
        """
        self.sum_per_sourcefile[self.finished] += 1
        self.foundOverall += 1
        return

    def getCurrentFile(self):
        """
        Provides the name of the current source file.
        
        @return: Name of current source file
        @rtype: C{String}
        """
        return self.settings.sourceFiles[self.finished]
        
    def getCurrentSize(self):
        """
        Provides the size of the current source file.
        
        Since searching within source files by providing start and end addresses within the files is possible
        this method returns the difference between these two values. For seaching from the beginning of a file
        up to the end these values are initialised with 0 / filesize which leads to the correct information
        for filesize here.
        
        @return: -1 if currently no source file is processed; otherwise the size of the current source file in bytes.
        @rtype: C{int}
        """
        if self.file_start != None and self.file_end != None:
            return self.file_end - self.file_start
        return -1
        
    def getCurrentFinished(self):
        """
        Provides the information about the progress within the current source file.
        
        @return: Progress within current source file in bytes.
        @rtype: C{int}
        """
        return self.progressWithinCurrent
    
    def getCurrentElapsedTime(self):
        """
        Provides the value for the time elapsed for processing the current source file.
        
        The  current time is requested from the system and the difference to the start time
        of the current file is calculated.
        
        @return: Elapsed time for current source file in seconds.
        @rtype: C{int}
        """
        now = time.time()
        return now - self.startTimes[self.finished]
    
    def getCurrentFound(self):
        """
        Provides the number of files found within the current source file in total for all signaturs.
        
        @return: Number of found files in current source file.
        @rtype: C{int}
        """
        return self.sum_per_sourcefile[self.finished]
        
    def getOverallFound(self):
        """
        Provides the number of files found in total for all source files and for all signatures.
        
        @return: Number of found files in total.
        @rtype: C{int}
        """
        return self.foundOverall
        
    def getSourceFileNumber(self):
        """
        Provides the number of involved source files for this execution.
        
        In fact this information is not stored in the status object itself; however, information about
        the number of files is kept in the settings instance. The status instance keeps a reference
        to the settings instance and performs a lookup in its information.
        
        @return: Number of source files in total.
        @rtype: C{int}
        """
        return self.settings.number_sourcefiles
        
    def hasMoreSourceFiles(self):
        """
        Checks, whether there are more source files to be processed at the current stage.
        
        The number of finished source files is compared with the number of total source files
        in the settings instance.
        
        @return: TRUE if more source files to be processed, otherwise FALSE
        @rtype: Boolean
        """
        return self.finished < self.settings.number_sourcefiles
    
    def getRunTimeForNumber(self, number):
        """
        Provides the time it took the program to process one specific source file.
        
        The values for the end time and the start time for this specific file are taken
        from the list and the difference between them represents the processing time.
        
        @param number: Running number of the source file the time shall be given for.
        @type number: C{int}
        @return: Processing time for the corrosponding source files in seconds.
        @rtype: C{int}
        """
        return self.endTimes[number] - self.startTimes[number]
