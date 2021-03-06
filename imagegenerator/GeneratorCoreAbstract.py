"""
Interface for Core for the ImageGenerator - all implementations should inherit from the class in here
and overwrite its methods.

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

class CoreInterface:
    """
    Abstract class for all core implementations (for the different operating systems). All 
    methods should be overwritten.
    
    @ivar _implementationName: Name of the implementation.
    @type _implementationName: C{String}
    """
    def __init__(self, implementationName):
        """
        Call this constructor from your super class with one parameter - a name for your
        implementation (the os name).
        
        @param implementationName: Name of the implementation inhereting from this class
        @type implementationName: C{String}
        """
        self._implementationName = implementationName
        
    def getImplementationName(self):
        """
        GETTER
        
        @return: The name of the implementation for this instance.
        @rtype: C{String}
        """
        return self._implementationName

    def createImage(self, status):
        """
        Central function of a core. Must be overwritten by every core implementation.
        """
        pass
        
    def getPossibleSources(self):
        """
        If any core implementation is able to provide some information about sources (devices),
        which are commonly used for imaging, put them into this function when overwriting this
        class.
        """
        pass

    def getSourceInfo(self):
        """
        When overwriting this function, explain in here what you did in L{getPossibleSources}. This
        information may be displayed to the user and they know what the list above is about
        and where the information was extracted from.
        """
        pass

    def getDefaultDDLocation(self):
        """
        This function should be overwritten in order to provide a default location for the dd
        command for this implementation.
        """
        return None

    def getSizeEstimationForPartition(self, partitionName):
        """
        Overwrite here if your core is able to estimate the size of a partition.
        """
        return None
        
