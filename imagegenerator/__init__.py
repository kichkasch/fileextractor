"""
Package for the ImageGenerator.

ImageGenerator is part of the FileExtractor as published on its website 
http://kkfileextractor.sourceforge.net. It extends FileExtractors 
capabilities by the function of creating the images from the sources.

Basically, the modules for the core, the gui and a command line interface (CLI) with their 
required modules are distinguish. For each operating system class a core has been
implemented.

Beside the integration with the FileExtractor, ImageGenerator may also be used
as StandAlone application. For this reason, both the L{ImageGenerator} module as well as the
L{ImageGeneratorCLI} module check for the main function and perform appropriate actions
to initialise the corrosponding modules.

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
