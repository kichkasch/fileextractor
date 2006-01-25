#!/usr/bin/env python
"""
Command line interface for the ImageGenerator. 

Also holds a class for generating runtime output containing the file size of the created
image file (class L{OutputObserver}). This class is its own thread, this is nessecary because
the execution of the command itself would block the thread otherwise.

This module can start the application. It is checking for the call of the __main__ function and
will in case initalise and start the ImageGenerator CLI version.

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)

@var OUTPUT_DELAY: Delay between two outputs for the filesize during the imaging process in seconds
@type OUTPUT_DELAY: C{Int}
@var DEBUG_FILENAME: Name of the file for temporaer storing of output of the os command
@type DEBUG_FILENAME: C{String}
"""
import Runtime
import CoreManager
import sys
import threading, time

OUTPUT_DELAY = 1    # in seconds; delay between 2 outputs
DEBUG_FILENAME = "./fileextractordebug.txt"

class ImageGeneratorCLI:
    """
    Integrates all functionality for the command line application.
    """
    def __init__(self):
        """
        Initialiser
        
        Nothing done here so far.
        """
        pass
        
    def startCLI(self):
        """
        Starts the entire application.
        
        Prompts the user for source device, destination file and the implementation to use. Afterwards,
        the settings and status class are instanciated and the appropriate core is generated. For 
        generating frequent output an instance of the class L{OutputObserver} is created too. Finally,
        after calling the C{createImage} function of the core, the return value is processed and, if
        sucessfully imaged, the file size is printed, otherwise an error message and the output
        of the operating system command.
        """
        manager = CoreManager.getInstance()
        implementation = "l"
        while implementation == "l":
            implementation = raw_input("Core implementations (l for list of available implementations): ")
            if implementation != "l":
                continue
            print manager.getListOfCoreNames()

        redirectBuffer = DEBUG_FILENAME
        settings = Runtime.Settings(redirectOutput = redirectBuffer)
        try:
            coreClass = manager.getCoreClass(implementation)
        except KeyError:
            print "\nRequested core not found. Program abortion.\n"
            sys.exit(-1)
        core = coreClass(settings)
    
        if core.getDefaultDDLocation() != None:
            st = "Location of the dd command [" + core.getDefaultDDLocation() + "]: "
        else:
            st = "Location of the dd command: "
        location_dd = raw_input(st)
        if location_dd == "":
            location_dd = core.getDefaultDDLocation()
        settings.setPathDD(location_dd)
            
        source = raw_input("Source file / source device (s for suggestions, h for help): ")
        while source == "s" or source == "h":
            if source == "s":
                suggestions, null = core.getPossibleSources()
                for sug in suggestions:
                    print ("\t%s" %sug)
            if source == "h":
                print core.getSourceInfo()
            source = raw_input("Source file / source device (s for suggestions, h for help): ")
        settings.setSource(source)
        
        destination = raw_input("Destination file (image file): ")
        settings.setDestination(destination)
        
        status = Runtime.Status()
        output = OutputObserver(status)
        output.start()
        status.setStarted()
        ret = core.createImage(status)      # Here we go :)
        if ret == 0:
            time1 = status.getElapsedTime()
            mins = str (int(time1) / 60)
            if len(mins) < 2:
                mins = '0' + mins
            secs = str (int(time1) % 60)
            if len(secs) < 2:
                secs = '0' + secs
            print ("\nImage created sucessfully. Size of image: %d Bytes. Time: %s mins %s secs." 
                %(status.getDestinationFileSize(), mins, secs ))
        else:
            print ("\nAn error occured during the imaging - error code: %d." %ret)
            print ("Output of the OS command:")
            print ("-" * 80)
            file = open(DEBUG_FILENAME)
            st = " "
            while st != "":
                st = file.readline()
                print (st)
            print ("-" * 80)

class OutputObserver(threading.Thread):
    """
    Observes the status object and print frequent output about the file size of the image file.
    
    @ivar _status: Reference to the status object
    @type _status: L{Runtime.Status}
    @ivar _buffer: Buffer, to print the output to. 
    @type _buffer: C{Buffer} - must support the functions C{write()} and C{flush()}
    """
    def __init__(self, status, buffer = sys.stdout):
        """
        Initialises the OutputObserver instance.
        
        The thread is initialised and the parameters are assigned instance variables.
        
        @param status: Status instance for this execution.
        @type status: L{Runtime.Status}
        @param buffer: Buffer, to print the output to. Default is standard output.
        @type buffer: C{Buffer} - must support the functions C{write()} and C{flush()}
        """
        threading.Thread.__init__(self)
        self._status = status
        self._buffer = buffer
        
    def run(self):
        """
        Is invoked whenever the method C{start()} (inherited from thread) is called from outside.
        
        Invokes the private method _observe inside this class.
        """
        self._observe()
        
    def _observe(self):
        """
        Checks the file size of the output file and print output frequently.
        
        Runs as long as the function L{Runtime.Status.isFinished} returns true. The size of the 
        destination file is gained from the status object and printed to the before defined 
        buffer. After a delay of L{OUTPUT_DELAY} seconds this process is performed again
        and again.
        """
        while not self._status.isFinished():
            size = self._status.getDestinationFileSize()
            self._buffer.write(chr(0x08) * 80)
            self._buffer.write("Current size of image file: " + str(size) + " Bytes.")
            time1 = self._status.getElapsedTime()
            mins = str (int(time1) / 60)
            if len(mins) < 2:
                mins = '0' + mins
            secs = str (int(time1) % 60)
            if len(secs) < 2:
                secs = '0' + secs
            self._buffer.write(" Time elapsed: %s:%s" %(mins,secs))
            self._buffer.flush()
            time.sleep (OUTPUT_DELAY)
        
if __name__ == "__main__":
    arguments = sys.argv
    cli = ImageGeneratorCLI()
    cli.startCLI()
    
