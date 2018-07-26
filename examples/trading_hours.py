#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 20:32:04 2018

@author: pablo
"""

import datetime
from os import environ

print(datetime.datetime.now().hour)
print(datetime.datetime.now().minute)

print(datetime.datetime.now())

print(environ.get('RH_USER'))
print(environ.get('RH_PASSWORD'))
