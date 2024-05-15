#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 19:17:04 2024

@author: jonny
"""
# from datetime import datetime
from datetime import datetime, timedelta, date

format_str = "%Y-%m-%d"
format_now = "%Y-%m-%d %H:%M:%S.%f"

time_now = datetime.now()
print(time_now)
index = str(time_now)

print(index[0:10])

my_date = datetime.strptime(index, format_now)

print(my_date)

