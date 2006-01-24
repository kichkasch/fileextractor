"""
Dialog for configuring FileExtractor and its modules

The GUI is wxDigit / wxPython based. 
@see: http://wxpython.org for details on wxPython

Changes here are written through to the L{FESettings} module. After hitting the OK button,
the save function in there will be invoked as well to make the settings persistent.

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)
"""

from wxPython.wx import *
import wx

DIR_CURRENT_ST = 'Working directory'

class SettingsDialog(wxDialog):
    """
    Holding all the information about the dialog.
    """
    
    def __init__(self, parent, ID, title):
        """
        Initialises all controls and registers the event listeners.
        """
        wxDialog.__init__(self, parent, ID, title, size=(600,400))

        outerBox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(panel, -1)
        panel_content = wx.Panel(panel, -1)        
        
        font_headings = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        panel_top = wx.Panel(self, -1)
        label = wxStaticText (panel_top, -1 , "Configure FileExtractor", style = wx.ALIGN_CENTRE )
        label.SetFont(font_headings)
        panel_fill1 = wx.Panel(panel_top, -1)
        panel_fill2 = wx.Panel(panel_top, -1)
        topBox = wx.BoxSizer(wx.HORIZONTAL)
        topBox.Add(panel_fill1, 4, wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL)
        topBox.Add(label, 5, wx.ALIGN_CENTER)
        topBox.Add(panel_fill2, 4, wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL)
        panel_top.SetSizer(topBox)

        
        self.tree = wx.TreeCtrl(panel1, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS | wxDOUBLE_BORDER)
        root = self.tree.AddRoot('Settings')
        fe = self.tree.AppendItem(root, 'FileExtractor')
        mod = self.tree.AppendItem(root, 'Modules')
        self.tree.Expand(fe)

        self.tree.AppendItem(fe, 'General')
        self.tree.AppendItem(fe, 'FileTypes')
        self.tree.AppendItem(fe, 'Output Files')

        self.tree.AppendItem(mod, 'ImageGenerator')
        
        vbox.Add(self.tree, 1, wx.EXPAND)
        panel1.SetSizer(vbox)
        
        
        panel_fill_h1 = wx.Panel(panel, -1)
##        panel_fill_h1.SetBackgroundColour(wx.RED)
        panel_fill_h2 = wx.Panel(panel, -1)
##        panel_fill_h2.SetBackgroundColour(wx.RED)
        panel_fill_h3 = wx.Panel(panel, -1)
##        panel_fill_h3.SetBackgroundColour(wx.RED)
        hbox.Add(panel_fill_h1, 1, wx.EXPAND)
        hbox.Add(panel1, 5, wx.EXPAND)
        hbox.Add(panel_fill_h2, 1, wx.EXPAND)
        hbox.Add(panel_content, 10, wx.EXPAND)
        hbox.Add(panel_fill_h3, 1, wx.EXPAND)
        panel.SetSizer(hbox)


        panel_buttons = wx.Panel(self, -1)
        panel_fill = wx.Panel(panel_buttons, -1)
##        panel_fill.SetBackgroundColour(wx.RED)
        bmApply = wx.Bitmap("icons/apply.png", wx.BITMAP_TYPE_PNG);
        b1 = wx.BitmapButton(panel_buttons, 601, bmApply, size=(30,25))
        bmCancel = wx.Bitmap("icons/cancel.png", wx.BITMAP_TYPE_PNG);
        b2 = wx.BitmapButton(panel_buttons, 602, bmCancel, size=(30,25))
        panel_fill1 = wx.Panel(panel_buttons, -1)
##        panel_fill1.SetBackgroundColour(wx.RED)
        box = wx.BoxSizer(wxHORIZONTAL)
        box.Add(panel_fill, 8, wxEXPAND)
##        panel_fill.SetBackgroundColour(wx.RED)
        box.Add(b2, 2, wxALIGN_CENTER )
        box.Add(b1, 2, wxALIGN_CENTER )
        box.Add(panel_fill1, 1,  wxEXPAND)
        panel_buttons.SetAutoLayout(True)
        panel_buttons.SetSizer(box)
        panel_buttons.Layout()

        
        #
        # Content area
        #
        self._lastChild = None
        self._topName = None
        self._imageGenerator = None
        self._general = None
        self._fileTypes = None
        self.content_swap_box =  wx.BoxSizer(wxVERTICAL)
        self.contentHeading = wx.TextCtrl(panel_content, -1, "Please choose an option from the tree", style = wxTE_MULTILINE | wxTE_READONLY | wxNO_BORDER )
        
        panel_fill = wx.Panel(panel_content, -1)        
##        panel_fill.SetBackgroundColour(wx.RED)
        self.panel_swap = wx.Panel(panel_content, -1)
        self.panel_swap.SetSizer(self.content_swap_box)
        
        contentBox = wx.BoxSizer(wxVERTICAL)
        contentBox.Add(self.contentHeading, 2, wxALIGN_CENTER | wxEXPAND)
        contentBox.Add(panel_fill, 1, wxEXPAND)
        contentBox.Add(self.panel_swap, 8, wxEXPAND)
        panel_content.SetAutoLayout(True)
        panel_content.SetSizer(contentBox)
        panel_content.Layout()
        
        
        panel_fill0 = wx.Panel(self, -1)
##        panel_fill0.SetBackgroundColour(wx.RED)
        panel_fill1 = wx.Panel(self, -1)
##        panel_fill1.SetBackgroundColour(wx.RED)
        panel_fill2 = wx.Panel(self, -1)
##        panel_fill2.SetBackgroundColour(wx.RED)
        panel_fill3 = wx.Panel(self, -1)
##        panel_fill3.SetBackgroundColour(wx.RED)
        
        outerBox.Add(panel_fill0, 1, wx.EXPAND)
        outerBox.Add(panel_top, 2,  wx.EXPAND )
        outerBox.Add(panel_fill1, 1, wx.EXPAND)
        outerBox.Add(panel, 15, wx.EXPAND)
        outerBox.Add(panel_fill2, 1, wx.EXPAND)
        outerBox.Add(panel_buttons, 2, wx.EXPAND)
        outerBox.Add(panel_fill3, 1, wx.EXPAND)
        self.SetSizer(outerBox) 
        self.Centre()
        self.CentreOnParent()
        
        st = wx.StaticText(self.panel_swap, -1, "Content:\n* FileExtractor\n   - General\n   - File Types\n   - Naming of output files\n* Modules\n   - ImageGenerator")
        self.content_swap_box.Add(st, 1, wx.ALIGN_TOP, wx.ALIGN_CENTER_HORIZONTAL)
        self._lastChild = st
        
        
        EVT_BUTTON(self, 602, self._OnExit)
        EVT_BUTTON(self, 601, self._OnApply)
        
        wx.EVT_TREE_SEL_CHANGED(self.tree, 1, self._OnSelChanged)

    def _OnApply(self, event):
        from FESettings import getSettings
        try:
            val = self.if_dir.GetValue()
            if val != DIR_CURRENT_ST:
                getSettings().setValue('output_dir', val)
        except AttributeError, msg:
            pass
            
        try:
            val = ''
            for x in range(0, self.signaturelist.GetCount()):
                name = self.signaturelist.GetString(x)
                if not self.signaturelist.IsChecked(x):
                    val += " %s |" %(name)
            getSettings().setValue('signatues_off', val)
        except AttributeError, msg:
            pass

        try:
            val = self.if_dir_img.GetValue()
            if val != DIR_CURRENT_ST:
                getSettings().setValue('ig_output_dir', val)
        except AttributeError, msg:
            pass
            
        try:
            val = self._chCore.GetStringSelection()
            getSettings().setValue('ig_default_core', val)
        except AttributeError, msg:
            pass
            
        try:
            val = self.spinDigits.GetValue()
            getSettings().setValue('naming_digits', val)
        except AttributeError, msg:
            pass

        try:
            val = self.spinStart .GetValue()
            getSettings().setValue('naming_start', val)
        except AttributeError, msg:
            pass

        getSettings().save()
        dlg = wxMessageDialog(self, "Your settings have been saved.",
                          "Save Setting Confirmation", wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

        self.EndModal(0)
        self.Destroy()
        
    def _OnSelChanged(self, event):
##        self._save()
        item =  event.GetItem()
##        print "Selected now: ", self.tree.GetItemText(item)
        if self._lastChild:
            self.content_swap_box.Remove(self._lastChild)
            self._lastChild.Show(0)
        
        if self.tree.GetItemText(item) == "ImageGenerator":
            import FileExtractor
            if FileExtractor._MODULE_IMAGE_GENERATOR:
                self.contentHeading.SetValue("Apply the settings for the module 'ImageGenerator' here.")
                self._putImageGeneratorOptionsContent()
            else:
                dlg = wx.MessageDialog(self, "The requested module was not found on this system.\n" \
                                            " Check your installation.",
                                      "Not installed", wxOK | wxICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            
        elif self.tree.GetItemText(item) == "Modules":
            self.contentHeading.SetValue("Apply settings for FE modules.\nChoose a module from the tree.")
            st = wx.StaticText(self.panel_swap, -1, "Available modules:\n - ImageGenerator")
            self.content_swap_box.Add(st, 1, wx.ALIGN_TOP, wx.ALIGN_CENTER_HORIZONTAL)
            self._lastChild = st
            
        elif self.tree.GetItemText(item) == "FileExtractor":
            self.contentHeading.SetValue("Settings for the FileExtractor.\nChoose a sub category from the tree.")
            st = wx.StaticText(self.panel_swap, -1, "Available options:\n - General\n - File Types\n - Naming rules for output files")
            self.content_swap_box.Add(st, 1, wx.ALIGN_TOP, wx.ALIGN_CENTER_HORIZONTAL)
            self._lastChild = st

        elif self.tree.GetItemText(item) == "General":
            self.contentHeading.SetValue("Specify general options for the FileExtractor.")
            self._putGeneralOptionsContent()
        elif self.tree.GetItemText(item) == "FileTypes":
            self.contentHeading.SetValue("Specify default behaviour for file types.")
            self._putFiletypeOptionsContent()
        elif self.tree.GetItemText(item) == "Output Files":
            self.contentHeading.SetValue("Define the way your recovered files shall be named.")
            self._putFilenameOptionsContent()
            
        self.content_swap_box.Layout()
            
##    def _save(self):
##        if self._topName == 'image':
##            self._imageGenerator = []
##            self._imageGenerator.append()
##        self._topName = None
            
    def _putGeneralOptionsContent(self):
        panel_top = wx.Panel(self.panel_swap, -1)
        label_outputdir = wxStaticText (panel_top, -1, "Output Directory")
        panel_dir = wxPanel(panel_top, -1)
        try:
            self.if_dir.Reparent(panel_dir)
        except AttributeError, msg:
            from FESettings import getSettings
            if getSettings().getValue('output_dir'):
                self.if_dir = wxTextCtrl(panel_dir, -1, getSettings().getValue('output_dir'))
            else:
                self.if_dir = wxTextCtrl(panel_dir, -1, DIR_CURRENT_ST)
            self.if_dir.SetEditable(false)
        
        bmDir = wx.Bitmap("icons/browse.png", wx.BITMAP_TYPE_PNG);
        panel_fill = wxPanel(panel_dir, -1)
##        panel_fill.SetBackgroundColour(wx.RED)
        bChooseDir = wxBitmapButton(panel_dir, 701, bmDir, size=(25,25))        

        box = wxBoxSizer(wxHORIZONTAL)
        box.Add(self.if_dir, 16, wxALIGN_CENTER)
        box.Add(panel_fill, 1, wx.EXPAND)
        box.Add(bChooseDir, 3, wxALIGN_CENTER)
        panel_dir.SetAutoLayout(True)
        panel_dir.SetSizer(box)
        panel_dir.Layout()
            
        panel_fill = wx.Panel(panel_top, -1)
##        panel_fill.SetBackgroundColour(wx.RED)
        topBox = wxBoxSizer(wxVERTICAL)
        topBox.Add(label_outputdir, 1, wx.EXPAND)
        topBox.Add(panel_dir, 1, wx.EXPAND | wx.TOP)
        topBox.Add(panel_fill, 4, wx.EXPAND)
        panel_top.SetAutoLayout(True)
        panel_top.SetSizer(topBox)
        panel_top.Layout()
        self.content_swap_box.Add(panel_top, 1, wx.EXPAND)
        
        EVT_BUTTON(self, 701, self._ChangeFEOutputDir)
        self._lastChild = panel_top
        
    def _ChangeFEOutputDir(self, event):
        dirDialog = wxDirDialog(self, "Choose Output Directory")
        if dirDialog.ShowModal() == wxID_OK:
            path = dirDialog.GetPath()
            self.dest_folder = path
            self.if_dir.SetValue(path)
        dirDialog.Destroy()

    def _putImageGeneratorOptionsContent(self):
        panel_top = wx.Panel(self.panel_swap, -1)

        lCore = wx.StaticText(panel_top, -1, "Choose default core")
##        choicesCore = CoreManager.getInstance().getListOfCoreNames()
        import imagegenerator
        choicesCore = imagegenerator.CoreManager.getInstance().getListOfCoreNames()
##        choicesCore = ['Win32 dd clone', 'Linux / Unix']
        from FESettings import getSettings
        try:
            self._chCore.Reparent(panel_top)
        except AttributeError, msg:
            self._chCore = wx.Choice(panel_top, 721, choices = choicesCore)
            self._chCore.SetSelection(0)
            if getSettings().getValue('ig_default_core'):
                for i in range(len(choicesCore)):
                    if choicesCore[i] == getSettings().getValue('ig_default_core'):
                        self._chCore.SetSelection(i)

        label_outputdir = wxStaticText (panel_top, -1, "Directory  for image")
        panel_dir = wxPanel(panel_top, -1)
        try:
            self.if_dir_img.Reparent(panel_dir)
        except AttributeError, msg:
            if getSettings().getValue('ig_output_dir'):
                self.if_dir_img = wxTextCtrl(panel_dir, -1, getSettings().getValue('ig_output_dir'))
            else:
                self.if_dir_img = wxTextCtrl(panel_dir, -1, DIR_CURRENT_ST)
            self.if_dir_img.SetEditable(false)
        
        bmDir = wx.Bitmap("icons/browse.png", wx.BITMAP_TYPE_PNG);
        panel_fill = wxPanel(panel_dir, -1)
##        panel_fill.SetBackgroundColour(wx.RED)
        bChooseDir = wxBitmapButton(panel_dir, 722, bmDir, size=(25,25))        

        box = wxBoxSizer(wxHORIZONTAL)
        box.Add(self.if_dir_img, 16, wxALIGN_CENTER)
        box.Add(panel_fill, 1, wx.EXPAND)
        box.Add(bChooseDir, 3, wxALIGN_CENTER)
        panel_dir.SetAutoLayout(True)
        panel_dir.SetSizer(box)
        panel_dir.Layout()
            
        panel_fill0 = wx.Panel(panel_top, -1)
##        panel_fill0.SetBackgroundColour(wx.RED)
        panel_fill = wx.Panel(panel_top, -1)
##        panel_fill.SetBackgroundColour(wx.RED)
        topBox = wxBoxSizer(wxVERTICAL)
        topBox.Add(lCore,1, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        topBox.Add(self._chCore, 1, wx.EXPAND, wx.TOP)
        topBox.Add(panel_fill0, 1, wx.EXPAND)
        topBox.Add(label_outputdir, 1, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        topBox.Add(panel_dir, 1, wx.EXPAND, wx.TOP)
        topBox.Add(panel_fill, 1, wx.EXPAND)
        panel_top.SetAutoLayout(True)
        panel_top.SetSizer(topBox)
        panel_top.Layout()
        self.content_swap_box.Add(panel_top, 1, wx.EXPAND)

        EVT_BUTTON(self, 722, self._ChangeIGOutputDir)        
        self._lastChild = panel_top

    def _ChangeIGOutputDir(self, event):
        dirDialog = wxDirDialog(self, "Choose Output Directory")
        if dirDialog.ShowModal() == wxID_OK:
            path = dirDialog.GetPath()
            self.dest_folder = path
            self.if_dir_img.SetValue(path)
        dirDialog.Destroy()        
        
    def _putFiletypeOptionsContent(self):
        from FESettings import getSettings
        import FileExtractorCore
        import signatures
        panel_top = wx.Panel(self.panel_swap, -1)

        label_signatures = wxStaticText (panel_top, -1 , "Select file types enabled by default")
        try:
            self.signaturelist.Reparent(panel_top)
        except AttributeError, msg:
            self.signaturelist = wxCheckListBox(panel_top, -1, style = wxLC_REPORT|wxSUNKEN_BORDER)
            thesignatures = FileExtractorCore.getAvailableSignatures()
            self.sigDict = {}
            for sig in thesignatures:
                name = sig[signatures.name]
                self.sigDict[name] = sig
            self.sigcontent = self.sigDict.keys()
            self.signaturelist.Set(self.sigcontent)
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
        
##        panel_fill = wx.Panel(panel_top, -1)
        topBox = wxBoxSizer(wxVERTICAL)
        topBox.Add(label_signatures,1, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        topBox.Add(self.signaturelist, 5, wx.EXPAND, wx.TOP)
##        topBox.Add(panel_fill, 1, wx.EXPAND)
        panel_top.SetAutoLayout(True)
        panel_top.SetSizer(topBox)
        panel_top.Layout()
        self.content_swap_box.Add(panel_top, 1, wx.EXPAND)
        
        self._lastChild = panel_top
        
    def _putFilenameOptionsContent(self):
        from FESettings import getSettings
        panel_top = wx.Panel(self.panel_swap, -1)
        lDigits = wxStaticText (panel_top, -1 , "Number of numeric digits in the filename")
        if getSettings().getValue('naming_digits'):
            initial = int(getSettings().getValue('naming_digits'))
        else:
            initial = 5
        self.spinDigits = wx.SpinCtrl (panel_top, 801, str(initial), min = 1, max=100, initial = initial)
        
        lStart = wxStaticText (panel_top, -1 , "Number to start with")
        if getSettings().getValue('naming_start'):
            start = int(getSettings().getValue('naming_start'))
        else:
            start = 0
        self.spinStart = wx.SpinCtrl (panel_top, 802, str(start), min = 0, max=10000, initial = start)

        self.nameExample = wx.TextCtrl(panel_top, -1, "Example: ", style = wx.TE_READONLY )
        self.nameExample.Enable(0)
        self.nameExample.SetBackgroundColour(self.GetBackgroundColour())
        self._updateNameExample()
        
        panel_fill0 = wx.Panel(panel_top, -1)
##        panel_fill0.SetBackgroundColour(wx.RED)
        panel_fill = wx.Panel(panel_top, -1)
##        panel_fill.SetBackgroundColour(wx.RED)
        topBox = wxBoxSizer(wxVERTICAL)
        topBox.Add(lDigits,1, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        topBox.Add(self.spinDigits, 1, wx.EXPAND, wx.TOP)
        topBox.Add(panel_fill0, 1, wx.EXPAND)
        topBox.Add(lStart, 1, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        topBox.Add(self.spinStart, 1, wx.EXPAND, wx.TOP)
        topBox.Add(panel_fill, 1, wx.EXPAND)
        topBox.Add(self.nameExample, 1, wx.EXPAND)
        panel_top.SetAutoLayout(True)
        panel_top.SetSizer(topBox)
        panel_top.Layout()
        self.content_swap_box.Add(panel_top, 1, wx.EXPAND)

        EVT_SPINCTRL(self, 801, self._updateNameExample)
        EVT_SPINCTRL(self, 802, self._updateNameExample)
        self._lastChild = panel_top
        
    def _updateNameExample(self, event = None):
        digits = int (self.spinDigits.GetValue())
        first = int ( self.spinStart.GetValue())
        st = "0" * (digits - len(str(first))) + str (first)
        self.nameExample.SetValue("Example: JPEG_%s.jpg" %(st))
        
    def _OnExit(self, event):
        self.EndModal(0)
        self.Destroy()
