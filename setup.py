from distutils.core import setup
from glob import glob
import py2exe

setup(console = [
        {
            "script": "main.py",
            "icon_resources": [(0, "icon.ico")]
        }
    ],
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    zipfile = None)
