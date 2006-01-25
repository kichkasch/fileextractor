"""
CoreManager for the ImageGenerator - chooses the right implementation for the execution.

The Singleton pattern has been implemented for this module. This way, there should also
only be one instance of the class L{CoreManager}, which may be accessed using the 
L{getInstance} method.

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)

@var _instance: Singelton Pattern - holds an instance of the type CoreManager. Should be the only 
instance for the entire program.
@type _instance: L{CoreManager.CoreManager}
"""
import GeneratorCoreAbstract

class CoreManager:
    """
    Maintains implementations for cores for different operating systems.
    
    A dictionary is maintained and whenever a new core is registered using the function
    L{registerCore} the implementation is saved with the name as key. Using the 
    function L{getCoreClass} the implementation may be requested.
    
    Take care, that whenever you register an implementation it should inherit from the
    class L{GeneratorCoreAbstract.CoreInterface} and overwrite all the methods
    defined in there.
    
    @ivar _cores: A dictionary maintaining the implementations
    @type _cores: C{Dict} with Key (Name as C{String}) and Value (Implementation as C{Class})
    """
    def __init__(self):
        """
        Initialises the CoreManager instance.
        
        Initialisation of the core dictionary.
        """
        self._cores = {}
    
    def registerCore(self, coreName, className):
        """
        Adds a new core implementation to the core manager.
        
        If there is not key in the dictionary with the name L{coreName} a new entry will
        be added with the given parameters.
        
        @param coreName: Name of the implementation (should be the OS name)
        @type coreName: C{String}
        @param className: Class of the implementation
        @type className: C{Class} (NOT C{String}!!!)
        """
        if not self._cores.has_key(coreName):
            self._cores[coreName] = className
    
    def getCoreClass(self, coreName):
        """
        Returns a core implementation for the given core name.
        
        @return: Value in the dictionary for the given key
        @rtype: Implementation of L{GeneratorCoreAbstract.CoreInterface}
        """
        return self._cores[coreName]
        
    def getListOfCoreNames(self):
        """
        Returns a list with the names of available core implementations.
        
        @return: List of core implementations
        @rtype: C{List} of C{Strings}
        """
        coreNames = self._cores.keys()
        return coreNames

_instance = None
def getInstance():
    """
    Getter method for Singleton implementation.
    
    You may always access an instance of type CoreManager using this method. If this method is called for the
    very first time on instance of type CoreManager is created and stored in an instance variable. The content
    of this instance variable is returned finally.
    
    @return: Reference to the only instance of a Manager
    @rtype: L{CoreManager.CoreManager}
    """
    global _instance
    if _instance == None:
        _instance = CoreManager()
    return _instance

import GeneratorCoreLinux
import GeneratorCoreWin32
