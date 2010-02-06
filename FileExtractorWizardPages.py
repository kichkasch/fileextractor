"""
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
import wx
from wx.wizard import *
import os
import os.path
import sys
import FESettings
from FESettings import getSettings
from FileExtractorWizard import _ID_INFO_SOURCES, _ID_B_DIR

class AbstractFileExtractorWizardPage(WizardPageSimple):
    def __init__(self, parent, prev=None, next=None, imagePath = None):
        WizardPageSimple.__init__(self, parent, prev, next)
        
#        self._baseDir = os.path.abspath(os.path.dirname(sys.argv[0]))
        self._baseDir = FESettings.BASEDIR
        image = wx.Bitmap(os.path.join(self._baseDir, imagePath), wx.BITMAP_TYPE_PNG)
       
        panel_outer = wx.Panel(self, -1)

        imageView = wx.StaticBitmap(panel_outer, -1, image, wx.DefaultPosition, wx.DefaultSize)
              
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(imageView, 4, wx.TOP)
        panel_outer.SetAutoLayout(True)
        panel_outer.SetSizer(box)
        panel_outer.Layout()

        self._contentPane = wx.Panel(self, -1)
        boxo = wx.BoxSizer(wx.VERTICAL)
        boxo.Add(panel_outer, 3, wx.EXPAND)
        boxo.Add(self._contentPane, 8, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(boxo)
        self.Layout()
        
    def getContentPane(self):
        return self._contentPane;

class WizardPageSplash(AbstractFileExtractorWizardPage):
    def __init__(self, parent):
        AbstractFileExtractorWizardPage.__init__(self, parent, None, None, "newicons/wizard_heading.png")

        contentPane = self.getContentPane()
        font_headings = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
#        p = wx.Panel(contentPane, -1)
        label = wx.StaticText(contentPane, -1, "\n\nFour steps to recover your data:" +
                              "\n\n  1. Apply your Settings\n  2. Create an image of the device" +
                              "\n  3. Extract the data\n  4. Show results" +
                              "\n\nClick 'Next' to start recovery.")
        label.SetFont(font_headings)
        
        label2 = wx.StaticText(contentPane, -1, "\n%s %s\nby %s\nemail: %s" %(FESettings.PROGRAM_NAME, FESettings.VERSION, FESettings.AUTHOR, FESettings.EMAIL))
        
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(label, 2, wx.EXPAND)
        box.Add(label2, 1, wx.RIGHT)
        contentPane.SetAutoLayout(True)
        contentPane.SetSizer(box)
        contentPane.Layout()
        print self
        
class WizardPageSetup(AbstractFileExtractorWizardPage):
    def __init__(self, parent):
        AbstractFileExtractorWizardPage.__init__(self, parent, None, None,"newicons/wizard_heading_1.png")

        contentPane = self.getContentPane()
        font_headings = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        lSources = wx.StaticText(contentPane, -1, "Choose your source device")
        lSources.SetFont(font_headings)
        
        panel_info = wx.Panel(contentPane, -1)
        choicesSources = []
        self._cbSources = wx.ComboBox(panel_info, -1, choices = choicesSources)

        bmDir = wx.Bitmap(os.path.join(self._baseDir, "icons/info.png"), wx.BITMAP_TYPE_PNG);
        panel_fill = wx.Panel(panel_info, -1)
##        panel_fill.SetBackgroundColour(wx.RED)
        bInfoSources = wx.BitmapButton(panel_info, _ID_INFO_SOURCES, bmDir, size=(28,28))        

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._cbSources, 16, wx.ALIGN_CENTER)
        box.Add(panel_fill, 1, wx.EXPAND)
        box.Add(bInfoSources, 3, wx.ALIGN_CENTER)
        panel_info.SetAutoLayout(True)
        panel_info.SetSizer(box)
        panel_info.Layout()
        
        
        lOutputDir = wx.StaticText (contentPane, -1, "Choose your output directory")
        lOutputDir.SetFont(font_headings)
        panel_dir = wx.Panel(contentPane, -1)
        if getSettings().getValue('output_dir'):
            import tools
            self.if_dir = wx.TextCtrl(panel_dir, -1, tools.determineAbsPath(getSettings().getValue('output_dir')))
        else:
            self.if_dir = wx.TextCtrl(panel_dir, -1, 'Working Directory')
        self.if_dir.SetEditable(False)        
        bmDir = wx.Bitmap(os.path.join(self._baseDir, "icons/browse.png"), wx.BITMAP_TYPE_PNG);
        panel_fill = wx.Panel(panel_dir, -1)
        bChooseDir = wx.BitmapButton(panel_dir, _ID_B_DIR, bmDir, size=(28,28))        

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.if_dir, 16, wx.ALIGN_CENTER)
        box.Add(panel_fill, 1, wx.ALIGN_CENTER)
        box.Add(bChooseDir, 3, wx.ALIGN_CENTER)
        panel_dir.SetAutoLayout(True)
        panel_dir.SetSizer(box)
        panel_dir.Layout()
        
        
        panel_fill1 = wx.Panel(contentPane, -1)
        panel_fill2 = wx.Panel(contentPane, -1)
        panel_fill3 = wx.Panel(contentPane, -1)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(panel_fill1, 3, wx.EXPAND)
        box.Add(lSources, 2, wx.EXPAND)
        box.Add(panel_info, 2, wx.EXPAND)
        box.Add(panel_fill2, 2, wx.EXPAND)
        box.Add(lOutputDir, 2, wx.EXPAND)
        box.Add(panel_dir, 2, wx.EXPAND)
        box.Add(panel_fill3, 7, wx.EXPAND)
        contentPane.SetAutoLayout(True)
        contentPane.SetSizer(box)
        contentPane.Layout()
        
        
class WizardPageImage(AbstractFileExtractorWizardPage):
    def __init__(self, parent):
        AbstractFileExtractorWizardPage.__init__(self, parent, None, None,"newicons/wizard_heading_2.png")

        contentPane = self.getContentPane()
        font_headings = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        panel_outer = contentPane
        
        self._lSource = wx.StaticText(panel_outer, -1, "Source: ")
        self._lSource.SetFont(font_headings)
        self._lFilesize = wx.StaticText(panel_outer, -1, "File Size: ")
        self._lFilesize.SetFont(font_headings)
        self._lTimeElapsed = wx.StaticText(panel_outer, -1, "Time elapsed: ")
        self._lTimeElapsed.SetFont(font_headings)

        self._gauge = wx.Gauge(panel_outer, -1, 10000)
        self._gauge.SetValue(0)
        
        panel_fill1 = wx.Panel(contentPane, -1)
        panel_fill2 = wx.Panel(contentPane, -1)
        panel_fill3 = wx.Panel(contentPane, -1)
        panel_fill4 = wx.Panel(contentPane, -1)
        panel_fill5 = wx.Panel(contentPane, -1)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(panel_fill1, 3, wx.EXPAND)
        box.Add(self._lSource, 2, wx.EXPAND)
        box.Add(panel_fill2, 2, wx.EXPAND)
        box.Add(self._lFilesize, 2, wx.EXPAND)
        box.Add(panel_fill3, 2, wx.EXPAND)
        box.Add(self._lTimeElapsed, 2, wx.EXPAND)
        box.Add(panel_fill4, 3, wx.EXPAND)
        box.Add(self._gauge, 2, wx.EXPAND)
        box.Add(panel_fill5, 2, wx.EXPAND)
        contentPane.SetAutoLayout(True)
        contentPane.SetSizer(box)
        contentPane.Layout()

class WizardPageRecover(AbstractFileExtractorWizardPage):
    def __init__(self, parent):
        AbstractFileExtractorWizardPage.__init__(self, parent, None, None,  "newicons/wizard_heading_3.png")

        contentPane = self.getContentPane()
        font_headings = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        panel_outer = contentPane
        
        self.label_current_found = wx.StaticText(panel_outer, -1, "Files recovered: 0")
        self.label_current_found.SetFont(font_headings)
        self.label_current_percentage = wx.StaticText(panel_outer, -1, "Finished: 0 Bytes / 0 Bytes (00.00 %)")
        self.label_current_percentage.SetFont(font_headings)
        self.label_current_time = wx.StaticText(panel_outer, -1, "Time elapsed: 00:00:00")
        self.label_current_time.SetFont(font_headings)

        self.gauge_current_file = wx.Gauge(panel_outer, -1, 10000)
        self.gauge_current_file.SetValue(0)
        
        panel_fill1 = wx.Panel(contentPane, -1)
        panel_fill2 = wx.Panel(contentPane, -1)
        panel_fill3 = wx.Panel(contentPane, -1)
        panel_fill4 = wx.Panel(contentPane, -1)
        panel_fill5 = wx.Panel(contentPane, -1)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(panel_fill1, 3, wx.EXPAND)
        box.Add(self.label_current_found, 2, wx.EXPAND)
        box.Add(panel_fill2, 2, wx.EXPAND)
        box.Add(self.label_current_percentage, 2, wx.EXPAND)
        box.Add(panel_fill3, 2, wx.EXPAND)
        box.Add(self.label_current_time, 2, wx.EXPAND)
        box.Add(panel_fill4, 3, wx.EXPAND)
        box.Add(self.gauge_current_file, 2, wx.EXPAND)
        box.Add(panel_fill5, 2, wx.EXPAND)
        contentPane.SetAutoLayout(True)
        contentPane.SetSizer(box)
        contentPane.Layout()
        

class WizardPageResults(AbstractFileExtractorWizardPage):
    def __init__(self, parent):
        AbstractFileExtractorWizardPage.__init__(self, parent, None, None,"newicons/wizard_heading_4.png")

        contentPane = self.getContentPane()
        font_headings = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self._lFilesRecovered = wx.StaticText(contentPane, -1, "Files recovered: 0")
        self._lFilesRecovered.SetFont(font_headings)
        self._timeOverall = wx.StaticText(contentPane, -1, "Overall time: 00:00:00")
        self._timeOverall.SetFont(font_headings)
        self._outputLocation = wx.StaticText(contentPane, -1, "Look for your recovered files in:\n Working Directory")
        self._outputLocation.SetFont(font_headings)
        
        panel_fill1 = wx.Panel(contentPane, -1)
        panel_fill2 = wx.Panel(contentPane, -1)
        panel_fill3 = wx.Panel(contentPane, -1)
        panel_fill4 = wx.Panel(contentPane, -1)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(panel_fill1, 3, wx.EXPAND)
        box.Add(self._lFilesRecovered, 2, wx.EXPAND)
        box.Add(panel_fill2, 2, wx.EXPAND)
        box.Add(self._timeOverall, 2, wx.EXPAND)
        box.Add(panel_fill3, 2, wx.EXPAND)
        box.Add(self._outputLocation, 3, wx.EXPAND)
        box.Add(panel_fill4, 6, wx.EXPAND)
        contentPane.SetAutoLayout(True)
        contentPane.SetSizer(box)
        contentPane.Layout()
