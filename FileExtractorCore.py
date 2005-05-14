#!/usr/bin/python
"""
The core of the FileExtractor. 

May be invoked either by the GUI frontend or the CLI interface. A status instance needs to
be passed (with is references settings instance), which will be used for configuring the
core. The status object is always kept up-to-date and may be read from the calling 
frontend.

How to use the core: From the core you may request the list of available signatures. Using 
this information a L{ExecutionSettings.ExecutionSettings} instance may be created and all
the information for source file names etc. may be applied. (see module L{ExecutionSettings} for
details. Afterwards, an L{ExecutionSettings.ExecutionStatus} instance has to be created - the core 
will use it to put up-to-date information about the execution in there. Pass the status instance
to the core. (In order to take advantage of the status object you have to run the core in a seperate 
thread). Use a timer and look for changes in the status object frequently.

The core handles exactly one source file. The iteration over a list of source files has to
be performed by the calling frontend. However, the status object is handled in a way,
that overall information for all source files are contained.

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)

@var maxlength: For internal processing - Indicates the maximum length for sequences in signatures (both
start and end sequences) - important for prefetching characters from the source files.)
@var start: For internal processing - Remembers, which file types have been started currently. This way
files may even be identified when they are stored within other files. (such as thumbnails) However, it
is not possible to find a file inside a file if both are of the same type.
@var skipped: For internal processing - some file types (end type 1) need skipping of end sequences. This dictionary
is responsible for remebering the skipped end sequences for all file types.
@var size: Size of the current source file.
@var binfile: Reference to the current source file descriptor.
"""
import struct
import os.path
import signatures
from tools import checkString
from tools import writeFile
import tools
import time

def getAvailableSignatures():
    """
    Forwards the request for available signatures to the signatures module. Normalises
    the output from this function (checks the signaturs).
    
    @return: C{None} if error in signatures file, otherwise the list of signatures.
    @rtype: C{List} of C{Signatures}
    """
    signs = signatures.getCopyOfAllSignauteres()
    if signatures.normaliseSignatures(signs) == -1:
        return None
    return signs

def init(status_passed):
    """
    Initalises the core for execution for one source file
    
    Variables for maximal signature sequence length, found start sequences,
    counters are reseted and the source file is opened. The status instance
    is updated and informed about the success of intialisation.
    
    @param status_passed: Status instance containing all information for the current execution.
    @type status_passed: ExecutionSettings.ExecutionStatus
    
    @return: Indicates, whether the initialisation was sucessful. (-1 / -2 for problems with signature file; 0 for success)
    @rtype: C{int}
    """
    global maxlength, start, skipped, size, binfile
    
    status = status_passed
    settings = status.settings

    settings.dest_folder = tools.checkDestfolder(settings.dest_folder)
    
    binfilename = status.getCurrentFile()
    binfile = open(binfilename, 'rb')

    if status.file_start == None:
        status.file_start = 0
    if status.file_end == None or status.file_end > os.path.getsize(binfilename):
        status.file_end = os.path.getsize(binfilename)

    counter = status.counter
    counterr = status.counterr   # for continue counting
    start = {}
    skipped = {}

    for j in settings.signatures:
        counter[j[signatures.name]] = 0
        start[j[signatures.name]] = -1
        skipped[j[signatures.name]] = 0
    

    size = status.file_end - status.file_start
    maxlength = signatures.normaliseSignatures(settings.signatures)
    if maxlength == -1:
        print ('Error in Signature File - required Entry missing in at least one signature')
        return -1
    if maxlength == -2:
        print ('Error in Signature File - wrong value for at least one signature')
        return -2
    disabled = signatures.disable(settings.signatures, settings.disabled_signatures)
    status.initialisedOne()
    return 0

    
def startSearch(status_passed):
    """
    Invokes the search on the file.
    
    Central bit of the core - examines the source file byte by byte and checks against the
    provided start sequences of files (provided by the signatures). Ones, a start sequence
    has been found, the further actions depend on the type of signature (in fact, how the end
    of the file is identified - by end sequence, file size info inside file or manual by
    additional module).
    
    The status object is constantly updated. The frequency of updating the status instance with
    progress within a source file depends on the value in the settings instance (
    ExecutionSettings.ExecutionSettings.output_frequency) In fact, this variable says how often
    a message shall be sent to the status object in total for the current source file.
    
    @param status_passed: Reference to the status instance for applying runtime information and
    gaining settings for the running.
    @type status_passed: ExecutionSettings.ExecutionStatus
    return: Active Signatures; Overall Counter
    rtype: C{List} of C{Signatures}; C{int}
    """
    global binfile, start, skipped, size, maxlength
    global status
    status= status_passed
    st = binfile.read(maxlength-1)

    dx = size / status.settings.output_frequency           # for user output only
    x = dx                                  # same here    
    
    file_pos = binfile.tell()
    status.startedOneSourceFile(size)
    
    while 1:
        c = ''
        if file_pos < status.file_end:
            c = binfile.read(1)
        file_pos = binfile.tell()
        if c!='':               # end of file
            st += c
    
        if file_pos-status.file_start >= x:
            status.updateFineshedForCurrent(file_pos-status.file_start)
            
            if status.settings.output_level == 3 and size!=0:
                print "Pos: 0x%x - %d / %d KB (%d %%)" %(file_pos, (file_pos-status.file_start)  / 1024 , size / 1024, (file_pos-status.file_start)*100/size)
            elif status.settings.output_level == 2:
                print "%d %%" %((file_pos-status.file_start)*100/size)
            elif status.settings.output_level == 1:
                print '#' ,
            x += dx
            
        for sig in status.settings.signatures:
            if start[sig[signatures.name]] == -1:
                if sig[signatures.start_seq][0] == ord(st[0]):
                    if checkString(st, sig[signatures.start_seq]):
                        start_pos = file_pos-len(st)
                        if status.settings.output_level == 3:
                            print ('Found start at 0x%x for %s' %(start_pos, sig[signatures.description]))
                        if sig[signatures.filesize_type] == signatures.TYPE_FILE_SIZE:
                            offsets = sig[signatures.filesize_address_offsets]
                            ofs = 0
                            for i in offsets:
                                binfile.seek(start_pos + i)
                                val = ord(binfile.read(1))
                                ofs = ofs * 256 + val
                            end_pos = start_pos + ofs
                            correction = sig[signatures.filesize_info_correction]
                            end_pos = end_pos + correction
                            writeFile(sig[signatures.name],status.counterr[sig[signatures.name]]+status.settings.counterstart_global,
                                  sig[signatures.extension],binfile, start_pos, end_pos-1,
                                  status.settings.dest_folder, status.settings.output_level == 3, status)
                            status.counter[sig[signatures.name]] += 1
                            status.counterr[sig[signatures.name]] += 1
                            status.foundFile()
                            binfile.seek(file_pos)
                        elif sig[signatures.filesize_type] == signatures.TYPE_MANUAL:
                            function = sig[signatures.filesizemanual_functionname]
                            if status.settings.output_level == 3:
                                print ('-- Enter signature defined function for end address determination for this file')
                            end_address = function(binfile, start_pos, status.settings.output_level == 3)
                            if (end_address < start_pos):
                                if status.settings.output_level == 3:
                                    print ('-- No valid end address found - skip this file.')
                                continue
                            writeFile(sig[signatures.name],status.counterr[sig[signatures.name]]+status.settings.counterstart_global,
                                  sig[signatures.extension],binfile, start_pos, end_address,
                                  status.settings.dest_folder, status.settings.output_level == 3, status)
                            status.counter[sig[signatures.name]] += 1   
                            status.counterr[sig[signatures.name]] += 1   
                            status.foundFile()
                            binfile.seek(file_pos)
                        else:
                            start[sig[signatures.name]] = start_pos
            else:
                if file_pos < start[sig[signatures.name]] + len(sig[signatures.start_seq]):
                    continue
                if sig[signatures.end_seq][0] == ord(st[0]):
                    if tools.checkString(st, sig[signatures.end_seq]):
                        end_pos = file_pos-len(st)+len(sig[signatures.end_seq])-1
                        if skipped[sig[signatures.name]] < sig[signatures.skip_end_seqs]:
                            skipped[sig[signatures.name]] +=1
                            if status.settings.output_level == 3:
                                print ('Found end at 0x%x for %s - skipped' %(end_pos, sig[signatures.description]))
                            continue
                        if status.settings.output_level == 3:
                            print ('Found end at 0x%x for %s' %(end_pos, sig[signatures.description]))
                        writeFile(sig[signatures.name],status.counterr[sig[signatures.name]]+status.settings.counterstart_global,
                                sig[signatures.extension],binfile, start[sig[signatures.name]], end_pos,
                                status.settings.dest_folder, status.settings.output_level == 3, status)
                        start[sig[signatures.name]] = -1
                        status.counter[sig[signatures.name]] += 1
                        status.counterr[sig[signatures.name]] += 1
                        status.foundFile()
                        skipped[sig[signatures.name]] = 0
            
        if len(st)==1:
            break
        st = st[1:]
    
    status.finishedOneSourceFile()
    return status.settings.signatures, status.counterr
    
