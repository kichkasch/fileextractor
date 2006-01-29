"""
Progress Dialog for the graphical interface for the ImageGenerator. 

The GUI is wxDigit / wxPython based. 
@see: http://wxpython.org for details on wxPython

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)

@var DEF_TITLE: Default title for the progress dialog window
@type DEF_TITLE: C{String}
@var DEF_SIZE: Default size for the progress dialog window
@type DEF_SIZE: Couple of 2 C{int}
@var _ID_OK: ID for event handling
@type _ID_OK: C{int}
@var _TIMER_ID: ID for timer event handling
@type _TIMER_ID: C{int}
"""
import Tools
import wx

DEF_TITLE = "Progress of imaging process"
DEF_SIZE = (400, 400)

_ID_OK = 201
_TIMER_ID = 501

class ProgressDialog(wx.Dialog):
    """
    Maintaining the dialog for the progress.
    
    Maintains some status information and a progress bar, which is, based on time,
    progressing from the beginning to the end all the time. 
    
    The status instance is constantly observed (controlled by a time) and new data
    in there is updated to the fields on the dialog.
    
    @ivar _settings: Settings instance for this generation
    @type _settings: L{Runtime.Settings}
    @ivar _status: Status instance for this generation.
    @type _status: L{Runtime.Status}
    """
    def __init__(self, parent, title = DEF_TITLE, settings=None, status=None):
        """
        Initialises the progress dialog.
        
        The controls are placed and the events are registerd. The timer is also
        initialised. 
        
        Finally, the constructor brings up the dialog itself in a
        modal manner. So, do NOT call L{ShowModal} from the outside!
        
        @param parent: Parent control
        @type parent: L{wx.Control}
        @param title: Title for the dialog window title bar
        @type title: C{String}
        @param settings: Settings instance for the generation
        @type settings: L{Runtime.Settings}
        @param status: Status instance for the generation
        @type status: L{Runtime.Status}
        """
        wx.Dialog.__init__(self, parent, -1, title, size = DEF_SIZE)
        
        self._settings = settings
        self._status = status
        
        font_headings = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        panel_outer = wx.Panel(self, -1)
        
        self._lTitle = wx.StaticText(panel_outer, -1, "Image is being processed")
        self._lTitle.SetFont(font_headings)
        self._lSource = wx.StaticText(panel_outer, -1, "Source: ")
        self._lDestination = wx.StaticText(panel_outer, -1, "Image File: ")
        self._lStartTime = wx.StaticText(panel_outer, -1, "Start Time: ")
        self._lFilesize = wx.StaticText(panel_outer, -1, "File Size: ")
        self._lTimeElapsed = wx.StaticText(panel_outer, -1, "Time elapsed: ")

        self._gauge = wx.Gauge(panel_outer, -1, 10000)
        self._gauge.SetValue(0)
        
        self._bOK = wx.Button(panel_outer, _ID_OK, "OK")
        self._updateValues(None)

        panel_fill_hor1 = wx.Panel(panel_outer, -1)
##        panel_fill_hor1.SetBackgroundColour(wx.RED)
        panel_fill_hor2 = wx.Panel(panel_outer, -1)
##        panel_fill_hor2.SetBackgroundColour(wx.RED)
        panel_fill_hor3 = wx.Panel(panel_outer, -1)
##        panel_fill_hor3.SetBackgroundColour(wx.RED)
        panel_fill_hor4 = wx.Panel(panel_outer, -1)
##        panel_fill_hor4.SetBackgroundColour(wx.RED)
        panel_fill_hor5 = wx.Panel(panel_outer, -1)
##        panel_fill_hor5.SetBackgroundColour(wx.RED)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(panel_fill_hor1, 1, wx.EXPAND)
        box.Add(self._lTitle, 2, wx.ALIGN_CENTER )
        box.Add(self._lSource, 1, wx.EXPAND)
        box.Add(self._lDestination, 1, wx.EXPAND)
        box.Add(self._lStartTime, 1, wx.EXPAND)
        box.Add(panel_fill_hor2, 1, wx.EXPAND)
        box.Add(self._lFilesize, 1, wx.EXPAND)
        box.Add(self._lTimeElapsed, 1, wx.EXPAND)
        box.Add(panel_fill_hor3, 1, wx.EXPAND)
        box.Add(self._gauge, 1, wx.EXPAND)
        box.Add(panel_fill_hor4, 1, wx.EXPAND)
        box.Add(self._bOK, 1, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        box.Add(panel_fill_hor5, 1, wx.EXPAND)
        

        panel_outer.SetAutoLayout(True)
        panel_outer.SetSizer(box)
        panel_outer.Layout()

        pFill1 = wx.Panel(self, -1)
##        pFill1.SetBackgroundColour(wx.RED)
        pFill2 = wx.Panel(self, -1)
##        pFill2.SetBackgroundColour(wx.RED)
        boxo = wx.BoxSizer(wx.HORIZONTAL)
        boxo.Add(pFill1, 1, wx.EXPAND)
        boxo.Add(panel_outer, 12, wx.EXPAND)
        boxo.Add(pFill2, 1, wx.EXPAND)


        self.SetAutoLayout(True)
        self.SetSizer(boxo)
        self.Layout()
        
        self._mytimer = wx.Timer(self, _TIMER_ID)
        self._mytimer.Start(1000, 0)
        
        self._bOK.Enable(0)
        wx.EVT_TIMER(self, _TIMER_ID, self._updateValues)
        wx.EVT_BUTTON(self, _ID_OK, self._evtOK)
        self.ShowModal()

    def _updateValues(self, event):
        """
        Function to be called frequently for updating the controls on the dialog window.
        
        This function is called by the time every second. It gains the latest data from 
        the status instance and updates the values for the controls. The gauge for the 
        progress is just put forward a certain amount of progress.
        
        If the status instance indicates the end of the execution, the title of the dialog
        is either set to "finished" or to "error" depending on the value for error in the
        status instance.
        
        @param event: Event causing this function.
        """
        self._lSource.SetLabel("Source: " + self._settings.getSource())
        self._lDestination.SetLabel("Image File: " + self._settings.getDestination())
        starttime = Tools.processTime(int(self._status.getStartTime()) % (60 * 60 * 24))
        self._lStartTime.SetLabel("Start Time: " + starttime[0] + ":" + starttime[1] + ":" + starttime[2])

        elapsed = Tools.processTime(self._status.getElapsedTime())
        if self._status.getEndFilesize():
            self._lFilesize.SetLabel("File Size: %s / %s (%d %%)" %(self._formatSize(self._status.getDestinationFileSize()), self._formatSize(self._status.getEndFilesize()), (self._status.getDestinationFileSize() * 100 / self._status.getEndFilesize())))
            self._gauge.SetValue(int(self._status.getDestinationFileSize() * 10000 / self._status.getEndFilesize()))
            if  self._status.getDestinationFileSize() != 0 and  self._status.getEndFilesize() - self._status.getDestinationFileSize() != 0:
                remaining = self._status.getElapsedTime() / self._status.getDestinationFileSize() * (self._status.getEndFilesize() - self._status.getDestinationFileSize())
                remaining = Tools.processTime(remaining)
                self._lTimeElapsed.SetLabel("Time elapsed: " + elapsed[0] + ":" + elapsed[1] + ":" + elapsed[2] + "  (remaining: " + remaining[0] + ":" + remaining[1] + ":" + remaining[2] + ")")
        else:
            self._lFilesize.SetLabel("File Size: %s" %(self._formatSize(self._status.getDestinationFileSize())))
            val = self._gauge.GetValue()
            self._gauge.SetValue((val + 2000 ) % 10000)
            self._lTimeElapsed.SetLabel("Time elapsed: " + elapsed[0] + ":" + elapsed[1] + ":" + elapsed[2])
        
        
        if self._status.isFinished():
            if self._status.getError() != None:
                self._lTitle.SetLabel("Error whilst Imaging")
            else:
                self._lTitle.SetLabel("Imaging finished")
            self._lTimeElapsed.SetLabel("Time elapsed: " + elapsed[0] + ":" + elapsed[1] + ":" + elapsed[2])
            self._gauge.SetValue(10000)
            self._bOK.Enable(1)
            
    def _formatSize(self, size):
        if size / 1024 < 1:
            return "%d Bytes" %(size)
        if size / (1024 * 1024) < 1:
            return "%d.%d KB" %(size / 1024, (size % 1024) / 103)
        return "%d.%d MB" %(size / (1024  * 1024),  (size % (1024  * 1024))/ (103 * 1024))

    def _evtOK(self, event):
        """
        Event handler function, called when the OK button is pressed.
        
        Stops the timer and end the modality of the dialog. Finally, the dialog is destroyed.
        
        @param event: Event causing this function.
        """
        self._mytimer.Stop()
        self.EndModal(1)
        self.Destroy()
    
