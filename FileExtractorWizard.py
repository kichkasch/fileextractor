#!/usr/bin/env python
"""
Reworked (wizard based) graphical interface for the FileExtractor. Contains the Wizard and a simple Application for
starting up the enhanced FileExtractor GUI Frontend.

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

import wx
from wx.wizard import *
from FileExtractorWizardPages import *
import sys
import os
import os.path
import thread
from imagegenerator import Tools
from ExecutionSettings import *
import signatures
import FileExtractorCore
import tools
import FESettings


_ID_WIZARD = 101
_ID_INFO_SOURCES = 201
_ID_B_DIR = 202
_TIMER_ID = 301
_TIMER_ID1 = 302
DEBUG_FILENAME = "./fileextractordebug.txt"


class FileExtractorWizard(Wizard):
    def __init__(self, parent = None, title = "%s %s" %(FESettings.PROGRAM_NAME, FESettings.VERSION)):
        Wizard.__init__(self, parent, _ID_WIZARD, title)

        #wx.InitAllImageHandlers()
        #wx.Image_AddHandler(wx.PNGHandler())
        self._page0 = WizardPageSplash(self)
        self._page1 = WizardPageSetup(self)
        self._page2 = WizardPageImage(self)
        self._page3 = WizardPageRecover(self)
        self._page4 = WizardPageResults(self)

        self._page0.SetNext(self._page1)
        self._page1.SetPrev(self._page0)
        self._page1.SetNext(self._page2)
        self._page2.SetPrev(self._page1)
        self._page2.SetNext(self._page3)
        self._page3.SetPrev(self._page2)
        self._page3.SetNext(self._page4)
        self._page4.SetPrev(self._page3)
        
        self.SetPageSize((300,370))


        EVT_WIZARD_PAGE_CHANGED(self, _ID_WIZARD, self._evtPageChanged)
        wx.EVT_BUTTON(self, _ID_INFO_SOURCES, self._evtInfoSources)
        wx.EVT_BUTTON(self, _ID_B_DIR, self._ChangeOutputDir)

        self.RunWizard(self._page0)

    def _evtPageChanged(self, evt):
        if evt.GetDirection():
            if self.GetCurrentPage() == self._page1:
                self._processSourcesList()
            elif self.GetCurrentPage() == self._page2:
                self.FindWindowById(wx.ID_FORWARD).Disable()
                self.FindWindowById(wx.ID_BACKWARD).Disable()
                self._startImageProcessing()
            elif self.GetCurrentPage() == self._page3:
                self.FindWindowById(wx.ID_FORWARD).Disable()
                self.FindWindowById(wx.ID_BACKWARD).Disable()
                self._startFileRecovery()
            elif self.GetCurrentPage() == self._page4:
                self._displayResults()

    def _processSourcesList(self):
        corename = tools.determineCoreName( FESettings.getSettings().getValue("ig_default_core"))
        locationDD = tools.determineAbsPath( FESettings.getSettings().getValue("ig_location_dd"))
        #print corename

        self._devicesDict = {}
        self._core  = self._initCore(corename, ddloc = locationDD)
        suggestions, devices = self._core.getPossibleSources()
        self._page1._cbSources.Clear()
        i = 0
        for sug in suggestions:
            self._page1._cbSources.Append(sug, None)
            self._devicesDict[sug] = devices[i]
            i += 1

    def _initCore(self, corename, settings = None, ddloc = None):
        from imagegenerator import CoreManager, Runtime
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

    def _evtInfoSources(self, evt):
        if self._core != None:
            message = self._core.getSourceInfo()
            dialog = wx.MessageDialog(self, message, "What are these entries about...", wx.ICON_INFORMATION | wx.OK )
            dialog.ShowModal()

    def _ChangeOutputDir(self, event):
        dirDialog = wx.DirDialog(self, "Choose Output Directory")
        if dirDialog.ShowModal() == wx.ID_OK:
            path = dirDialog.GetPath()
            self.dest_folder = path
            self._page1.if_dir.SetValue(path)
        dirDialog.Destroy()

    def _startImageProcessing(self):
        from imagegenerator import Runtime

        corename = tools.determineCoreName( FESettings.getSettings().getValue("ig_default_core"))
        location_dd = tools.determineAbsPath( FESettings.getSettings().getValue("ig_location_dd"))
        location_dest = tools.determineAbsPath( os.path.join(FESettings.getSettings().getValue("ig_output_dir"), FESettings.getSettings().getValue("ig_output_filename")))
        
        self._timeAllTogether = 0
        
        sourceTmp = self._page1._cbSources.GetValue()
##            sourceTmp = self._cbSources.GetStringSelection()
        if self._devicesDict.has_key(sourceTmp):
            source = self._devicesDict[sourceTmp]
        else:
            source = sourceTmp
        #location_dest = "d:\\temp\\dd.img"
        if os.path.exists(location_dest):
            print "Image file existing - I am overwriting."
            os.remove(location_dest)
#        if not self._checkOverwrite(location_dest):
#            return
        redirectBuffer = DEBUG_FILENAME
        settings = Runtime.Settings(path_dd = location_dd, source = source, 
                destination = location_dest, redirectOutput = redirectBuffer)
        #corename = tools.determineCoreName( getSettings("ig_default_core"))
        #print corename
        core = self._initCore(corename, settings)

        status = Runtime.Status()
        status.setStarted()
        sizeEstimation = core.getSizeEstimationForPartition(settings.getSource())
        if sizeEstimation:
            status.setEndFilesize(sizeEstimation)
        thread.start_new_thread(core.createImage,(status,))
        
        self._mytimer = wx.Timer(self, _TIMER_ID)
        self._mytimer.Start(1000, 0)
        wx.EVT_TIMER(self, _TIMER_ID, self._updateValuesImaging)
        self._status = status
        self._settings = settings

        
#        if self._callback != None:
#            if status.getError() != None:
#                self._callback.error(status.getError())
#            elif status.isFinished():
#                self._callback.success(settings.getDestination())

    def _updateValuesImaging(self, event):
        self._page2._lSource.SetLabel("Source: " + self._settings.getSource())
        elapsed = Tools.processTime(self._status.getElapsedTime())
        if self._status.getEndFilesize():
            self._page2._lFilesize.SetLabel("File Size: %s / %s (%d %%)" %(self._formatSize(self._status.getDestinationFileSize()), self._formatSize(self._status.getEndFilesize()), (self._status.getDestinationFileSize() * 100 / self._status.getEndFilesize())))
            self._page2._gauge.SetValue(int(self._status.getDestinationFileSize() * 10000 / self._status.getEndFilesize()))
            if  self._status.getDestinationFileSize() != 0 and  self._status.getEndFilesize() - self._status.getDestinationFileSize() != 0:
                remaining = self._status.getElapsedTime() / self._status.getDestinationFileSize() * (self._status.getEndFilesize() - self._status.getDestinationFileSize())
                remaining = Tools.processTime(remaining)
                self._page2._lTimeElapsed.SetLabel("Time elapsed: " + elapsed[0] + ":" + elapsed[1] + ":" + elapsed[2] + "  (- " + remaining[0] + ":" + remaining[1] + ":" + remaining[2] + ")")
        else:
            self._page2._lFilesize.SetLabel("File Size: %s" %(self._formatSize(self._status.getDestinationFileSize())))
            val = self._page2._gauge.GetValue()
            self._page2._gauge.SetValue((val + 2000 ) % 10000)
            self._page2._lTimeElapsed.SetLabel("Time elapsed: " + elapsed[0] + ":" + elapsed[1] + ":" + elapsed[2])
            
        if self._status.isFinished():
            if self._status.getError() != None:
                print "error"
                #self._lTitle.SetLabel("Error whilst Imaging")
            else:
                #self._lTitle.SetLabel("Imaging finished")
                print "done - all fine"
            self._page2._lTimeElapsed.SetLabel("Time elapsed: " + elapsed[0] + ":" + elapsed[1] + ":" + elapsed[2])
            self._page2._gauge.SetValue(10000)
            self._mytimer.Stop()
            self._timeAllTogether = self._status.getElapsedTime()
            self.FindWindowById(wx.ID_FORWARD).Enable()
            self.FindWindowById(wx.ID_BACKWARD).Enable()
      
    def _formatSize(self, size):
        if size / 1024 < 1:
            return "%d Bytes" %(size)
        if size / (1024 * 1024) < 1:
            return "%d.%d KB" %(size / 1024, (size % 1024) / 103)
        return "%d.%d MB" %(size / (1024  * 1024),  (size % (1024  * 1024))/ (103 * 1024))
        
    def _startFileRecovery(self):
        location_img = tools.determineAbsPath( os.path.join(FESettings.getSettings().getValue("ig_output_dir"), FESettings.getSettings().getValue("ig_output_filename")))
        if self._page1.if_dir.GetValue() == "Working Directory":
            location_dest = tools.determineAbsPath("./")
        else:
            location_dest = tools.determineAbsPath(self._page1.if_dir.GetValue())
        
        self.settings = ExecutionSettings(sourceFiles = [location_img], 
                                          signatures = signatures.getCopyOfAllSignauteres(),
                                          output_frequency = 2300, output_level = 0,
                                          dest_folder = location_dest)
        self.status = ExecutionStatus(self.settings)
        self.startTime = time.time()

        if FileExtractorCore.init(self.status) < 0:
            print "Error on initialisation"
            
        thread.start_new_thread(self._startRecoveryInThred,(self.status,))

        self._mytimer = wx.Timer(self, _TIMER_ID1)
        self._mytimer.Start(1000, 0)
        wx.EVT_TIMER(self, _TIMER_ID1, self._updateValuesRecovery)
        
    def _startRecoveryInThred(self, status):
        FileExtractorCore.startSearch(status)
        self._mytimer.Stop()

        now = time.time()
        self._timeAllTogether += (now - self.startTime)
        self._updateValuesRecovery(None)
        self.FindWindowById(wx.ID_FORWARD).Enable()
        self.FindWindowById(wx.ID_BACKWARD).Enable()
        
    def _updateValuesRecovery(self, event):
        if not self.status.hasMoreSourceFiles():
            return
        elapsed = self.status.getCurrentElapsedTime()
        time1 = tools.processTime(elapsed)
        self.label_current_time_value = "Time elapsed: "+time1[0]+":"+time1[1]+":"+time1[2]
        
        if  self.status.getCurrentFinished() != 0 and (self.status.getCurrentSize() - self.status.getCurrentFinished()) != 0:
            remaining = self.status.getCurrentElapsedTime() / self.status.getCurrentFinished() * (self.status.getCurrentSize() - self.status.getCurrentFinished())
            remaining = tools.processTime(remaining)
            elapsed = time1
            self.label_current_time_value = "Time elapsed: " + elapsed[0] + ":" + elapsed[1] + ":" + elapsed[2] + "  (- " + remaining[0] + ":" + remaining[1] + ":" + remaining[2] + ")"
        
        self.gauge_current_file_value = self.status.getCurrentFinished() * 10000 / self.status.getCurrentSize()
        progress = int(round(self.status.getCurrentFinished() * 10000.0 / self.status.getCurrentSize())) 
        self.label_current_percentage_value = "Finished: "+ self._formatSize(self.status.getCurrentFinished())+" / "+self._formatSize(self.status.getCurrentSize()) + " (" + str(progress / 100) +"."+ str(progress  % 100 / 10) + str(progress % 100 % 10) +" %)"
        self.label_current_found_value = "Files recovered: " + str(self.status.getCurrentFound())
        #self.label_overall_filesdone_value = "Current source file: "+ str(self.status.finished+1) + " / " + str(self.status.getSourceFileNumber())
        progress_per_file = 10000.0 / self.status.getSourceFileNumber()
        progressOverall = int(round(self.status.finished * progress_per_file + self.status.getCurrentFinished() * progress_per_file / self.status.getCurrentSize()))

        self._page3.label_current_time.SetLabel(self.label_current_time_value)
        self._page3.gauge_current_file.SetValue(self.gauge_current_file_value)
        self._page3.label_current_percentage.SetLabel(self.label_current_percentage_value)
        self._page3.label_current_found.SetLabel(self.label_current_found_value)

    def _displayResults(self):
        elapsed = tools.processTime(self._timeAllTogether)
        self._page4._timeOverall.SetLabel("Overall time: " + elapsed[0] + ":" + elapsed[1] + ":" + elapsed[2])
        self._page4._lFilesRecovered.SetLabel("Files recovered: " + str(self.status.getOverallFound()))
        if self._page1.if_dir.GetValue() == "Working Directory":
            location_dest = tools.determineAbsPath("./")
        else:
            location_dest = tools.determineAbsPath(self._page1.if_dir.GetValue())
        self._page4._outputLocation.SetLabel("Look for your recovered files in:\n " +
                                             location_dest)

        if FESettings.getSettings().getValue("ig_delete_imagefile") == "yes":
            location_dest = tools.determineAbsPath( FESettings.getSettings().getValue("ig_output_dir"))
            if os.path.exists(location_dest):
                os.remove(location_dest)
                print "Image file removed."


if __name__ == "__main__":    
    app = wx.PySimpleApp()
    # load settings
    FESettings.getSettings().load()

    app._wizard = FileExtractorWizard()
    app._wizard.Destroy()
    app.MainLoop()
    
