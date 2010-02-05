#!/usr/bin/env python
"""
Command Line interface for the FileExtractor. Initialises and starts the fileextractor core.

This module can start the application. It is checking for the call of the __main__ function and
will in case of activate the core.

@author: Michael Pilgermann
@contact: mailto:kichkasch@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)
"""
import FileExtractorCore
import tools
import signatures
import sys
from ExecutionSettings import ExecutionSettings
from ExecutionSettings import ExecutionStatus
from ExecutionSettings import def_digits

def usage(programname):
    """
    Displays the usage text to standard output.
    
    @param programname: Name of the program (usually first argument of the CLI argument list)
    """
    print ""
    print "Usage: %s [-sX] [-eX] [-dX] [-nX] [-fS] [-o{1|2|3}] filename" %programname
    print ""
    print "Parameters"
    print "\t-sX\tStart position inside file for searching (default 0)"
    print "\t-eX\tEnd position inside file for searching (default filesize)"
    print "\t-dX\tNumber of digits for numbering the files (default %d)" %def_digits
    print "\t-nX\tNumber of first file to create (default 0)"
    print "\t-fS\tDestination folder for extracted files (default current directory)"
    print "\t-oX\tOutput level (1-progress; 2-percentage/occurences; 3-full debug) - (default 2)"
    print "\t-gX\tOutput frequency - depending on the size: filesize/X (default 100)"
    print "\t-iY\tSignature operations"
    print "\t\t-is\tShow available signaturs"
    print "\t\t-idS\tDisable Signature with name S"
    print ""

def handleArguments(args):
    """
    Processes a list of arguments.
    
    Creates a new L{ExecutionSettings} and a new L{ExecutionStatus} object.
    Iterates the list of arguments and assigns any known argument value to the given 
    settings or status instance.
    
    @param args: List of arguments to be processed (usually the CLI arguments list)
    @return: Info about success: 0 - not successful, 1 - Signature information is requested,
    2 - successful; The settings applied to the Settings / Status instances
    @rtype: C{int}; L{ExecutionStatus}
    """
    if len(args) < 2:
        usage(args[0])
        return 0, None
    settings = ExecutionSettings(signatures = signatures.getCopyOfAllSignauteres())
    status = ExecutionStatus(settings)
    disabled_signs = []
    for arg in args:
        if arg[0] != '-':
            continue
        if arg[1] == 's':
            status.file_start = int(arg[2:])
        elif arg[1] == 'e':
            status.file_end = int(arg[2:])
        elif arg[1] == 'd':
            settings.digits = int(arg[2:])
        elif arg[1] == 'n':
            settings.counterstart_global = int(arg[2:])
        elif arg[1] == 'f':
            settings.dest_folder = arg[2:]
        elif arg[1] == 'o':
            settings.output_level = int(arg[2:])
        elif arg[1] =='g':
            settings.output_frequency = int(arg[2:])
        elif arg[1] =='i':
            if arg[2] == 's':
                return 1, status
            elif arg[2] == 'd':
                disabled_signs.append(arg[3:])
            else:
                print ('Unrecognised option for Signature operations: %c [Ignored]' %(arg[2]))
        else:
            print ('Unrecognised option: %c [Ignored]' %(arg[1]))
    settings.dest_folder = tools.checkDestfolder(settings.dest_folder)
    settings.sourceFiles.append(args[len(args)-1])
    settings.disableSignatureWithNames(disabled_signs)
    return 2, status

def printHeader(status):
    """
    Display information about the settings for the current application execution on standard sutput.
    
    @param status: Information container for current execution.
    @type status: L{ExecutionStatus}
    """
    signs = status.settings.signatures
    binfilename = status.getCurrentFile()
    size = status.getCurrentSize()
    print "\nSearching for Files inside Files"
    print "--------------------------------"
    print "The following signatures are activated:"
    for sig in signs:
        print ('\t%s\t: %s' %(sig[signatures.name], sig[signatures.description]))
    print ('\nFile to search in: %s (%d Bytes)\n' % (binfilename, size))
    print "Settings:"
    print "\tRead from: 0x%x to: 0x%x" %(status.file_start, status.file_end)
    print "\tDigits for running number: %d" %status.settings.digits
    print "\tStart counting from: %d" %status.settings.counterstart_global
    print "\tTarget Directory: %s" %status.settings.dest_folder
    print "\tOutput Level: %d" %status.settings.output_level
    print ""
    
def printResults(signs, counter, time_passed):
    """
    Displays the results for the performed execution to standard output.
    
    @param signs: Signatures which were active for this execution.
    @type signs: C{dict}
    @param counter: Number of found files for each signature for the last execution.
    @type counter: C{dict}
    @param time_passed: Time passing during the execution.
    @type time_passed: C{float}
    """
    print "--------------------------------"
    print "\nSearch finished - results:"
    print "\nThe following number of files were found and stored:"
    for sig in signs:
        print ('\t%s\t: %d File(s)' %(sig[signatures.name], counter[sig[signatures.name]]))
    print ('Overall processing time: %f seconds' %time_passed)

def startCLI(argv):
    """
    Starts the CLI application
    
    An L{ExecutionSettings} object is intialised and passed to the method L{handleArguments}, which
    assigns the appropriate values. Afterwards, the FileExtractor core is initialised and
    started with the given source file.
    
    @param argv: List of arguments processed by the application (CL arguments)
    """
    ret, status = handleArguments(argv)
    if ret==0:
        sys.exit()
        
    if ret == 1:
        signatures.printSignatures(status.settings.getActiveSignatures())
        sys.exit()
    
    if FileExtractorCore.init(status) < 0:
        sys.exit()

    printHeader(status)
    signs, counter = FileExtractorCore.startSearch(status)
    printResults(signs, counter, status.getRunTimeForNumber(0))
    
if __name__ == "__main__":
    startCLI(sys.argv)
