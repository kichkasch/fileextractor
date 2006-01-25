#!/usr/bin/env python
"""
Graphical interface for the ImageGenerator. Contains the MainFrame (a wizard) and a simple Application for
starting up the ImageGenerator GUI Frontend.

Furthermore, a callback for the wizard is implemented to react on certain events, namly the cancel and the 
finished action from the wizard. An application using the ImageGenerator may also receive callbacks about
the sucess of the generation - a default callback is implemented, namely the ref{ImagingCallback}, which
produces some very basic output to standard out.

The GUI is wxDigit / wxPython based. 
@see: http://wxpython.org for details on wxPython

This module can start the application. It is checking for the call of the __main__ function and
will in case of start create a simple Python application and initialise and start the ImageGenerator
afterwards.

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)
"""
import ImageGeneratorWizard
import ProgressDialog
import Runtime
import wx
import thread

class WizardCallback:
    """
    Callback for events created by the wiard.
    
    @ivar _generator: Reference to the Generator Instance.
    @type _generator: L{ImageGenerator}
    """
    def __init__(self, generator):
        """
        Initialises the callback instance. 
        
        A reference to the given instance of a generator is saved in a private variable
        for later use.
        
        @param generator: Generator instance this callback has been instantiated with.
        @type generator: L{ImageGenerator}
        """
        self._generator = generator
        
    def cancelled(self):
        """
        Callback function to be invoked by the wizard in case of user abortion on
        the wizard.
        
        Forwards the call to the corresponding function in the generator instance. 
        (L{ImageGenerator.abortProcessing})
        """
        self._generator.abortProcessing()
        
    def finished(self, core, settings):
        """
        Callback function to be invoked by the wizard in case of finishing the imaging
        process. (both ways, sucessful or unsucessful finishing.)
        
        Invokes the corresponding function in the generator instance. 
        (L{ImageGenerator.startProcessing})
        """
##        print core.getImplementationName()
##        print settings.getPathDD()
##        print settings.getSource()
##        print settings.getDestination()
        self._generator.startProcessing(core, settings)

class ImagingCallback:
    """
    Default Implementation for the callbacks created by the ImageGenerator itself. 
    
    For each event (sucess, error or cancel) a very basic output to standard out is
    created.
    
    These function must be overwritten with exactly the given signature if you want to
    register your own callback with your application.
    
    @ivar _generator: Reference to the Generator Instance.
    @type _generator: L{ImageGenerator}
    """
    def __init__(self, generator):
        """
        Initialises the callback instance. 
        
        A reference to the given instance of a generator is saved in a private variable
        for later use.
        
        @param generator: Generator instance this callback has been instantiated with.
        @type generator: L{ImageGenerator}
        """
        self._generator = generator
        
    def success(self, destinationfilename):
        """
        To be called by the generator in case of finishing a generation sucessfully.
        
        Prints "Imaging sucessful" to standard out.
        """
        print "Imaging sucessful"
        
    def error(self, msg = None):
        """
        To be called by the generator in case of finishing a generation not sucessfully.
        
        Print "Error whilst Imaging" to standard out.
        """
        print "Error whilst Imaging: \n%s" %(msg)
        
    def cancelled(self):
        """
        To be called by the generator in case of abortion of the generation.
        
        Prints "Imaging aborted" to standard out.
        """
        print "Imaging aborted"
        
class ImageGenerator:
    """
    Heart of the gui for the ImageGenerator. 
    
    The gui is wizard based. This class handles the wizards and the callbacks created by the 
    wizard, which are kind of forwarded to a generator callback to be registered.
    
    No application is created within this class. (For example L{wx.PySimpleApp}) This has to 
    be performed outside before initialising the ImageGenerator.
    
    @ivar _callback: Reference to the registered Generator callback
    @type _callback: Any class with the interface exactly like L{ImagingCallback}
    @ivar _parentControl: The exPython parent control of the wizard
    @type _parentControl: L{wx.Control}
    """
    def __init__(self, callback = None, parentControl = None, baseDir = "."):
        """
        Initialises the image generator.
        
        Stores the values for the given parameters in the private instance variables. If callback
        is C{None} the L{ImagingCallback} is used as default.
        
        After initialising, use the function L{start} to bring up the wizard.
        
        @param callback: Generator callback to be informed about any of the events success, error or cancel
        @type callback: Any class with the interface exactly like L{ImagingCallback}
        @param parentControl: The exPython parent control of the wizard
        @type parentControl: L{wx.Control}
        """
        if callback == None:
            self._callback = ImagingCallback(self)
        else:
            self._callback = callback
        self._parentControl = parentControl
        
        self._baseDir = baseDir
        
    def start(self, parameters = {}):
        """
        Initialises the wizard and hands the control to it.
        
        The values for callback and parent control in the instance variables are passed to
        the constructor for the ImageGeneratorWizard. (L{ImageGeneratorWizard.__init__})
        
        Also takes care of showing and destroying the wizard instance.
        
        @param parameters: You can pass some parameters for default core and output directory.
        @type parameters: C{Dict}
        """
        wiz_callback = WizardCallback(self)
        wizard = ImageGeneratorWizard.ImageGeneratorWizard(wiz_callback, parent = self._parentControl, parameters = parameters, baseDir = self._baseDir)
        wizard.show()
        wizard.Destroy()
    
    def startProcessing(self, core, settings):
        """
        To be invoked by the wizard callback once the "start" button has been pressed.
        
        Creates a status instance (L{Runtime.Status}) for the generation. Afterwards, the
        core is started in its own thread. Finally, the progress dialog is brought up and
        the appropriate action corresponding to the information in the status object is
        performed; basically, either calling the error or the success function in the 
        generator callback.
        
        @param core: Core to be used for the imaging
        @type core: Any class with exactly the interface as L{GeneratorCoreAbstract.CoreInterface}
        @param settings: Settings instance to be used for this imaging
        @type settings: L{Runtime.Settings}
        """
        status = Runtime.Status()
        status.setStarted()
        thread.start_new_thread(core.createImage,(status,))
        progress = ProgressDialog.ProgressDialog(parent = self._parentControl, settings = settings, status = status)
        if self._callback != None:
            if status.getError() != None:
                self._callback.error(status.getError())
            elif status.isFinished():
                self._callback.success(settings.getDestination())
    
    def abortProcessing(self):
        """
        To be invoked by the wizard callback once the "cancel" button has been pressed.
        
        The call is passed to the generator callback function for cancel.
        """
        if self._callback != None:
            self._callback.cancelled()
            
if __name__ == "__main__":        
    app = wx.PySimpleApp(0)
    gen = ImageGenerator()
    gen.start()
