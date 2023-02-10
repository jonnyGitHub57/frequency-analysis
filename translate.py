# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 17:59:30 2020

@author: jonny
"""

from Verbs import Verb

# Debug variables to mimit 'conditional' compile macros
DebugMode= False
DebugPrints= 0

# Initialize family members and set their weight, length and target weight
verb_data = Verb('Nederlaands')

verb_data.Count_verbs()
print('Hello world')