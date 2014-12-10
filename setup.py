from distutils.core import setup
from glob import glob
import py2exe

setup(console=["main.py"],
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    zipfile = None)
