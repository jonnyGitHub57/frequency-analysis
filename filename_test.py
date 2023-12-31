#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 04:44:06 2023

@author: jonny
"""

import easygui
import re
import os




source_file = easygui.fileopenbox()
"""
Strip away the path and search the xml-file for previous use of
the selected file (name).
"""
file_name, file_ext = os.path.splitext(source_file)
full_path, file_name = os.path.split(source_file)
head, category = os.path.split(full_path)

if file_ext.lower() == '.txt' or file_ext.lower == '.pdf':
    print('The source file will be analysed by Stanza')
elif file_ext.lower() == '.pdf':
    print('The pdf-file will have its text extracted')
else:
    print('The file extension indicates an unsupported file format')
    print('If the file is a text or pdf file, rename it and re-try')
