# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:16:45 2020

@author: vsamm
"""

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
additional_modules = []

build_exe_options = {"includes": additional_modules,
                     "packages": ["numpy", "tkinter"],
                     "excludes": [''],
                     "include_files": ['roughness.ico']}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="skinfriction_2",
      version="2.0",
      description="none",
      options={"build_exe": build_exe_options},
      executables=[Executable(script="SkinFriction_Loss_2.pyw", base=base)])