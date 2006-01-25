"""
Wizard for the graphical interface for the ImageGenerator. 

Two pages are part of this wizard, the first one for choosing a core for the
generation (available core are received from the L{CoreManager}) and the location
of the dd command. On the second page of the wizard the location for the device
to image and the output file have to be defined.

A class L{GeneratorWizardPage} is utelised in order to provide a common layout for
the different wizard pages.

The GUI is wxDigit / wxPython based. 
@see: http://wxpython.org for details on wxPython

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)

@var DEF_TITLE: Default title for the ImageGenerator Wizard title bar
@type DEF_TITLE: C{String}
@var DEBUG_FILENAME: Name of the file to buffer output of the dd command.
@type DEBUG_FILENAME: C{String}
@var _ID_WIZARD: ID for wxpython event handling.
@type _ID_WIZARD: C{int}
@var _ID_BROWSE_DD: ID for wxpython event handling.
@type _ID_BROWSE_DD: C{int}
@var _ID_BROWSE_DEST: ID for wxpython event handling.
@type _ID_BROWSE_DEST: C{int}
@var _ID_INFO_SOURCES: ID for wxpython event handling.
@type _ID_INFO_SOURCES: C{int}
@var _ID_CH_CORES: ID for wxpython event handling.
@type _ID_CH_CORES: C{int}
"""
import CoreManager
import Runtime
import wx
from wx.wizard import *

DEF_TITLE = "ImageGenerator"
DEBUG_FILENAME = "./fileextractordebug.txt"
_ID_WIZARD = 101
_ID_BROWSE_DD = 201
_ID_BROWSE_DEST = 202
_ID_INFO_SOURCES = 203
_ID_CH_CORES = 204

class GeneratorWizardPage(WizardPageSimple):
    """
    Common layout for generator wizard pages.
    
    All wizard pages used for the image generator wizard should be instances of this
    class rather then of L{WizardPageSimple} or the like.
    
    The layout is organised and the values for the title and the message are displayed. The area
    to be used for content in the wizard page may be accessed using the function
    L{getContentPane}.
    
    @ivar _title: Title of the page (not the wizard). This one is displayed inside the window area.
    @type _title: c{String}
    @ivar _message: Message to be displayed underneath the title. Should be a help, which data 
    should be provided by the user here.
    @type _message: c{String}
    """
    def __init__(self, parent, prev=None, next=None, title = "Image Generator", message = "Apply your settings"):
        """
        Initialises the wizard page.
        
        The super constructor is called. Values for title and message are stored in private instance
        variables. Layouts and so on are managed and the controls are initialised and placed properly.
        
        @param parent: Parent control of this wizard page.
        @type parent: L{ImageGeneratorWizard}
        @param prev: Previous page of this page in wizard order. None, if the first one. Passed to the 
        initialiser of the super class L{wx.wizard.WizardPageSimple.__init__}
        @type prev: L{GeneratorWizardPage}
        @param next: Next page of this page in wizard order. None, if the last one. Passed to the 
        initialiser of the super class L{wx.wizard.WizardPageSimple.__init__}
        @type next: L{GeneratorWizardPage}
        @param title: Title of the wizard page.
        @type title: C{String}
        @param message: Help text for the wizard page.
        @type message: C{String}
        """
        WizardPageSimple.__init__(self, parent, prev, next)
        
        self._title = title
        self._message = message
        
        font_headings = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        panel_outer = wx.Panel(self, -1)

        label_title = wx.StaticText(panel_outer, -1, self._title)
        label_title.SetFont(font_headings)
##        label_message = wx.StaticText(panel_outer, -1, self._message)
        label_message = wx.TextCtrl(panel_outer, -1, self._message, size= (300,60), style = wx.TE_MULTILINE | wx.TE_READONLY | wx.NO_BORDER)
        label_message.Enable(0)
        self._panel_content = wx.Panel(panel_outer, -1)
        
        panel_fill_hor2 = wx.Panel(panel_outer, -1)
        panel_fill_hor3 = wx.Panel(panel_outer, -1)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(label_title, 2, wx.ALIGN_CENTER )
        box.Add(label_message, 4, wx.EXPAND)
        box.Add(panel_fill_hor2, 1, wx.EXPAND)
        box.Add(self._panel_content, 12, wx.EXPAND)
        box.Add(panel_fill_hor3, 1, wx.EXPAND)

        panel_outer.SetAutoLayout(True)
        panel_outer.SetSizer(box)
        panel_outer.Layout()

        pFill1 = wx.Panel(self, -1)
        pFill2 = wx.Panel(self, -1)
        boxo = wx.BoxSizer(wx.VERTICAL)
        boxo.Add(pFill1, 1, wx.EXPAND)
        boxo.Add(panel_outer, 20, wx.EXPAND)
        boxo.Add(pFill2, 1, wx.EXPAND)


        self.SetAutoLayout(True)
        self.SetSizer(boxo)
        self.Layout()
                        
    def getContentPane(self):
        """
        Returns the area of the wizard page, which is supposed to be filled with content.
        
        The panel is not configured with any layout manager.
        
        @return: Area in the wizard page to put controls on.
        @rtype: L{wx.Panel}
        """
        return self._panel_content

class ImageGeneratorWizard(Wizard):
    """
    Wizard for the ImageGenerator.
    
    Initialises and maintains the wizard pages and registers and responds to all 
    required events.
    
    @ivar _core: Currently chosen core for this generation
    @type _core: L{GeneratorCoreAbstract.CoreInterface}
    @ivar _callback: Callback for the events cancel and finish
    @type _callback: Any class overwriting the functions C{cancelled} and C{finished}
    @ivar _devicesDict: Dictionary for resovling human readable device entries into 
    proper device names
    @type _devicesDict: C{Dictionary}: Key is C{String} and Value is C{String}
    @ivar _page1: First wizard page
    @type _page1: L{GeneratorWizardPage}
    @ivar _page2: Second wizard page
    @type _page2: L{GeneratorWizardPage}
    """
    def __init__(self, callback = None, parent = None, title = DEF_TITLE, parameters = {}):
        """
        Initialises the wizard instance.
        
        The constructor of the super class (wx.wizard.Wizard.__init__) is called and
        the given parameters are stored in instance variables. The content for the 
        two wizard pages is initialised and they are put in order. Finally, the events
        are registered with the corrosponding functions.
        
        A dictionary is initialised, which resolves human readable entries for the
        devices into the proper device names. Both the human readable version and the
        real device names may be received from the core.
        
        @param callback: Callback instance for the events cancel and finish.
        @type callback: Any class overwriting the functions C{cancelled} and C{finished}
        @param parent: Parent control for the wizard. Passed to the super constructor.
        @type parent: L{wx.Control}
        @param title: Title for the title bar of the wizard window. Passed to the super constructor.
        @type title: C{String}
        @param parameters: You can pass some parameters for default core and output directory.
        @type parameters: C{Dict}
        """
        Wizard.__init__(self, parent, _ID_WIZARD, title)
        
        self._core = None
        self._callback = callback
        self._devicesDict = {}
        
        self._page1 = GeneratorWizardPage(self, title = "Core details", 
            message = "Please choose the generator core and check the settings " \
            "for the location of the dd command.")
        
        self._page2 = GeneratorWizardPage(self, self._page1, title = "Location details",
            message = "Choose your source (file or device) from the list or specify your " \
                "own device location in the input field. Also choose the location for " \
                "the output image file.")
        self._page1.SetNext(self._page2)
        
        import wx
        wx.InitAllImageHandlers()

        self._fillPageOne(parameters)
        self._fillPageTwo(parameters)
        
        self.SetPageSize((400,400))
        
        self._evtCoreSeclect(None)

        
        EVT_WIZARD_PAGE_CHANGED(self, _ID_WIZARD, self._evtPageChanged)
        EVT_WIZARD_CANCEL(self, _ID_WIZARD, self._evtCancel)
        EVT_WIZARD_FINISHED(self, _ID_WIZARD, self._evtFinished)
        wx.EVT_CHOICE(self, _ID_CH_CORES, self._evtCoreSeclect)
        wx.EVT_BUTTON(self, _ID_BROWSE_DD, self._evtBrowseDD)
        wx.EVT_BUTTON(self, _ID_BROWSE_DEST, self._evtBrowseDest) 
        wx.EVT_BUTTON(self, _ID_INFO_SOURCES, self._evtInfoSources)
    
    def _fillPageOne(self, parameters):
        """
        Putting the controls for the first wizard page.
        
        Controls for the core choice and the specifying of the location for
        the dd command are placed on the content pane of the first
        wizard page.
        """
        panel_outer = wx.Panel(self._page1.getContentPane(), -1)
        
        lCore = wx.StaticText(panel_outer, -1, "Choose Core")
        choicesCore = CoreManager.getInstance().getListOfCoreNames()
        self._chCore = wx.Choice(panel_outer, _ID_CH_CORES, choices = choicesCore)
        self._chCore.SetSelection(0)
        if parameters.has_key('default_core'):
            for i in range(len(choicesCore)):
                if choicesCore[i] == parameters['default_core']:
                    self._chCore.SetSelection(i)
        
##        import wx
        lLocDD = wx.StaticText(panel_outer, -1, "Specify Location of the dd-command")
##        self._tcLocDD = wx.TextCtrl(panel_outer, -1)
##        bBrowse = wx.Button(panel_outer, _ID_BROWSE_DD, "Browse")
        panel_dir = wx.Panel(panel_outer, -1)
        self._tcLocDD = wx.TextCtrl(panel_dir , -1)        
        bmDir = wx.Bitmap("icons/browse.png", wx.BITMAP_TYPE_PNG);
        panel_fill = wx.Panel(panel_dir, -1)
##        panel_fill.SetBackgroundColour(wx.RED)
        bBrowse = wx.BitmapButton(panel_dir, _ID_BROWSE_DD, bmDir, size=(25,25))        

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._tcLocDD, 16, wx.ALIGN_CENTER)
        box.Add(panel_fill, 1, wx.EXPAND)
        box.Add(bBrowse, 3, wx.ALIGN_CENTER)
        panel_dir.SetAutoLayout(True)
        panel_dir.SetSizer(box)
        panel_dir.Layout()

        
        panel_fill_hor2 = wx.Panel(panel_outer, -1)
        panel_fill_hor3 = wx.Panel(panel_outer, -1)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(lCore, 1, wx.EXPAND)
        box.Add(self._chCore, 1, wx.EXPAND)
        box.Add(panel_fill_hor2, 1, wx.EXPAND)
        box.Add(lLocDD, 1, wx.EXPAND)
        box.Add(panel_dir, 2, wx.EXPAND)
##        box.Add(self._tcLocDD, 2, wx.EXPAND)
##        box.Add(bBrowse, 2, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        box.Add(panel_fill_hor3, 2, wx.EXPAND)

        panel_outer.SetAutoLayout(True)
        panel_outer.SetSizer(box)
        panel_outer.Layout()

        boxo = wx.BoxSizer(wx.VERTICAL)
        boxo.Add(panel_outer, 20, wx.EXPAND)

        self._page1.getContentPane().SetAutoLayout(True)
        self._page1.getContentPane().SetSizer(boxo)
        self._page1.getContentPane().Layout()
        
    def _fillPageTwo(self, parameters):
        """
        Putting the controls for the second wizard page.
        
        Controls for the specifying of the source device and the location
        of the destination image file are placed on the content pane of the second
        wizard page.
        """
        import wx
        panel_outer = wx.Panel(self._page2.getContentPane(), -1)
        
        lSources = wx.StaticText(panel_outer, -1, "Choose or specify source")
        
        panel_info = wx.Panel(panel_outer, -1)
        choicesSources = []
        self._cbSources = wx.ComboBox(panel_info, -1, choices = choicesSources)

        bmDir = wx.Bitmap("icons/info.png", wx.BITMAP_TYPE_PNG);
        panel_fill = wx.Panel(panel_info, -1)
##        panel_fill.SetBackgroundColour(wx.RED)
        bInfoSources = wx.BitmapButton(panel_info, _ID_INFO_SOURCES, bmDir, size=(25,25))        

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._cbSources, 16, wx.ALIGN_CENTER)
        box.Add(panel_fill, 1, wx.EXPAND)
        box.Add(bInfoSources, 3, wx.ALIGN_CENTER)
        panel_info.SetAutoLayout(True)
        panel_info.SetSizer(box)
        panel_info.Layout()

##        bInfoSources = wx.Button(panel_outer, _ID_INFO_SOURCES, "Info")

        lLocDest = wx.StaticText(panel_outer, -1, "Specify Location of output image file")
        panel_dir = wx.Panel(panel_outer, -1)
        self._tcLocDest = wx.TextCtrl(panel_dir, -1)
        if parameters.has_key('output_dir'):
            self._tcLocDest.SetValue(parameters['output_dir'])

        bmDir = wx.Bitmap("icons/browse.png", wx.BITMAP_TYPE_PNG);
        panel_fill = wx.Panel(panel_dir, -1)
##        panel_fill.SetBackgroundColour(wx.RED)
        bBrowseDest = wx.BitmapButton(panel_dir, _ID_BROWSE_DEST, bmDir, size=(25,25))        

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._tcLocDest, 16, wx.ALIGN_CENTER)
        box.Add(panel_fill, 1, wx.EXPAND)
        box.Add(bBrowseDest, 3, wx.ALIGN_CENTER)
        panel_dir.SetAutoLayout(True)
        panel_dir.SetSizer(box)
        panel_dir.Layout()
            
##        bBrowseDest = wx.Button(panel_outer, _ID_BROWSE_DEST, "Browse")
        
        panel_fill_hor2 = wx.Panel(panel_outer, -1)
        panel_fill_hor3 = wx.Panel(panel_outer, -1) 
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(lSources, 1, wx.EXPAND)
        box.Add(panel_info, 2, wx.EXPAND)
##        box.Add(self._cbSources, 2, wx.EXPAND)
##        box.Add(bInfoSources, 2, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        box.Add(panel_fill_hor2, 1, wx.EXPAND)
        box.Add(lLocDest, 1, wx.EXPAND)
        box.Add(panel_dir, 2, wx.EXPAND)
##        box.Add(self._tcLocDest, 2, wx.EXPAND)
##        box.Add(bBrowseDest, 2, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        box.Add(panel_fill_hor3, 2, wx.EXPAND)

        panel_outer.SetAutoLayout(True)
        panel_outer.SetSizer(box)
        panel_outer.Layout()

        boxo = wx.BoxSizer(wx.VERTICAL)
        boxo.Add(panel_outer, 20, wx.EXPAND)

        self._page2.getContentPane().SetAutoLayout(True)
        self._page2.getContentPane().SetSizer(boxo)
        self._page2.getContentPane().Layout()
        pass
        
    def _processSourcesList(self):
        """
        Renews the entries in the sources list of wizard page two.
        
        Initialises the core with the name as provided in the choice for core
        and tries to get information about source suggestions from this core. If
        successful, these suggestions are put into the combo box for sources.
        
        Also brings the values in the dictionary for the resolving of device
        names (L{_devicesDict}) up to date.
        """
        corename = self._chCore.GetStringSelection()
        ddloc = self._tcLocDD.GetValue()
        self._devicesDict = {}
        self._core  = self._initCore(corename, ddloc = ddloc)
        suggestions, devices = self._core.getPossibleSources()
        self._cbSources.Clear()
        i = 0
        for sug in suggestions:
            self._cbSources.Append(sug, None)
            self._devicesDict[sug] = devices[i]
            i += 1
    
    def _initCore(self, corename, settings = None, ddloc = None):
        """
        Initialises a core from the core manager with the given name.
        
        If not provided, it assembles a settings class and attempts to instantiate
        a core with the given name. If not successful, the entire program execution
        is aborted.
        
        @param corename: Name of the core to be initialised
        @type corename: C{String}
        @param settings: Settings to be used for this core
        @type settings: L{Runtime.Settings}
        @param ddloc: Location of the dd command. Is only used if the settings instance is not provided
        @type ddloc: C{String}
        
        @return: Reference to the created core instance.
        @rtype: L{GeneratorCoreAbstract.CoreInterface}
        """
        manager = CoreManager.getInstance()
        redirectBuffer = DEBUG_FILENAME
        if settings == None:
            if ddloc == None:
                settings = Runtime.Settings(redirectOutput = redirectBuffer)
            else:
                settings = Runtime.Settings(redirectOutput = redirectBuffer, path_dd = ddloc)
        try:
            coreClass = manager.getCoreClass(corename)
        except KeyError:
            print "\nRequested core not found. Program abortion.\n"
            sys.exit(-1)
        return coreClass(settings)
    
    def show(self):
        """
        Brings the wizard finally up.
        
        To be called after the constructor. Brings up the wizard with the first
        page. 
        """
        self.RunWizard(self._page1)
        
    def _evtPageChanged(self, evt):
        """
        Event handler function called when user changed pages.
        
        The sources list is recreated whenever page two has become the new page. This is
        performed by passing the request to the private function L{_processSourcesList}.
        
        @param evt: Event instance
        """
        if self.GetCurrentPage() == self._page2:
            self._processSourcesList()

    def _evtCancel(self, evt):
        """
        Event handler function called when user cancels the wizard.
        
        If a callback is available, its function for cancel is invoked.
        
        @param evt: Event instance
        """
        if self._callback != None:
            self._callback.cancelled()
        
    def _evtFinished(self, evt):
        """
        Event handler function called when user pushs finish on the last wizard page.
        
        Only if there is a callback available, all the information from both pages is gathered 
        and put into a new settings (L{Runtime.Settings}) instance. A core is instantiated and
        the values for settings and core are passed to the callback using its function for
        finish.
        
        @param evt: Event instance
        """
        if self._callback != None:
            location_dd = self._tcLocDD.GetValue()
            sourceTmp = self._cbSources.GetValue()
##            sourceTmp = self._cbSources.GetStringSelection()
            if self._devicesDict.has_key(sourceTmp):
                source = self._devicesDict[sourceTmp]
            else:
                source = sourceTmp
            location_dest = self._tcLocDest.GetValue()
            redirectBuffer = DEBUG_FILENAME
            settings = Runtime.Settings(path_dd = location_dd, source = source, 
                destination = location_dest, redirectOutput = redirectBuffer)
            corename = self._chCore.GetStringSelection()
            core = self._initCore(corename, settings)
            self._callback.finished(core, settings)

    def _evtCoreSeclect(self, evt):
        """
        Event handler function called when a new core was selected.

        The core with the name selected is attempted to be instantiated and its default location
        for the dd command is being collected. This value is afterwards put in the text input 
        control for the location of the dd command on wizard page one.
        
        @param evt: Event instance
        """
        corename = self._chCore.GetStringSelection()
        core  = self._initCore(corename)
        def_ddloc = core.getDefaultDDLocation()
        self._tcLocDD.SetValue(def_ddloc)
        
    def _evtBrowseDD(self, evt):
        """
        Event handler function called when the button for browse for the dd command location was pressed.
        
        Opens a file dialog (open modus) and eventuelly (depending on the user action) puts the chosen value
        into the text input field for the dd command.
        
        @param evt: Event instance
        """
        currentValue = self._tcLocDD.GetValue()
        try:
            tmp = currentValue.rindex("/")
            dir = currentValue[0:tmp]
        except ValueError:
            dir = ""
        
        fileDialog = wx.FileDialog(self, "Specify location for the dd command", 
                defaultFile = currentValue, defaultDir = dir, style = wx.OPEN | wx.CHANGE_DIR)
        if fileDialog.ShowModal() == wx.ID_OK:
            newValue = fileDialog.GetPath()
            self._tcLocDD.SetValue(newValue)

    def _evtBrowseDest(self, evt):
        """
        Event handler function called when the button for browse for the destination image file was pressed.
        
        Opens a file dialog (save modus) and eventuelly (depending on the user action) puts the chosen value
        into the text input field for the destination image file.
        
        @param evt: Event instance
        """
        currentValue = self._tcLocDest.GetValue()
        try:
            tmp = currentValue.rindex("/")
            dir = currentValue[0:tmp]
        except ValueError:
            dir = ""
        
        fileDialog = wx.FileDialog(self, "Specify location for destination image file", 
                defaultFile = currentValue, defaultDir = dir, style = wx.SAVE | wx.CHANGE_DIR)
        if fileDialog.ShowModal() == wx.ID_OK:
            newValue = fileDialog.GetPath()
            self._tcLocDest.SetValue(newValue)
    
    def _evtInfoSources(self, evt):
        """
        Event handler function called when the button "Info" next to the sources list is pressed.
        
        If a core has been instantiated, the information about the sources is received from it and
        displayed in a modal message box.
        
        @param evt: Event instance
        """
        if self._core != None:
            message = self._core.getSourceInfo()
            dialog = wx.MessageDialog(self, message, "What are these entries about...", wx.ICON_INFORMATION | wx.OK )
            dialog.ShowModal()
