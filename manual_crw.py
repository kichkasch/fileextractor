"""
Extension for signatures. CRW in the signatures module is marked as signature type
manual. This module is the extension in order to dertermine the end of a CRW file
within a binfile.

In fact, this is a very dirty implementation - but seems to work for the pics we extracted
from a partition for a speciifc camera. (It asumes 3 entries in  the "main dir" within the file
and the first entry must be of type 0x0520) - check CRW docs for more details.

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)

@var sequ: Sequence for starting the directory at the end of a CRW file
@type sequ: C{List} of C{int}
@var sequ_zeros: 5 bytes in a row are at a certain position quite at the end of our CRW files
@type sequ_zeros: C{List} of C{int}
@var sequ1: Another sequence which was at the same location within all our CRW files right at the end.
@type sequ1: C{List} of C{int}
@var sequ2: Again, another sequence which was at the same location within all our CRW files right at the end.
@type sequ2: C{List} of C{int}
"""

import tools

sequ = [0x03, 0x00, 0x05, 0x20]
sequ_zeros = [0x00, 0x00, 0x00, 0x00, 0x00]
sequ1 = [0x07, 0x20]
sequ2 = [0x0A, 0x30]

def crw_getendaddress(file, offset, debug_output):
    """
    Calculate the end address of a CRW file.
    
    This function must be implemented with exactly these parameters in order to use it for
    the L{FileExtractorCore}. It determines the end of a CRW file within a binary source file.
    
    When examing several examples of CRW files and taking some documentation of this file format
    in addition it could be outworked that right at the end of a CRW file kind of a directory
    is stored. Luckyly for us, some sequences in there appeared at exactly the same position within
    the example files measured from the end of the file. These circumstances enable us to estimate
    the end of a CRW file. Not sure, whether is works for all CRWs, but it worked for ours and
    recovered more than 2000 pictures.
    
    @param file: Source file the start sequence was found in
    @type file: Reference to a file
    @param offset: Position of the start sequence within the source file
    @type offset: C{int}
    @param debug_output: Indicates, whether to produce output to standard out.
    @type debug_output: C{Boolean}
    
    @return: -1 if the end of the file could not be determined, otherwise the offset inside the
    source file for the end of the found file measured from the beginning of the source file.
    @rtype: C{int}
    
    @attention: There is no limitation implemented for the file size of the found file. Consequently,
    this function will examine the source file from the start offset up to the end, which can
    take quite a while.
    @todo: Implement a break criterion and limit the file size.
    """
    if debug_output:
        print ("\tEntered function in additional module manual_crw for calculating")
        print ("\tend address for CRW file (depending on the file size this may last several minutes)")
    st = file.read(len(sequ)-1)
    while (len(st)>1):
        ch = file.read(1)
        st = st + ch
        if ord(st[0]) == sequ[0]:
            if tools.checkString(st, sequ):
                pos = file.tell() - len(sequ)
                file.seek(pos + 7)
                st1 = file.read(5)
                if tools.checkString(st1, sequ_zeros):
                    file.seek(pos + 12)
                    st2 = file.read(2)
                    if tools.checkString(st2, sequ1):
                        file.seek(pos + 22)
                        st2 = file.read(2)
                        if tools.checkString(st2, sequ2):
                            if debug_output:
                                print("\t--- Leave function - calculated end address: 0x%x" %(pos+35))
                            return pos + 35
        st = st[1:]
    if debug_output:
        print ("\t--- Leave function now - no end address could be determined")
    return -1
