"""
Provides one class for a progress dialog for the FileExtractor GUI.

The GUI is wxDigit / wxPython based. 
@see: http://wxpython.org for details on wxPython

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)
"""
from wxPython.wx import *
import tools
import FileExtractorCore
import thread
from time import sleep
import time
import signatures
import ResultDialog
from ExecutionSettings import ExecutionSettings, ExecutionStatus

_ID_B_RESULT = 301
_TIMER_ID = 501

class ProgressDialog(wxDialog):
    """ Progress Dialog for the FileExtractor GUI FrontEnd
        
        A L{ExecutionSettings.ExecutionSettings} instance has to be passed to this class.
        A new L{ExecutionSettings.ExecutionStatus} instance will be created in here.
        A timer is implemented which will lookup for changes in the status class once every
        second. Changes are visualised with two progress bars (one for the current source
        file and one for the overall progress) and textual output (for elapsed time,
        files found and percentage finished).
        
        @ivar status: Reference to status instance.
        @type status: L{ExecutionSettings.ExecutionStatus} 
        @ivar settings: Reference to settings instance.
        @type settings: L{ExecutionSettings.ExecutionSettings} 
    """
    def __init__(self, parent, ID, title, settings):
        """
        Initalises the progress dialog.
        
        Creates a wxDialog (size L{wxSize(400,500)}) and fills the content. All events are
        registered with their private functions. After setting up the components, the
        function L{ExecutionController} is called in a new thread. A new timer is
        created, so that the function L{updateControls} is called once every second.
        Finally, the dialog window is adjusted at the centre of the parent window.
        
        This constructor calls the L{wxPython.wx.wxDialog.ShowModal} itself; hence, it must not be 
        invoked from the outside after initalisation.
        
        @param parent: Parent window for this wxDialog - passed to the superclass constructor (wxPython.wx.wxDialog.__init__)
        @type parent: L{wxPython.wx.wxFrame}
        @param ID: ID for this component - passed to the superclass constructor (wxPython.wx.wxDialog.__init__)
        @type ID: C{int}
        @param title: Title for the dialog - - passed to the superclass constructor (wxPython.wx.wxDialog.__init__)
        @type title: C{String}
        @param settings: Settings for the execution
        @type settings: L{ExecutionSettings.ExecutionSettings}
        """
        wxDialog.__init__(self, parent, ID, title,
                         wxDefaultPosition, wxSize(400, 500))
        
        self.settings = settings
        
        font_headings = wxFont(12, wxDEFAULT, wxNORMAL, wxBOLD)
        
        panel_outer = wxPanel(self, -1)
        
        panel_current_file = wxPanel(panel_outer, -1)
##        pFillCurrent1 = wxPanel(panel_current_file, -1)
##        pFillCurrent2 = wxPanel(panel_current_file, -1)
##        pFillCurrent3 = wxPanel(panel_current_file, -1)
        pFillCurrent4 = wxPanel(panel_current_file, -1)
        label_current_file = wxStaticText (panel_current_file, -1 , "Current File")
        label_current_file.SetFont(font_headings)
        self.label_current_filename = wxStaticText (panel_current_file, -1, "Source filename: ")
        self.label_current_found = wxStaticText (panel_current_file, -1, "Files Found: 0")
        self.label_current_time = wxStaticText(panel_current_file, -1, "Time elapsed: 00:00:00")
        self.label_current_percentage = wxStaticText(panel_current_file, -1, "Finished: 00.00 % (0 / 0 Bytes)")
        self.gauge_current_file = wxGauge(panel_current_file, -1, 10000)
        self.gauge_current_file.SetValue(0)
        
        box_current_file = wxBoxSizer(wxVERTICAL)
##        box_current_file.Add(pFillCurrent1, 1, wxEXPAND)
        box_current_file.Add(label_current_file, 2, wxALIGN_CENTER_VERTICAL | wxALIGN_CENTER_HORIZONTAL)
##        box_current_file.Add(pFillCurrent2, 1, wxEXPAND)
        box_current_file.Add(self.label_current_filename, 2, wxEXPAND)
        box_current_file.Add(self.label_current_found, 2, wxEXPAND)
        box_current_file.Add(self.label_current_time, 2, wxEXPAND)
        box_current_file.Add(self.label_current_percentage, 2, wxEXPAND)
##        box_current_file.Add(pFillCurrent3, 1, wxEXPAND)
        box_current_file.Add(self.gauge_current_file, 1, wxEXPAND)
        box_current_file.Add(pFillCurrent4, 1, wxEXPAND)
        panel_current_file.SetAutoLayout(True)
        panel_current_file.SetSizer(box_current_file)
        panel_current_file.Layout()

        panel_overall = wxPanel(panel_outer, -1)
##        pFillOverall1 = wxPanel(panel_overall, -1)
##        pFillOverall2 = wxPanel(panel_overall, -1)
##        pFillOverall3 = wxPanel(panel_overall, -1)
        pFillOverall4 = wxPanel(panel_overall, -1)
        label_overall = wxStaticText (panel_overall, -1 , "Overall Progress")
        label_overall.SetFont(font_headings)
        self.label_overall_filesdone = wxStaticText (panel_overall, -1, "Current source file: 0 / 0")
        self.label_overall_found = wxStaticText (panel_overall, -1, "Files found: 0")
        self.label_overall_time = wxStaticText(panel_overall, -1, "Time elapsed: 00:00:00")
        self.label_overall_percentage = wxStaticText(panel_overall, -1, "Finished: 00.00 %")
        self.gauge_overall = wxGauge(panel_overall, -1, 10000)
        self.gauge_overall.SetValue(0)
        
        box_overall = wxBoxSizer(wxVERTICAL)
##        box_overall.Add(pFillOverall1, 1, wxEXPAND)
        box_overall.Add(label_overall, 2, wxALIGN_CENTER_VERTICAL | wxALIGN_CENTER_HORIZONTAL)
##        box_overall.Add(pFillOverall2, 1, wxEXPAND)
        box_overall.Add(self.label_overall_filesdone, 2, wxEXPAND)
        box_overall.Add(self.label_overall_found, 2, wxEXPAND)
        box_overall.Add(self.label_overall_time, 2, wxEXPAND)
        box_overall.Add(self.label_overall_percentage, 2, wxEXPAND)
##        box_overall.Add(pFillOverall3, 1, wxEXPAND)
        box_overall.Add(self.gauge_overall, 1, wxEXPAND)
        box_overall.Add(pFillOverall4, 1, wxEXPAND)
        panel_overall.SetAutoLayout(True)
        panel_overall.SetSizer(box_overall)
        panel_overall.Layout()

        pFill1 = wxPanel(panel_outer, -1)
        pFill2 = wxPanel(panel_outer, -1)
        pFill3 = wxPanel(panel_outer, -1)

        self.bResultButton = wxButton(panel_outer, _ID_B_RESULT, "Results")
        self.bResultButton.Enable(false)

        box = wxBoxSizer(wxVERTICAL)
        box.Add(pFill1, 1)
        box.Add(panel_current_file, 10, wxEXPAND)
        box.Add(pFill2, 1)
        box.Add(panel_overall, 10, wxEXPAND)
        box.Add(self.bResultButton, 1, wxALIGN_CENTER_VERTICAL | wxALIGN_RIGHT)
        box.Add(pFill3, 1)
        panel_outer.SetAutoLayout(True)
        panel_outer.SetSizer(box)
        panel_outer.Layout()
        
        pFill4 = wxPanel(self, -1)
        pFill5 = wxPanel(self, -1)
        
        boxo = wxBoxSizer(wxHORIZONTAL)
        boxo.Add(pFill4, 1, wxEXPAND)
        boxo.Add(panel_outer, 12, wxEXPAND)
        boxo.Add(pFill5, 1, wxEXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(boxo)
        self.Layout()
        
        # timer for updating information
        self.label_current_filename_value = "Source filename: "
        self.label_overall_filesdone_value = "Current source file: 0 / 0"
        self.label_current_time_value = "Time elapsed: 00:00:00"
        self.gauge_current_file_value = 0
        self.label_current_percentage_value = "Finished: 00.00 % (0.000 / 0.000 MB)"
        self.gauge_overall_value = 0
        self.label_overall_percentage_value = "Finished: 00.00 %"
        self.label_current_found_value = "Files Found: 0"
        self.label_overall_found_value = "Files Found: 0"
        self.label_overall_time_value = "Time elapsed: 00:00:00"
        
        mytimer = wxTimer(self, _TIMER_ID)
        mytimer.Start(1000)
        
        thread.start_new_thread(self.ExecutionController,())
        
        EVT_BUTTON(self, _ID_B_RESULT, self._ShowResult)
        EVT_TIMER(self, _TIMER_ID, self.updateControls)
        
        self.CentreOnParent()
        self.ShowModal()
        
    def ExecutionController(self):
        """
        Responsible for the invocation of the FileExtractorCore
        
        A new ExecutionStatus instance is created (L{self.status}). Afterwards, the list of source files
        (as given in the settings object) is itererated on for each source file the 
        FileExtractor Core is initialised and started.
        
        This message is invoked whenever the "Start" button is pressed on the dialog.
        """
        self.status = ExecutionStatus(self.settings)
        self.startTime = time.time()
        for srcFile in self.settings.sourceFiles:
            if FileExtractorCore.init(self.status) < 0:
                print "Error for " + srcFile
            signs, counter = FileExtractorCore.startSearch(self.status)
    
    def updateControls(self, event):
        """
        Updates all the controls in the dialog with the values provided by the L{self.status}
        instance.
        
        This message is invoked once every second by a timer installed in this class.
        
        @param event: Timer event.
        """
        # calculation
        if self.status.hasMoreSourceFiles():
            self.label_current_filename_value = "Source filename: " + self.status.getCurrentFile()
            elapsed = self.status.getCurrentElapsedTime()
            time1 = tools.processTime(elapsed)
            self.label_current_time_value = "Time elapsed: "+time1[0]+":"+time1[1]+":"+time1[2]
            self.gauge_current_file_value = self.status.getCurrentFinished() * 10000 / self.status.getCurrentSize()
            progress = int(round(self.status.getCurrentFinished() * 10000.0 / self.status.getCurrentSize())) 
            self.label_current_percentage_value = "Finished: "+ str(progress / 100) +"."+ str(progress % 100) +"% ("+ str(self.status.getCurrentFinished())+" / "+str(self.status.getCurrentSize())+" Bytes)"
            self.label_current_found_value = "Files Found: " + str(self.status.getCurrentFound())
            self.label_overall_filesdone_value = "Current source file: "+ str(self.status.finished+1) + " / " + str(self.status.getSourceFileNumber())
            progress_per_file = 10000.0 / self.status.getSourceFileNumber()
            progressOverall = int(round(self.status.finished * progress_per_file + self.status.getCurrentFinished() * progress_per_file / self.status.getCurrentSize()))
        else:
            self.label_current_filename_value = "Source filename: "
            self.label_current_time_value = "Time elapsed: "
            self.gauge_current_file_value = 10000
            progress = 10000.0
            self.label_current_percentage_value = "Finished: "+ str(progress / 100) +"."+ str(progress % 100) +"% "
            self.label_current_found_value = "Files Found: "
            self.label_overall_filesdone_value = "Current source file: "+ str(self.status.getSourceFileNumber()) + " / " + str(self.status.getSourceFileNumber())
            progress_per_file = 10000.0 / self.status.getSourceFileNumber()
            progressOverall = 10000.0
        self.gauge_overall_value = progressOverall
        self.label_overall_percentage_value = "Finished: "+str(progressOverall/100)+"."+str(progressOverall%100)+" %"
        self.label_overall_found_value = "Files Found: " + str(self.status.getOverallFound())
        now = time.time()
        time1 = tools.processTime(now - self.startTime)
        self.label_overall_time_value = "Time elapsed: "+time1[0]+":"+time1[1]+":"+time1[2]
        
        # and applying
        self.label_current_filename.SetLabel(self.label_current_filename_value)
        self.label_overall_filesdone.SetLabel(self.label_overall_filesdone_value)
        self.label_current_time.SetLabel(self.label_current_time_value)
        self.gauge_current_file.SetValue(self.gauge_current_file_value)
        self.label_current_percentage.SetLabel(self.label_current_percentage_value)
        self.gauge_overall.SetValue(self.gauge_overall_value)
        self.label_overall_percentage.SetLabel(self.label_overall_percentage_value)
        self.label_current_found.SetLabel(self.label_current_found_value)
        self.label_overall_found.SetLabel(self.label_overall_found_value)
        self.label_overall_time.SetLabel(self.label_overall_time_value)
        if not self.status.hasMoreSourceFiles():
            self.bResultButton.Enable(true)

    def _ShowResult(self, event):
        resDialog = ResultDialog.ResultDialog(self, -1, "Searching outcomes", self.status)
        
        self.EndModal(0)
        self.Destroy()
