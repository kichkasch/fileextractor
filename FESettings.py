"""
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

#
# Settings for FileExtractor
#

# 1st part: Application specific settings
PROGRAM_NAME = "FileExtractor"
VERSION = "1.0.2"
AUTHOR = "Michael Pilgermann"
EMAIL = "kichkasch@gmx.de"
URL = "http://freshmeat.net/projects/fileextractor"
COPYRIGHT = "(C) 2010 " + AUTHOR
BASEDIR = "/opt/fileextractor"  # FIX ME


# 2nd part: user specific settings
DEFAULT_FILE = 'fileextractor_settings.dat'
DEFAULT_LOCATION  ='.'

settings = None
def getSettings():
    """
    'Singleton'
    """
    global settings
    if not settings:
        settings = Settings()
    return settings

class Settings:

    def __init__(self):
        self._values = {}
        self._comments = {}
        
    def load(self, filename = DEFAULT_FILE, location = DEFAULT_LOCATION):
        import os.path
        try:
            file = open(os.path.join(location, filename), 'r')
        except IOError, msg:
            # fair enough; there is not yet any settings on this machine
            return
        line1 = ' '
        line2 = ' '
        while line1 and line2:
            comment = file.readline()
            if comment and not comment[0] == "#":
                line1 = comment
                comment = None
            else:
                line1 = file.readline()
            if line1:
                line2 = file.readline()
                if line2:
                    self._values[line1.strip()] = line2.strip()
                    if comment:
                        self._comments[line1.strip()] = comment.strip()
                    #print ("%s: %s (%s)" %(line1, line2, comment))
        
    def save(self, filename = DEFAULT_FILE, location = DEFAULT_LOCATION):
        import os.path
        file = open(os.path.join(location, filename), 'w')
        for key in self._values.keys():
            if self._comments.has_key(key):
                file.write("%s\n" %self._comments[key])
            file.write("%s\n" %(key))
            file.write("%s\n" %(self._values[key]))
        file.close()
        
    def getValue(self, key):
        try:
            return self._values[key]
        except KeyError, msg:
            return None
        
    def setValue(self, key, value):
        self._values[key] = value
        
    
