#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 04:44:06 2023

@author: jonny
"""

import easygui
import re
import os
import ntpath



source_file = easygui.fileopenbox()
"""
Strip away the path and search the xml-file for previous use of
the selected file (name).
"""
full_path, file_name = os.path.split(source_file)
print(f'File: {os.path.basename(source_file)}')
print('Path: ', full_path)
print('File name: ', file_name)

file_name, file_ext = os.path.splitext(source_file)
print(file_ext)
print(source_file)
