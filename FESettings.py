"""
Loading and saving configurations - based on ConfigObj 
(see http://www.voidspace.org.uk/python/articles/configobj.shtml)

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

from configobj  import ConfigObj  #requires python-configobj
import os.path

#
# Settings for FileExtractor
#

# 1st part: Application specific settings
PROGRAM_NAME = "FileExtractor"
VERSION = "1.0.3"
AUTHOR = "Michael Pilgermann"
EMAIL = "kichkasch@gmx.de"
URL = "http://freshmeat.net/projects/fileextractor"
COPYRIGHT = "(C) 2010 " + AUTHOR
BASEDIR = "/opt/fileextractor"  # FIX ME


# 2nd part: user specific settings
DEFAULT_FILE = 'fileextractor_settings.ini'
DEFAULT_LOCATION = os.path.join(os.environ.get('HOME'), '.fileextractor') 

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
        self._config = {}
        
    def load(self, filename = DEFAULT_FILE, location = DEFAULT_LOCATION):
        if os.path.exists(os.path.join(location, filename)):
            self._config = ConfigObj(os.path.join(location, filename))
        else:
            self._config = ConfigObj()
            self._config.filename = os.path.join(location, filename)
            for key, value in DEFAULTS.iteritems():
                self.setValue(key, value)
        
    def save(self, filename = None, location = None):
        if filename and location:
            self._config.filename = os.path.join(location, filename)
        self._config.write()
        
    def getValue(self, key):
        try:
            return self._config[key]
        except KeyError, msg:
            return None
        
    def setValue(self, key, value):
        self._config[key] = value
        

DEFAULTS = {
            "ig_location_dd": "/bin/dd", 
            "signatues_off" : "", 
            "naming_start" : "1", 
            "ig_output_dir" : "/tmp", 
            "ig_output_filename" : "fileextractor.img", 
            "output_dir" : "/tmp", 
            "ig_default_core" : "Linux", 
            "naming_digits" : "5", 
            "command_sudo" : "gksudo --message 'Imaging needs root priveliges - Please provide password!'"
}
