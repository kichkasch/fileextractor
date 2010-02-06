"""
The new and fast core of the FileExtractor. 

This module is only a stub. The actual implementation has now been shifted to a C-Module. This way
the extracting process can be speeded up significantly.

It provides exactly the same interface as the original FileExtractorCore.

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
"""

def getAvailableSignatures():
    return None
    
def init(status_passed):
    return None
    
def startSearch(status_passed):
    return None
