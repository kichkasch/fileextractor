#
# Settings for FileExtractor
#

from wxPython.wx import *
import wx

class SettingsDialog(wxDialog):
    def __init__(self, parent, ID, title):
        wxDialog.__init__(self, parent, ID, title, size=(600,400))

        outerBox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(panel, -1)
        panel_content = wx.Panel(panel, -1)        
        
        font_headings = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        panel_top = wx.Panel(self, -1)
        label = wxStaticText (panel_top, -1 , "Configure FileExtractor")
        label.SetFont(font_headings)
        topBox = wx.BoxSizer(wx.HORIZONTAL)
        topBox.Add(label, 1, wx.CENTER)

        
        self.tree = wx.TreeCtrl(panel1, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        root = self.tree.AddRoot('Settings')
        fe = self.tree.AppendItem(root, 'FileExtractor')
        mod = self.tree.AppendItem(root, 'Modules')
        self.tree.Expand(fe)

        gen = self.tree.AppendItem(fe, 'General')
        self.tree.AppendItem(fe, 'FileTypes')

        self.tree.AppendItem(mod, 'ImageGenerator')
        
        vbox.Add(self.tree, 1, wx.EXPAND)
        panel1.SetSizer(vbox)
        
        
        panel_fill_h1 = wx.Panel(panel, -1)
        panel_fill_h2 = wx.Panel(panel, -1)
        panel_fill_h3 = wx.Panel(panel, -1)
        hbox.Add(panel_fill_h1, 1, wx.CENTER)
        hbox.Add(panel1, 5, wx.EXPAND)
        hbox.Add(panel_fill_h2, 1, wx.EXPAND)
        hbox.Add(panel_content, 10, wx.EXPAND)
        hbox.Add(panel_fill_h3, 1, wx.EXPAND)
        panel.SetSizer(hbox)


        panel_buttons = wx.Panel(self, -1)
        panel_fill = wx.Panel(panel_buttons, -1)
        bmApply = wx.Bitmap("icons/apply.png", wx.BITMAP_TYPE_PNG);
        b1 = wx.BitmapButton(panel_buttons, 601, bmApply, size=(30,25))
        bmCancel = wx.Bitmap("icons/cancel.png", wx.BITMAP_TYPE_PNG);
        b2 = wx.BitmapButton(panel_buttons, 602, bmCancel, size=(30,25))
        panel_fill1 = wx.Panel(panel_buttons, -1)
        box = wx.BoxSizer(wxHORIZONTAL)
        box.Add(panel_fill, 8, wxALIGN_CENTER | wxEXPAND)
        box.Add(b2, 2, wxALIGN_CENTER )
        box.Add(b1, 2, wxALIGN_CENTER )
        box.Add(panel_fill1, 1, wxALIGN_CENTER | wxEXPAND)
        panel_buttons.SetAutoLayout(True)
        panel_buttons.SetSizer(box)
        panel_buttons.Layout()

        
        #
        # Content area
        #
        self._lastChild = None
        self.content_swap_box =  wx.BoxSizer(wxVERTICAL)
        self.contentHeading = wx.TextCtrl(panel_content, -1, "Please choose an option from the tree", style = wxTE_MULTILINE | wxTE_READONLY | wxNO_BORDER )
        
        panel_fill = wx.Panel(panel_content, -1)        
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
        panel_fill1 = wx.Panel(self, -1)
        panel_fill2 = wx.Panel(self, -1)
        panel_fill3 = wx.Panel(self, -1)
        
        outerBox.Add(panel_fill0, 1, wx.EXPAND)
        outerBox.Add(panel_top, 2, wx.CENTER)
        outerBox.Add(panel_fill1, 1, wx.EXPAND)
        outerBox.Add(panel, 15, wx.EXPAND)
        outerBox.Add(panel_fill2, 1, wx.EXPAND)
        outerBox.Add(panel_buttons, 2, wx.EXPAND)
        outerBox.Add(panel_fill3, 1, wx.EXPAND)
        self.SetSizer(outerBox) 
        self.Centre()
        self.CentreOnParent()
        
        EVT_BUTTON(self, 602, self._OnExit)

        wx.EVT_TREE_SEL_CHANGED(self.tree, 1, self._OnSelChanged)
        
    def _OnSelChanged(self, event):
        item =  event.GetItem()
##        print "Selected now: ", self.tree.GetItemText(item)
        if self._lastChild:
            self.content_swap_box.Remove(self._lastChild)
            self._lastChild.Show(0)
        
        if self.tree.GetItemText(item) == "ImageGenerator":
            self.contentHeading.SetValue("Apply the settings for the module 'ImageGenerator' here.")
            self._putImageGeneratorOptionsContent()
        elif self.tree.GetItemText(item) == "Modules":
            self.contentHeading.SetValue("Apply settings for FE modules.\nChoose a module from the tree.")
            st = wx.StaticText(self.panel_swap, -1, "Available modules:\n - ImageGenerator")
            self.content_swap_box.Add(st, 1, wx.ALIGN_TOP, wx.ALIGN_CENTER_HORIZONTAL)
            self._lastChild = st
            
        elif self.tree.GetItemText(item) == "FileExtractor":
            self.contentHeading.SetValue("Settings for the FileExtractor.\nChoose a sub category from the tree.")
            st = wx.StaticText(self.panel_swap, -1, "Available options:\n - General\n - File Types")
            self.content_swap_box.Add(st, 1, wx.ALIGN_TOP, wx.ALIGN_CENTER_HORIZONTAL)
            self._lastChild = st

        elif self.tree.GetItemText(item) == "General":
            self.contentHeading.SetValue("Specify general options for the FileExtractor.")
            self._putGeneralOptionsContent()
        elif self.tree.GetItemText(item) == "FileTypes":
            self.contentHeading.SetValue("Specify default behaviour for file types.")
        self.content_swap_box.Layout()
            
    def _putGeneralOptionsContent(self):
        panel_top = wx.Panel(self.panel_swap, -1)
        label_outputdir = wxStaticText (panel_top, -1, "Output Directory")
        panel_dir = wxPanel(panel_top, -1)
        self.if_dir = wxTextCtrl(panel_dir, -1, "Working Directory")
        self.if_dir.SetEditable(false)
        
        bmDir = wx.Bitmap("icons/browse.png", wx.BITMAP_TYPE_PNG);
        panel_fill = wxPanel(panel_dir, -1)
        bChooseDir = wxBitmapButton(panel_dir, 701, bmDir, size=(25,25))        

        box = wxBoxSizer(wxHORIZONTAL)
        box.Add(self.if_dir, 16, wxALIGN_CENTER)
        box.Add(panel_fill, 1, wxALIGN_CENTER)
        box.Add(bChooseDir, 3, wxALIGN_CENTER)
        panel_dir.SetAutoLayout(True)
        panel_dir.SetSizer(box)
        panel_dir.Layout()
            
        panel_fill = wx.Panel(panel_top, -1)
        topBox = wxBoxSizer(wxVERTICAL)
        topBox.Add(label_outputdir, 1, wx.ALIGN_BOTTOM,)
        topBox.Add(panel_dir, 1, wx.EXPAND, wx.TOP)
        topBox.Add(panel_fill, 4, wx.EXPAND)
        panel_top.SetAutoLayout(True)
        panel_top.SetSizer(topBox)
        panel_top.Layout()
        self.content_swap_box.Add(panel_top, 1, wx.EXPAND)
        
        self._lastChild = panel_top

    def _putImageGeneratorOptionsContent(self):
        panel_top = wx.Panel(self.panel_swap, -1)

        lCore = wx.StaticText(panel_top, -1, "Choose default core")
##        choicesCore = CoreManager.getInstance().getListOfCoreNames()
        choicesCore = ['Win32 dd clone', 'Linux / Unix']
        self._chCore = wx.Choice(panel_top, 721, choices = choicesCore)
        self._chCore.SetSelection(0)

        label_outputdir = wxStaticText (panel_top, -1, "Directory  for image")
        panel_dir = wxPanel(panel_top, -1)
        self.if_dir = wxTextCtrl(panel_dir, -1, "Working Directory")
        self.if_dir.SetEditable(false)
        
        bmDir = wx.Bitmap("icons/browse.png", wx.BITMAP_TYPE_PNG);
        panel_fill = wxPanel(panel_dir, -1)
        bChooseDir = wxBitmapButton(panel_dir, 722, bmDir, size=(25,25))        

        box = wxBoxSizer(wxHORIZONTAL)
        box.Add(self.if_dir, 16, wxALIGN_CENTER)
        box.Add(panel_fill, 1, wxALIGN_CENTER)
        box.Add(bChooseDir, 3, wxALIGN_CENTER)
        panel_dir.SetAutoLayout(True)
        panel_dir.SetSizer(box)
        panel_dir.Layout()
            
        panel_fill0 = wx.Panel(panel_top, -1)
        panel_fill = wx.Panel(panel_top, -1)
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
        
        self._lastChild = panel_top

        
    def _OnExit(self, event):
        self.EndModal(0)
        self.Destroy()
