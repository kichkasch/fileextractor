#!/usr/bin/env python
"""
Graphical interface for the FileExtractor. Contains the MainFrame and a simple Application for
starting up the FileExtractor GUI Frontend.

The GUI is wxDigit / wxPython based. 
@see: http://wxpython.org for details on wxPython

This module can start the application. It is checking for the call of the __main__ function and
will in case of start the simple Application.


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

import sys
import os
import os.path


try:
#    from wxPython.wx import * - compatibility issue
    from wxPython.wx import *
    import wxPython.html
    from wxPython.htmlhelp import *
except ImportError:
    print "\nIMPORT ERROR"
    print "The site package for wxPython could not be imported."
    print "You must install wxPython before running the FileExtractor!"
    print"\nCheck 'http://wxpython.org' for information on wxPython and 'http://wxpython.org/download.php#binaries'" 
    print "for downloading binary versions."
    print "\nYou may also check the project home page's install page 'http://kkfileextractor.sourceforge.net/installation.htm' " \
    "for more information."
    raw_input("\nPress enter to abort")
    sys.exit(-1)
    
import FESettings
import FileExtractorCore
import signatures
import ProgressDialog
from ExecutionSettings import ExecutionSettings

_MODULE_IMAGE_GENERATOR = 0

try:
    from imagegenerator import ImageGenerator
    print "Module Imagegenerator initialised."
    _MODULE_IMAGE_GENERATOR = 1
except ImportError:
    print "Module Imagegenerator not available."

_ID_ADD = 101
_ID_START = 102
_ID_OPTIONS = 103
_ID_EXIT  = 104
_ID_IMAGEGENERATOR = 105
_ID_CONTENT = 201
_ID_ABOUT = 202
_ID_B_ADD = 301
_ID_B_REMOVE = 302
_ID_B_INFO = 303
_ID_B_DIR = 304
_ID_B_START = 305

_helpFile_arch = "fileextractorhelp.zip"

class FileExtractorFrame(wxFrame):
    """ 
    MainFrame for the FileExtractor GUI FrontEnd
    
    Responsible for the MainFrame of the application, containing all the panels, a menubar and
    also the Event Handling. Further classes from the modules ProgressDialog and ResultDialog
    are required for displaying dialogs during runtime.
    """
    
    def __init__(self, parent, ID, title):
        """
        Instantiate a FileExtractorFrame.
    
        A wxFrame will be created with the size L{wxSize}(600,400). The position
        is default position, indicated by the keyword wxDefaultPosition. The events for the
        buttons and menu items are registered as well.
        
        After execution of this constructor your application should initialise the help dialog using 'L{initHelp}()'
        and display the frame 'frame.Show()' / 'app.SetTopWindow(frame). When using the provided application class 
        (L{FileExtractorSimpleApp}), these steps are done by the module.

        Keyword arguments:
        @param parent: The parent window (passed to super class constructor L{wxPython.wx.wxFrame.__init__})
        @type parent: L{wxPython.wx.wxFrame}
        @param ID: The id of the wxControl (passed to super class constructor L{wxPython.wx.wxFrame.__init__})
        @type ID: C{int}
        @param title: The title of the frame (passed to super class constructor L{wxPython.wx.wxFrame.__init__})
        @type title: C{String}
        """
#        self._baseDir = os.path.abspath(os.path.dirname(sys.argv[0]))                #os.getcwd() 
        self._baseDir = FESettings.BASEDIR
        
        import wx
        wx.InitAllImageHandlers()
        
        # load settings
        from FESettings import getSettings
        getSettings().load()

        wxFrame.__init__(self, parent, ID, title,
                         wxDefaultPosition, wxSize(600, 500))
        
        from FESettings import getSettings
        if getSettings().getValue('output_dir'):
            self.dest_folder = getSettings().getValue('output_dir')
        else:
            self.dest_folder = "./"
        
        self.CreateStatusBar()
        self.SetStatusText("FileExtractor initialised ...")
        
        appLogo = wx.Icon(os.path.join(self._baseDir, "icons/fileextractor.png"), wx.BITMAP_TYPE_PNG);
        self.SetIcon(appLogo)
        
        panel_outer = wxPanel(self, -1)
        
        panel_left = wxPanel(panel_outer, -1)
        panel_right = wxPanel(panel_outer, -1)

        label_sources = wxStaticText (panel_left, -1 , "Source File(s)")

        self.filelist = wxListBox(panel_left, -1, style = wxLC_REPORT|wxSUNKEN_BORDER)
        self.content = []
        self.filelist.Set(self.content)
        
        panel_buttons = wxPanel(panel_left, -1)
        #b1 = wxButton(panel_buttons, _ID_B_ADD, "Add")
        #b2 = wxButton(panel_buttons, _ID_B_REMOVE, "Remove")

        panel_fill = wxPanel(panel_buttons, -1)
        bmAdd = wx.Bitmap(os.path.join(self._baseDir, "icons/edit_add.png"), wx.BITMAP_TYPE_PNG);
        b1 = wxBitmapButton(panel_buttons, _ID_B_ADD, bmAdd, size=(30,25))
        bmRem = wx.Bitmap(os.path.join(self._baseDir, "icons/edit_remove.png"), wx.BITMAP_TYPE_PNG);
        b2 = wxBitmapButton(panel_buttons, _ID_B_REMOVE, bmRem, size=(30,25))

        box = wxBoxSizer(wxHORIZONTAL)
        box.Add(panel_fill, 1, wxALIGN_CENTER | wxEXPAND)
        box.Add(b1, 1, wxALIGN_CENTER )
        box.Add(b2, 1, wxALIGN_CENTER )
        panel_buttons.SetAutoLayout(True)
        panel_buttons.SetSizer(box)
        panel_buttons.Layout()
        
        
        
        bmLogo = wx.Bitmap(os.path.join(self._baseDir, "icons/felogo2.png"), wx.BITMAP_TYPE_PNG);
        sbmLogo = wxStaticBitmap(panel_left, 567, bmLogo, size = (250, 140))
        
        panel_fill = wxPanel(panel_left, -1)

        #panel_fill1 = wxPanel(panel_left, -1)
        
        box = wxBoxSizer(wxVERTICAL)
        box.Add(label_sources, 1, wxALIGN_CENTER_VERTICAL | wxALIGN_CENTER_HORIZONTAL)
        box.Add(self.filelist, 6, wxEXPAND)
        box.Add(panel_buttons, 2, wxEXPAND ) #| wxALIGN_CENTER_VERTICAL)
        box.Add(panel_fill, 1, wxEXPAND)
        box.Add(sbmLogo, 8, wxALIGN_CENTER_VERTICAL | wxALIGN_CENTER_HORIZONTAL)

        panel_left.SetAutoLayout(True)
        panel_left.SetSizer(box)
        panel_left.Layout()

        # and now the right panel
        label_signatures = wxStaticText (panel_right, -1 , "Select File Types")

        self.signaturelist = wxCheckListBox(panel_right, -1, style = wxLC_REPORT|wxSUNKEN_BORDER)
        thesignatures = FileExtractorCore.getAvailableSignatures()
        self.sigDict = {}
        for sig in thesignatures:
            name = sig[signatures.name]
            self.sigDict[name] = sig
        self.sigcontent = self.sigDict.keys()
        self.signaturelist.Set(self.sigcontent)
##        for i in range(0, len(self.sigcontent)):
##            self.signaturelist.Check(i)
        
        st = getSettings().getValue('signatues_off')
        d  = {}
        if st:
            for x in st.split('|'):
                d[x.strip()] = x.strip()
        for i in range(0, len(self.sigcontent)):
            if d.has_key(self.signaturelist.GetString(i)):
                self.signaturelist.Check(i, false)
            else:
                self.signaturelist.Check(i)
        
            
        
        bmInfo = wx.Bitmap(os.path.join(self._baseDir, "icons/info.png"), wx.BITMAP_TYPE_PNG);
        bInfo = wxBitmapButton(panel_right, _ID_B_INFO, bmInfo, size=(60,20))
        
        
        #bInfo = wxButton(panel_right, _ID_B_INFO, "Info")
        
        
        label_outputdir = wxStaticText (panel_right, -1, "Output Directory")
        panel_dir = wxPanel(panel_right, -1)
        if getSettings().getValue('output_dir'):
            self.if_dir = wxTextCtrl(panel_dir, -1, getSettings().getValue('output_dir'))
        else:
            self.if_dir = wxTextCtrl(panel_dir, -1, 'Working Directory')
        self.if_dir.SetEditable(false)
        #bChooseDir = wxButton(panel_dir, _ID_B_DIR, "Change Directory")        
        
        bmDir = wx.Bitmap(os.path.join(self._baseDir, "icons/browse.png"), wx.BITMAP_TYPE_PNG);
        panel_fill = wxPanel(panel_dir, -1)
        bChooseDir = wxBitmapButton(panel_dir, _ID_B_DIR, bmDir, size=(30,30))        

        box = wxBoxSizer(wxHORIZONTAL)
        box.Add(self.if_dir, 16, wxALIGN_CENTER)
        box.Add(panel_fill, 1, wxALIGN_CENTER)
        box.Add(bChooseDir, 3, wxALIGN_CENTER)
        panel_dir.SetAutoLayout(True)
        panel_dir.SetSizer(box)
        panel_dir.Layout()
        
        
##        pFill1 = wxPanel(panel_right, -1)
        pFill2 = wxPanel(panel_right, -1)
        pFill3 = wxPanel(panel_right, -1)

        panel_start = wxPanel(panel_right, -1)
        panel_fills1 = wxPanel(panel_start, -1)
##        panel_fills2 = wxPanel(panel_start, -1)

        bmStart = wx.Bitmap(os.path.join(self._baseDir, "icons/start4.png"), wx.BITMAP_TYPE_PNG);
        bStartSearch  = wxBitmapButton(panel_start, _ID_B_START, bmStart, size=(105,22))

        #bStartSearch = wxButton(panel_start, _ID_B_START, "Start Search")
        boxs = wxBoxSizer(wxHORIZONTAL)
        boxs.Add(panel_fills1, 7, wxEXPAND)
        boxs.Add(bStartSearch, 7, wxEXPAND | wxALIGN_RIGHT)
##        boxs.Add(panel_fills2, 1, wxEXPAND)
        panel_start.SetAutoLayout(True)
        panel_start.SetSizer(boxs)
        panel_start.Layout()
        
        boxr = wxBoxSizer(wxVERTICAL)
        boxr.Add(label_signatures, 1, wxALIGN_CENTER_VERTICAL | wxALIGN_CENTER_HORIZONTAL)
        boxr.Add(self.signaturelist, 10, wxEXPAND)
##        boxr.Add(pFill1, 1, wxEXPAND)
        boxr.Add(bInfo, 2, wxALIGN_CENTER_VERTICAL | wxALIGN_RIGHT)
        boxr.Add(pFill2, 1, wxEXPAND)
        boxr.Add(label_outputdir, 1, wxALIGN_BOTTOM| wxALIGN_CENTER_HORIZONTAL)
        boxr.Add(panel_dir, 2, wxEXPAND | wxALIGN_CENTER_VERTICAL | wxALIGN_LEFT)
        boxr.Add(pFill3, 1, wxEXPAND)
        boxr.Add(panel_start, 2, wxEXPAND)

        panel_right.SetAutoLayout(True)
        panel_right.SetSizer(boxr)
        panel_right.Layout()


        
        # layout for outer window

        panel_fill_hor1 = wxPanel(panel_outer, -1)
        panel_fill_hor2 = wxPanel(panel_outer, -1)
        panel_fill_hor3 = wxPanel(panel_outer, -1)
        box = wxBoxSizer(wxHORIZONTAL)
        box.Add(panel_fill_hor1, 1, wxEXPAND)
        box.Add(panel_left, 10, wxEXPAND)
        box.Add(panel_fill_hor2, 1, wxEXPAND)
        box.Add(panel_right, 10, wxEXPAND)
        box.Add(panel_fill_hor3, 1, wxEXPAND)

        panel_outer.SetAutoLayout(True)
        panel_outer.SetSizer(box)
        panel_outer.Layout()

        pFill1 = wxPanel(self, -1)
        pFill2 = wxPanel(self, -1)
##        pFill3 = wxPanel(self, -1)
        boxo = wxBoxSizer(wxVERTICAL)
        boxo.Add(pFill1, 1, wxEXPAND)
        boxo.Add(panel_outer, 20, wxEXPAND)
        boxo.Add(pFill2, 1, wxEXPAND)
##        boxo.Add(panel_start, 1, wxEXPAND)
##        boxo.Add(pFill3, 1, wxEXPAND)


        self.SetAutoLayout(True)
        self.SetSizer(boxo)
        self.Layout()

        
        fileMenu = wx.Menu()
        addItem = wx.MenuItem(fileMenu, _ID_ADD, "&Add Source File",
                    "Add Source File to be searched in")
        bm = wx.Bitmap(os.path.join(self._baseDir, "icons/small/edit_add.png"), wx.BITMAP_TYPE_PNG);
        addItem.SetBitmap(bm)
        fileMenu.AppendItem(addItem)
        startItem = wx.MenuItem(fileMenu, _ID_START, "&Start Searching",
                    "Go and find your files")
        bm = wx.Bitmap(os.path.join(self._baseDir, "icons/small/start.png"), wx.BITMAP_TYPE_PNG);
        startItem.SetBitmap(bm)
        fileMenu.AppendItem(startItem)
        fileMenu.AppendSeparator()
        prefItem = wx.MenuItem(fileMenu, _ID_OPTIONS, "&Options",
                    "Apply Settings for the program")
        bm = wx.Bitmap(os.path.join(self._baseDir, "icons/small/configure.png"), wx.BITMAP_TYPE_PNG);
        prefItem.SetBitmap(bm)
        fileMenu.AppendItem(prefItem)
        fileMenu.AppendSeparator()
        exitItem = wx.MenuItem(fileMenu, _ID_EXIT, "E&xit", "Terminate the program")
        bmExit = wx.Bitmap(os.path.join(self._baseDir, "icons/small/exit.png"), wx.BITMAP_TYPE_PNG);
        exitItem.SetBitmap(bmExit)
        fileMenu.AppendItem(exitItem)
        
        menuBar = wxMenuBar()
        menuBar.Append(fileMenu, "&File");
        
        toolsMenu = wxMenu()
        imageItem = wx.MenuItem(toolsMenu, _ID_IMAGEGENERATOR, "&ImageGenerator...",
                    "Create an image file")
        bm = wx.Bitmap(os.path.join(self._baseDir, "icons/small/tools_image.png"), wx.BITMAP_TYPE_PNG);
        imageItem.SetBitmap(bm)
        toolsMenu.AppendItem(imageItem)
        menuBar.Append(toolsMenu, "&Tools")
        
        helpMenu = wxMenu()
        helpItem = wx.MenuItem(helpMenu, _ID_CONTENT, "&Content",
                    "How to use this Program in detail")
        bm = wx.Bitmap(os.path.join(self._baseDir, "icons/small/help.png"), wx.BITMAP_TYPE_PNG);
        helpItem.SetBitmap(bm)
        helpMenu.AppendItem(helpItem)
        helpMenu.AppendSeparator()
        aboutItem = wx.MenuItem(helpMenu, _ID_ABOUT, "&About",
                    "Basic Information about this program")
        bm = wx.Bitmap(os.path.join(self._baseDir, "icons/small/info.png"), wx.BITMAP_TYPE_PNG);
        aboutItem.SetBitmap(bm)
        helpMenu.AppendItem(aboutItem)
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)

        EVT_MENU(self, _ID_ABOUT, self._OnAbout)
        EVT_MENU(self, _ID_EXIT,  self._TimeToQuit)
        EVT_MENU(self, _ID_ADD,  self._AddSourceFile)
        EVT_MENU(self, _ID_START,  self._StartSearch)
        EVT_MENU(self, _ID_CONTENT,  self._showHelp)
        EVT_MENU(self, _ID_OPTIONS,  self._OnSettings)
        if _MODULE_IMAGE_GENERATOR:
            EVT_MENU(self, _ID_IMAGEGENERATOR, self._startImageGenerator)
        else:
            EVT_MENU(self, _ID_IMAGEGENERATOR,  self._NotAvailable)
            
        EVT_BUTTON(self, _ID_B_ADD, self._AddSourceFile)
        EVT_BUTTON(self, _ID_B_REMOVE, self._RemoveSourceFile)
        EVT_BUTTON(self, _ID_B_INFO, self._InfoSignature)
        EVT_BUTTON(self, _ID_B_DIR, self._ChangeOutputDir)
        EVT_BUTTON(self, _ID_B_START, self._StartSearch)
        
        #
        # toolbar
        #
##        import wx
##        wx.InitAllImageHandlers()
        #toolbar = self.CreateToolBar(style = wxNO_BORDER | wxTB_HORIZONTAL)
        toolbar = self.CreateToolBar(style = wxRAISED_BORDER | wxTB_TEXT | wxTB_HORIZONTAL)
        self.ToolBar = toolbar
        toolbar.SetToolBitmapSize((21,21))
        # 1. global
        bmExit = wx.Bitmap(os.path.join(self._baseDir, "icons/exit.png"), wx.BITMAP_TYPE_PNG);
        toolbar.DoAddTool(id = 1001, bitmap = bmExit, label="Exit", shortHelp = "Quit FileExtractor")
        toolbar.AddSeparator()
        # 2. Actions
        bmAdd = wx.Bitmap(os.path.join(self._baseDir, "icons/edit_add.png"), wx.BITMAP_TYPE_PNG);
        toolbar.DoAddTool(id = 1002, bitmap = bmAdd, label="Add", shortHelp = "Add Source File")
        bmRem = wx.Bitmap(os.path.join(self._baseDir, "icons/edit_remove.png"), wx.BITMAP_TYPE_PNG);
        toolbar.DoAddTool(id = 1003, bitmap = bmRem, label="Remove", shortHelp = "Remove Source File")
        bmStart = wx.Bitmap(os.path.join(self._baseDir, "icons/start.png"), wx.BITMAP_TYPE_PNG);
        toolbar.DoAddTool(id = 1004, bitmap = bmStart, label="Start", shortHelp = "Start recovery")
        toolbar.AddSeparator()
        # 3. Tools
        bmImage = wx.Bitmap(os.path.join(self._baseDir, "icons/tools_image.png"), wx.BITMAP_TYPE_PNG);
        toolbar.DoAddTool(id = 1005, bitmap = bmImage, label="Image", shortHelp = "Image your data source")
        toolbar.AddSeparator()
        # 4. Configure
        bmConf = wx.Bitmap(os.path.join(self._baseDir, "icons/configure.png"), wx.BITMAP_TYPE_PNG);
        toolbar.DoAddTool(id = 1006, bitmap = bmConf, label="Configure", shortHelp = "Configure FileExtractor")
        toolbar.AddSeparator()
        # 5. Help
        bmHelp = wx.Bitmap(os.path.join(self._baseDir, "icons/help.png"), wx.BITMAP_TYPE_PNG);
        toolbar.DoAddTool(id = 1007, bitmap = bmHelp, label="Help", shortHelp = "FileExtractor Help")
        toolbar.AddSeparator()

        toolbar.Realize()
        
        EVT_TOOL(self, 1001, self._TimeToQuit)
        EVT_TOOL(self, 1002, self._AddSourceFile)
        EVT_TOOL(self, 1003, self._RemoveSourceFile)
        EVT_TOOL(self, 1004, self._StartSearch)
        if _MODULE_IMAGE_GENERATOR:
            EVT_TOOL(self, 1005, self._startImageGenerator)
        else:
            EVT_TOOL(self, 1005, self._NotAvailable)        
        EVT_TOOL(self, 1006, self._OnSettings)
        EVT_TOOL(self, 1007, self._showHelp)

    def _OnSettings(self, event):
        import SettingsDialog
        dia  = SettingsDialog.SettingsDialog(self, -1, "FileExtractor Configuration", self._baseDir)
        dia.ShowModal()
        dia.Destroy()        

    def _OnAbout(self, event):
        dlg = wxMessageDialog(self, "%s - Version %s\n"
                              "Searching for Files within binary sources\n"
                              "\nAuthor: %s\n"
                              "Email: %s\n\n"
                              "%s"
                              "\n\nPublished under the General Public License (GPL)   " %(FESettings.PROGRAM_NAME, FESettings.VERSION, FESettings.AUTHOR, FESettings.EMAIL, FESettings.URL),
                              "About Me", wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def _TimeToQuit(self, event):
        self.Close(true)
    
    def _UnderConstruction(self, event):
        dlg = wxMessageDialog(self, "Under Construction\n",
                              "Coming soon", wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
    def _NotAvailable(self, event):
        dlg = wxMessageDialog(self, "The requested module was not found on this system.\n" \
                                    " Check your installation.",
                              "Not installed", wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
    def _AddSourceFile(self, event):
        fileDialog = wxFileDialog(self, "Choose a source File", style = wxOPEN)
        if fileDialog.ShowModal() == wxID_OK:
            name = fileDialog.GetPath()
            self.content.append(name)
            self.filelist.Set(self.content)
        fileDialog.Destroy()
    
    def _RemoveSourceFile(self, event):
        selection = self.filelist.GetSelection()
        if selection < 0:
            dlg = wxMessageDialog(self, "Please select exactly one item\n"
                                "to be removed from the list.",
                              "Select file from list", wxOK | wxICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            del self.content[selection]
            self.filelist.Set(self.content)
    
    def _StartSearch(self, event):
        sourceFiles = self.content
        if len(sourceFiles) < 1:
            dlg = wxMessageDialog(self, "No source file specified.\n\n"
                                "Please provide at least one file in the\n"
                                "list of source files.",
                                "No source file", wxOK | wxICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        dis_sigs = []
        for i in range(0, len(self.sigcontent)):
            if not self.signaturelist.IsChecked(i):
                dis_sigs.append(self.sigcontent[i])
        from FESettings import getSettings
        if getSettings().getValue('naming_digits') and getSettings().getValue('naming_digits'): # they only come together
            digits = int(getSettings().getValue('naming_digits'))
            start = int(getSettings().getValue('naming_start') )
            settings = ExecutionSettings(disabled_signatures = dis_sigs, sourceFiles = sourceFiles, dest_folder=self.dest_folder,
                    signatures = signatures.getCopyOfAllSignauteres(), output_level = 0, output_frequency=10000, digits = digits, 
                    counterstart = start)
        else:
            settings = ExecutionSettings(disabled_signatures = dis_sigs, sourceFiles = sourceFiles, dest_folder=self.dest_folder,
                    signatures = signatures.getCopyOfAllSignauteres(), output_level = 0, output_frequency=10000)
        progressDialog = ProgressDialog.ProgressDialog(self, -1, "Progress of Search",
                settings)

    def _InfoSignature(self, event):
        selection = self.signaturelist.GetSelection()
        if selection < 0:
            dlg = wxMessageDialog(self, "Please select exactly one item\n"
                                "from the signature list before requesting more information.",
                                "Select signature from list", wxOK | wxICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            cur_sig = self.sigDict[self.sigcontent[selection]]
            name = cur_sig[signatures.name]
            description = cur_sig[signatures.description]
            extension = cur_sig[signatures.extension]
            filesize_type = cur_sig[signatures.filesize_type]
            if filesize_type == signatures.TYPE_END_SEQUENCE:
                type_string = "File end identified by End Sequence"
            elif filesize_type == signatures.TYPE_FILE_SIZE:
                type_string = "File end identified by File Size information"
            elif filesize_type == signatures.TYPE_MANUAL:
                type_string = "File end identified by user specific function"
            dlg = wxMessageDialog(self, "Signature name: " + name + "\n"
                                "File Extension: " + extension + "\n\n" +
                                description + "\n" +
                                type_string,
                              "Signature Information", wxOK | wxICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            
    def _ChangeOutputDir(self, event):
        dirDialog = wxDirDialog(self, "Choose Output Directory")
        if dirDialog.ShowModal() == wxID_OK:
            path = dirDialog.GetPath()
            self.dest_folder = path
            self.if_dir.SetValue(path)
        dirDialog.Destroy()
    
    def _startImageGenerator(self, event):
        print "Starting module Image Generator..."
        parameters = {}
        from FESettings import getSettings
        if getSettings().getValue('ig_default_core'):
            parameters['default_core'] = getSettings().getValue('ig_default_core')
        if getSettings().getValue('ig_output_dir') and getSettings().getValue('ig_output_filename'):
            parameters['output_dir'] = os.path.join(getSettings().getValue('ig_output_dir'), getSettings().getValue('ig_output_filename'))
        imageGenerator = ImageGenerator.ImageGenerator(callback = self, parentControl = self, baseDir = self._baseDir)
        imageGenerator.start(parameters = parameters)
        
    def _showHelp(self, event):
        global helpFile
        self._showIt()
    
    def initHelp(self):
        """
        Initalises the help dialog
        
        The help dialog has to be initialised before the MainFrame is shown; the 
        displaying of the help dialog is managed by the application itself.
        
        The zip handler will be invoked, a new help controller will be created
        and the help zipfile (helpbook) (as specified in the private
        variable L{_helpFile_arch}) is added to this help control.
        """
        wxFileSystem_AddHandler(wxZipFSHandler())
        # Create the viewer
        self.helpctrl = wxHtmlHelpController(wxHF_TOOLBAR | wxHF_CONTENTS | wxHF_INDEX | wxHF_PRINT | wxHF_BOOKMARKS)
        # and add the books
        global _helpFile_arch
        self.helpctrl.AddBook(os.path.join(self._baseDir,_helpFile_arch), 1)
    
    def _showIt(self):
        # start it up!
        self.helpctrl.DisplayContents()

        
    #################################################################################
    ### stuff for image generator callback
    def cancelled(self):
        pass
        
    def success(self, destname):
        dlg = wxMessageDialog(self, "The image file was created sucessfully" \
                                "\n(name: " + destname + ")" \
                                "\n\nAdd the image file to the source list?",
                              "Imaging finished", wxYES_NO | wxICON_QUESTION)
        if dlg.ShowModal() == wxID_YES:
            self.content.append(destname)
            self.filelist.Set(self.content)
        dlg.Destroy()
        
    def error(self, msg):
        dlg = wxMessageDialog(self, "The image file could not be created\n\n"
                                "Low level Error Message:\n%s" %(msg),
                              "Imaging error", wxOK | wxICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        
    ### end stuff image generator callback
    #################################################################################
    
class FileExtractorSimpleApp(wxApp):
    """
    Simple Application for initialising and displaying the MainFrame.
    
    """
    def OnInit(self):
        """
        Initialiser
        
        This function should be called by the constructor of the superclass L{wxPython.wx.wxApp}
        
        Creates a frame object of type FileExtractorFrame and initialises its help (L{FileExtractorFrame.initHelp}). 
        Finally, this frame is displayed and marked as the top window of this
        application.
        
        @return: Indicates, whether the application was invoked successfully.
        @rtype: Bool
        """
        frame = FileExtractorFrame(NULL, -1, "%s - Version %s" %(FESettings.PROGRAM_NAME, FESettings.VERSION))
        frame.initHelp()
        frame.Show(true)
        self.SetTopWindow(frame)
        return true

if __name__ == "__main__":        
    app = FileExtractorSimpleApp(0)
    app.MainLoop()
