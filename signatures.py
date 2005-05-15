"""
Maintains all signatures for FileExtractor.

Each sequence in here is responsible for one file type. All file types are identified by start sequences.
Basically, three different types of signatures are available. They are different in the determination
of the end of files. Type one (indicated by L{TYPE_END_SEQUENCE}) provides an end sequence for the file
type. Type two (indicated by L{TYPE_FILE_SIZE}) indicates, that the information about the file size
is encoded in the file itself - the offset has to be provided measured from the beginning of the
file. Type three (indicated by L{TYPE_MANUAL}) is for the remaining file types. Non of the two previous
ways may be used for a file type - so there is still a way to implement yourself the algorithm for
finding the end of a file. For more information on signatures please check the project web-site.

Each signature (file type) is represented by a dictionary. Each dictionary must provide certain keys. 
The strings for the required keys are provided in this module. (L{name} for the UNIQUE name of 
a signature, L{description} for an optional description, L{extension} for the file extension, 
L{start_seq} for the start sequence and L{filesize_type} for the type of signauture; i.e how to
identify the end of a file. Further fields are available; however, there requirements depends on 
the signature type. These ones are L{end_seq} (Type 1), L{skip_end_seqs} (Type 1), 
l{filesize_address_offset} (Type 2), L{filesize_info_correction} (Type 2) and 
L{filesizemanual_functionname} (Type 3). After all a global C{List} is maintains which holds 
all the signatures (L{signs}). Take care, that after creating the dictionary for a new signature,
you don't forget to add the dictionary to the list.

Finally, some functions are provided, dealing with signature related problems.

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)

@var signs: List of Signatures
@type signs: C{List} of C{Dictionaries}
@var name: Key value for the dictionary entry for name
@type name: C{String}
@var description: Key value for the dictionary entry for description
@type description: C{String}
@var extension: Key value for the dictionary entry for extension
@type extension: C{String}
@var start_seq: Key value for the dictionary entry for start_seq
@type start_seq: C{String}
@var end_seq: Key value for the dictionary entry for end_seq
@type end_seq: C{String}
@var skip_end_seqs: Key value for the dictionary entry for skip_end_seqs
@type skip_end_seqs: C{String}
@var filesize_type: Key value for the dictionary entry for filesize_type
@type filesize_type: C{String}
@var filesize_address_offsets: Key value for the dictionary entry for filesize_address_offsets
@type filesize_address_offsets: C{String}
@var filesizemanual_functionname: Key value for the dictionary entry for filesizemanual_functionname
@type filesizemanual_functionname: C{String}
@var filesize_info_correction: Key value for the dictionary entry for filesize_info_correction
@type filesize_info_correction: C{String}
@var TYPE_END_SEQUENCE: Constant variable - assigned to signature dictionary key filesize_type if Type 1
@type TYPE_END_SEQUENCE: C{int}
@var TYPE_FILE_SIZE: Constant variable - assigned to signature dictionary key filesize_type if Type 2
@type TYPE_FILE_SIZE: C{int}
@var TYPE_MANUAL: Constant variable - assigned to signature dictionary key filesize_type if Type 3
@type TYPE_MANUAL: C{int}
"""

TYPE_END_SEQUENCE = 0
TYPE_FILE_SIZE = 1
TYPE_MANUAL = 2

signs = []
name = 'name'
description = 'description'
extension = 'extension'
start_seq = 'start_sequence'
end_seq = 'end_sequence'
skip_end_seqs = 'skip_end_seqs'     # required for jpegs - the first occurence for the end sequence needs to be skipped
filesize_type = 'filesize_type'
filesize_address_offsets = 'filesize_addresses'
filesizemanual_functionname = 'manual_functionname'
filesize_info_correction = 'filesize_info_correction'

# signature for jpeg files
_jpeg = {}
_jpeg[name] = 'JPEG'
_jpeg[description] = 'JPEG Image File'
_jpeg[extension] = 'jpeg'
_jpeg[start_seq] = [0xFF, 0xD8, 0xFF, 0xE1]
_jpeg[end_seq] = [0xFF, 0xD9]
_jpeg[skip_end_seqs] = 1
_jpeg[filesize_type] = TYPE_END_SEQUENCE

_bmp = {}
_bmp[name] = 'BMP'
_bmp[description] = 'Bitmap Image File'
_bmp[extension] = 'bmp'
_bmp[start_seq] = [0x42, 0x4D, None, None, None, None, 0x00, 0x00, 0x00, 0x00, 0x36, None, 0x00, 0x00]
_bmp[filesize_address_offsets] = [0x05,0x04,0x03,0x02]
_bmp[filesize_type] = TYPE_FILE_SIZE

_gif = {}
_gif[name] = 'GIF'
_gif[description] = 'GIF Image File'
_gif[extension] = 'gif'
_gif[start_seq] = [0x47, 0x49, 0x46, 0x38]
_gif[end_seq] = [0x00, 0x3B]
_gif[skip_end_seqs] = 0
_gif[filesize_type] = TYPE_END_SEQUENCE

# signature for CRW  files (Canon picture file format)
# mpilgerm 2005-04-15
_crw = {}
_crw[name] = 'CRW'
_crw[description] = 'CRW Image File'
_crw[extension] = 'crw'
_crw[start_seq] = [0x49, 0x49, 0x1A, 0x00, 0x00, 0x00, 0x48, 0x45, 0x41, 0x50, 0x43, 0x43, 0x44, 0x52]
_crw[filesize_type] = TYPE_MANUAL
import manual_crw
_crw[filesizemanual_functionname] = manual_crw.crw_getendaddress

# signature for CR2  files (Canon picture file format)
# mpilgerm 2005-04-14
_cr2 = {}
_cr2[name] = 'CR2'
_cr2[description] = 'CR2 Canon Picture File'
_cr2[extension] = 'cr2'
_cr2[start_seq] = [0x49, 0x49, 0x2A, 0x00, 0x10, 0x00, 0x00, 0x00, 0x43, 0x52, 0x02, 0x00]
_cr2[end_seq] = [0xFF, 0xD9]
_cr2[skip_end_seqs] = 2
_cr2[filesize_type] = TYPE_END_SEQUENCE

# signature for THM  files (Canon picture help file format)
# mpilgerm 2005-04-14
_thm = {}
_thm[name] = 'THM'
_thm[description] = 'THM Canon Picture Thumbnail File'
_thm[extension] = 'thm'
_thm[start_seq] = [0xFF, 0xD8, 0xFF, 0xE1, 0x09, 0xFE, 0x45, 0x78, 0x69, 0x66, 0x00, 0x00, 0x49, 0x49]
_thm[end_seq] = [0xFF, 0xD9]
_thm[skip_end_seqs] = 0
_thm[filesize_type] = TYPE_END_SEQUENCE

# signature for WAV Files
# mpilgerm 2005-04-25
# more info: http://ccrma.stanford.edu/courses/422/projects/WaveFormat/
_wav = {}
_wav[name] = 'WAVE'
_wav[description] = 'WAVE Music File'
_wav[extension] = 'wav'
_wav[start_seq] = [0x52, 0x49, 0x46, 0x46]
_wav[filesize_address_offsets] = [0x07, 0x06, 0x05, 0x04]
_wav[filesize_info_correction] = 8
_wav[filesize_type] = TYPE_FILE_SIZE

# signature for PNG Picture files
# http://download.mirror.ac.uk/sites/www.libpng.org/pub/png/spec/1.2/png-1.2-pdg.html
# mpilgerm 2005-05-15
_png = {}
_png[name] = 'PNG'
_png[description] = 'Portable Netowrk Graphics (PNG) Picture File'
_png[extension] = 'png'
_png[start_seq] = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
_png[end_seq] = [0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82]
_png[skip_end_seqs] = 0
_png[filesize_type] = TYPE_END_SEQUENCE


# #######################################################
# put your own signatures here
#
# make sure that the name is unique within the entire list
# don't forget to add them to the signatures list at the end of this file



# #######################################################
# (de) activate signatures

signs.append(_jpeg)
signs.append(_bmp)
signs.append(_gif)
signs.append(_cr2)
signs.append(_thm)
signs.append(_crw)
signs.append(_wav)
signs.append(_png)


# #######################################################
# functions
#

def getCopyOfAllSignauteres():
    """
    Provides a list of copies of each signature.
    
    @return: List of copies of signatures
    @rtype: C{List} of Signatures Dictionaries
    """
    ret = []
    for sig in signs:
        ret.append(sig)
    return ret

def normaliseSignatures(signs):     # returns the size of the longest signature
    """
    Chechs the given signatures for mistakes.
    
    Iterates the given list of signatures and checks whether all the required keys for the
    dictionaries for each signatures are avaiable and valid depending on their signature
    type.
    
    Furthermore, the maximum length of binary signatures is stored. Both start and end
    sequences are involved in this process. This number is returned by the function.
    
    @param signs: List of signatures to be examined
    @type signs: C{List} of Signatures C{Dictionaries}
    @return: Maximum length of (start / end) sequence
    @rtype: C{int}
    """
    maxlength = 1
    for sig in signs:
        if not sig.has_key(filesize_type):
            return -1
        if not sig.has_key(name):
            return -1
        if not sig.has_key(start_seq):
            return -1
        if sig[filesize_type] == TYPE_END_SEQUENCE and not sig.has_key(end_seq):
            return -1
        if sig[filesize_type] == TYPE_FILE_SIZE and not sig.has_key(filesize_address_offsets):
            return -1
        if sig[filesize_type] == TYPE_MANUAL and not sig.has_key(filesizemanual_functionname):
            return -1
        if sig[name].strip() == '':
            return -2
        if len(sig[start_seq]) > maxlength:
            maxlength = len(sig[start_seq])
        if sig[filesize_type] == TYPE_END_SEQUENCE:
            if len(sig[end_seq]) > maxlength:
                maxlength = len(sig[end_seq])
            if not sig.has_key(skip_end_seqs):
                sig[skip_end_seqs] = 0
        if sig[filesize_type] == TYPE_FILE_SIZE:
            if not sig.has_key(filesize_info_correction):
                sig[filesize_info_correction] = 0
        if not sig.has_key(description):
            sig[description] = 'no description'
        if not sig.has_key(extension):
            sig[extension] = ''
        
    return maxlength
        
def printSignatures(signs):
    """
    Displays a small table with information about each signature to standard output.
    
    Iterates the given list of signatures and prints the name, description and 
    extension for each of them in form of a table.
    
    @param signs: List of signatures to be printed
    @type signs: C{List} of Signature C{Dictionaries}
    """
    print "Available Signatures"
    print "--------------------"
    for sig in signs:
        print ('\t%s\t- %s (Ext: %s)' %(sig[name], sig[description], sig[extension]))
    print ""
    
def disable(signs, neg_list):
    """
    Removes the entires from a negative list in the list of signatures.
    
    Iterates the items in the negative list and checks whether they are existent in the given
    list of signatures. If this is the case, this item is removed from the list. The point of this
    function is the handling of two different types of list; the signature list is a list of
    signature dictionaries, the negative list instead is a list of strings with names of
    signatures.
    
    This function does not perform its operations on a copy of the signatures list. Consequently,
    the returned list is a reference to the same list as given as a parameter. If you still need
    the full list afterwards make a copy before.
    
    @param signs: List of signatures where the items shall be removed from.
    @type signs: C{List} of Signature {Dictionaries}
    @param neg_list: List of signature names to be removed from the signature list
    @type neg_list: C{List} of C{Strings}
    @return: List of signatures not containing any signature named in the negative list
    @rtype: C{List} of Signature {Dictionaries}
    """
    disabled = []
    for neg in neg_list:
        for sig in signs:
            if neg == sig[name]:
                disabled.append(sig)
                signs.remove(sig)
                break
    return disabled
