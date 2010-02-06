"""
Provides one class for a result dialog for the FileExtractor GUI.

The GUI is wxDigit / wxPython based. 
@see: http://wxpython.org for details on wxPython

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
from wxPython.wx import *
from wxPython.grid import *
import tools
import signatures

_ID_B_OK = 301

class ResultDialog(wxDialog):
    """
    Result Dialog for the GUI Frontend of FileExtractor.
    
    This class provides a dialog for visualising the results of an entire execution over
    several source files. It extracts information from an status instance and puts the
    results into a table.
    """
    def __init__(self, parent, ID, title, status):
        """
        Initialises the result dialog.
        
        Creates a wxDialog (size L{wxSize(600,400)}) and fills the content. The events for
        the close button is registered with its private function.
       
        Finally, this dialog is centered on the parent window and displayed modally. Hence;
        the function L{ShowModal()} must not be invoked from the calling module.
        
        @param parent: Parent window for this wxDialog - passed to the superclass constructor (wxPython.wx.wxDialog.__init__)
        @type parent: L{wxPython.wx.wxFrame}
        @param ID: ID for this component - passed to the superclass constructor (wxPython.wx.wxDialog.__init__)
        @type ID: C{int}
        @param title: Title for the dialog - - passed to the superclass constructor (wxPython.wx.wxDialog.__init__)
        @type title: C{String}
        @param status: Status instance for the execution results shall be shown for
        @type status: L{ExecutionSettings.ExecutionStatus}
        """
        wxDialog.__init__(self, parent, ID, title,
                         wxDefaultPosition, wxSize(600, 400))
        
        settings = status.settings
        font_headings = wxFont(12, wxDEFAULT, wxNORMAL, wxBOLD)

        panel_outer = wxPanel(self, -1)

        label_results = wxStaticText (panel_outer, -1 , "Results")
        label_results.SetFont(font_headings)
        
        panel_content = wxPanel(panel_outer, -1)
        colour = panel_content.GetBackgroundColour()

        grid = wxGrid(panel_content, -1, wxDefaultPosition, wxSize(400,300), wxSIMPLE_BORDER)
        no_rows = len(settings.sourceFiles) + 2
        no_cols = len(settings.signatures) + 2
        grid.CreateGrid(no_rows,no_cols)
        font_bold = grid.GetDefaultCellFont()
        font_bold.SetWeight(wxBOLD)
        colour_grid = grid.GetDefaultCellTextColour()
        grid.SetDefaultCellBackgroundColour(colour)
        grid.EnableEditing(false)
        grid.SetRowLabelSize(0)
        grid.SetColLabelSize(0)
        grid.SetGridLineColour(colour_grid)
        i = 1
        for sourceFile in settings.sourceFiles:
            grid.SetCellValue(i,0, sourceFile)
            grid.SetCellAlignment(i, 0, wxALIGN_RIGHT, wxALIGN_CENTRE)
            i += 1
        grid.SetCellValue(no_rows-1,0, "After all")
        grid.SetCellAlignment(no_rows-1, 0, wxALIGN_RIGHT, wxALIGN_CENTRE)
        grid.SetCellFont(no_rows-1, 0, font_bold)
        
        j = 1
        for j1 in range(0, len(settings.signatures)):
            sig = settings.signatures[j1]
            grid.SetCellValue(0, j, sig[signatures.name])
            grid.SetCellAlignment(0, j, wxALIGN_CENTRE, wxALIGN_CENTRE)
            grid.SetColSize(j,50)
            j += 1
        grid.SetColSize(0,150)
        grid.SetColSize(no_cols-1,100)
        
        grid.SetCellValue(0, no_cols-1,"Time")
        grid.SetCellAlignment(0, no_cols-1, wxALIGN_CENTRE, wxALIGN_CENTRE)
        
        overall_time = 0
        k = 1
        for z in range(0, len(settings.sourceFiles)):
            name = settings.sourceFiles[z]
            res = status.result_eachfile[z]
            l = 1
            for l1 in range(0, len(settings.signatures)):
                sig = settings.signatures[l1]
                if res.has_key(sig[signatures.name]):
                    grid.SetCellValue(k, l, str(res[sig[signatures.name]]))
                else:
                    grid.SetCellValue(k, l, "0")
                grid.SetCellAlignment(k, l, wxALIGN_RIGHT, wxALIGN_CENTRE)
                l += 1
            overall_time += status.getRunTimeForNumber(z)
            timeL = tools.processTime(status.getRunTimeForNumber(z))
            grid.SetCellValue(k, no_cols-1, timeL[0] + ":" + timeL[1] + ":" + timeL[2])
            grid.SetCellAlignment(k, no_cols-1, wxALIGN_RIGHT, wxALIGN_CENTRE)
            k += 1
        timeL = tools.processTime(overall_time)
        grid.SetCellValue(no_rows-1, no_cols-1, timeL[0] + ":" + timeL[1] + ":" + timeL[2])
        grid.SetCellAlignment(no_rows-1, no_cols-1, wxALIGN_RIGHT, wxALIGN_CENTRE)
        grid.SetCellFont(no_rows-1, no_cols-1, font_bold)
        
        l = 1
        for l1 in range(0, len(settings.signatures)):
            sig = settings.signatures[l1]
            grid.SetCellValue(no_rows-1, l, str(status.counterr[sig[signatures.name]]))
            grid.SetCellAlignment(no_rows-1, l, wxALIGN_RIGHT, wxALIGN_CENTRE)
            grid.SetCellFont(no_rows-1, l, font_bold)
            l += 1
                    
        boxc = wxBoxSizer(wxVERTICAL)
        boxc.Add(grid,1, wxEXPAND)
        panel_content.SetAutoLayout(True)
        panel_content.SetSizer(boxc)
        panel_content.Layout()
        
        label_destfolder = wxStaticText(panel_outer, -1, "Find your output files in")
        if_dir = wxTextCtrl(panel_outer, -1, settings.dest_folder)
        if_dir.SetEditable(false)
        if_dir.Enable(false)
        
        self.bOKButton = wxButton(panel_outer, _ID_B_OK, "OK")
        
        pFill0 = wxPanel(panel_outer, -1)
        pFill1 = wxPanel(panel_outer, -1)
        pFill2 = wxPanel(panel_outer, -1)
        pFill3 = wxPanel(panel_outer, -1)
        pFill4 = wxPanel(panel_outer, -1)
        box = wxBoxSizer(wxVERTICAL)
        box.Add(pFill0, 1)
        box.Add(label_results, 2, wxALIGN_CENTER_VERTICAL | wxALIGN_CENTER_HORIZONTAL)
        box.Add(pFill1, 1)
        box.Add(panel_content, 15, wxEXPAND)
        box.Add(pFill2, 1)
        box.Add(label_destfolder, 1, wxALIGN_CENTER_VERTICAL | wxALIGN_LEFT)
        box.Add(if_dir, 2, wxEXPAND | wxALIGN_CENTER_VERTICAL | wxALIGN_LEFT)
        box.Add(pFill3, 1)
        box.Add(self.bOKButton, 2, wxALIGN_CENTER_VERTICAL | wxALIGN_RIGHT)
        box.Add(pFill4, 1)
        panel_outer.SetAutoLayout(True)
        panel_outer.SetSizer(box)
        panel_outer.Layout()
        
        
        pFill4 = wxPanel(self, -1)
        pFill5 = wxPanel(self, -1)
        boxo = wxBoxSizer(wxHORIZONTAL)
        boxo.Add(pFill4, 1, wxEXPAND)
        boxo.Add(panel_outer, 20, wxEXPAND)
        boxo.Add(pFill5, 1, wxEXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(boxo)
        self.Layout()

        EVT_BUTTON(self, _ID_B_OK, self.closeItDown)

        
        self.CentreOnParent()
        self.ShowModal()

    def closeItDown(self, event):
        """
        Shuts down the dialog.
        
        Should be invoked in case of an event for pressing the "close" button. The modal
        mode is ended and the dialog is destroyed.
        
        @param event: The event causing invocation of this function.
        """
        self.EndModal(0)
        self.Destroy()
