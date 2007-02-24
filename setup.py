"""
Setup module for FileExtractor

FileExtractor

@author: Michael Pilgermann
@contact: mailto:mpilgerm@glam.ac.uk
@license: GPL (General Public License)
"""

from distutils.core import setup

if __name__ == "__main__":
    setup (
        name = "fileextractor",
        version = "1.0",
        description = "FileExtractor - recover your data",
        author = "Michael Pilgermann",
        author_email = "mpilgerm@glam.ac.uk",
        url = "http://kkfileextractor.sourceforge.net",
        package_dir = {'fileextractor': '.'},
        packages = ["fileextractor", "fileextractor.imagegenerator"]
        )
