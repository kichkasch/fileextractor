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
def assemble(filename, distribution):
    from distutils.core import setup
    import py2exe
    import sys
    
    
    # enter the filename of your wxPython code file to compile ...
#    filename = "FileExtractorWizard.py"
#    distribution = "FileExtractorWizard"    
    
    # if run without args, build executables in quiet mode
    if len(sys.argv) == 1:
        sys.argv.append("py2exe")
        sys.argv.append("-q")
    
    class Target:
        def __init__(self, **kw):
            self.__dict__.update(kw)
            # for the versioninfo resources, edit to your needs
            self.version = "1.0.2"
            self.company_name = "No Company"
            self.copyright = "2010 Michael Pilgermann"
            self.name = distribution
    
    ################################################################
    # The manifest will be inserted as resource into your .exe.  This
    # gives the controls the Windows XP appearance (if run on XP ;-)
    #
    # Another option would be to store it in a file named
    # test_wx.exe.manifest, and copy it with the data_files option into
    # the dist-dir.
    #
    manifest_template = '''
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity
        version="5.0.0.0"
        processorArchitecture="x86"
        name="%(prog)s"
        type="win32"
    />
    <description>%(prog)s Program</description>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity
                type="win32"
                name="Microsoft.Windows.Common-Controls"
                version="6.0.0.0"
                processorArchitecture="X86"
                publicKeyToken="6595b64144ccf1df"
                language="*"
            />
        </dependentAssembly>
    </dependency>
    </assembly>
    '''
    
    RT_MANIFEST = 24
    
    # description is the versioninfo resource
    # script is the wxPython code file
    # manifest_template is the above XML code
    # distribution will be the exe filename
    # icon_resource is optional, remove any comment and give it an iconfile you have
    #   otherwise a default icon is used
    # dest_base will be the exe filename
    test_wx = Target(
        description = "FileExtractor",
        script = filename,
        other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog=distribution))],
        icon_resources = [(1, "icons/lupe.ico")],
        dest_base = distribution)
    
    ################################################################
    
    setup(
        options = {"py2exe": {"compressed": 1,
                              "optimize": 2,
                              "ascii": 1,
                              "bundle_files": 1}},
        zipfile = None,
        windows = [test_wx],
        )    
    
if __name__ == "__main__":
    #setup (console = ["FileExtractorWizard.py"])
    #setup (name = "FileExtractor", 
           #windows = [{"script":"FileExtractorWizard.py"}])

    assemble ("FileExtractorWizard.py", "FileExtractorWizard")
    assemble ("FileExtractor.py", "FileExtractor")    
