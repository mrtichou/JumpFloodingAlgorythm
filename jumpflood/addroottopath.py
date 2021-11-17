# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 15:55:44 2021

@author: marti
"""
import os, sys

DEPTH = 1 
root = os.path.realpath(__file__ + '/..' * (DEPTH + 1))
if root not in [os.path.realpath(p) for p in sys.path]:
    sys.path.append(root)
    print(f"{root} added to sys.path")
else:
    print(f"{root} already in sys.path")
