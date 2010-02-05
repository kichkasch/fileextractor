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

@author: Michael Pilgermann
@contact: mailto:kichkasch@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)
"""
