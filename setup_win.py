"""
setup_win.py

Setup file for Windows32 - creating an executable from all the Python sources

Don't forget to put the icons, the help zip and the dd  clone afterwards.

http://www.py2exe.org/

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

from distutils.core import setup
import py2exe

setup(windows=["fileextractor.py"])
