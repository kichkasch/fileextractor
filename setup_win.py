"""
setup_win.py

Setup file for Windows32 - creating an executable from all the Python sources

Don't forget to put the icons, the help zip and the dd  clone afterwards.

http://www.py2exe.org/

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@organization: Information Security Group / University of Glamorgan 
@contact: http://www.glam.ac.uk/soc/research/isrg.php
@license: GPL (General Public License)
"""

from distutils.core import setup
import py2exe

setup(windows=["fileextractor.py"])
