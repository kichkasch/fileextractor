#
# Settings for FileExtractor
#

DEFAULT_FILE = 'fileextractor_settings.dat'
DEFAULT_LOCATION  ='.'

settings = None
def getSettings():
    global settings
    if not settings:
        settings = Settings()
    return settings

class Settings:

    def __init__(self):
        self._values = {}
        
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
            line1 = file.readline()
            if line1:
                line2 = file.readline()
                if line2:
                    self._values[line1.strip()] = line2.strip()
        
    def save(self, filename = DEFAULT_FILE, location = DEFAULT_LOCATION):
        import os.path
        file = open(os.path.join(location, filename), 'w')
        for key in self._values.keys():
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
        
    
