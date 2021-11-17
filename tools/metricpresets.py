# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 14:30:13 2021

@author: marti
"""

from .constants import EARTH_RADIUS
# import constants as c
from .metrics import EuclidianMetric, SphericalMetric

from inspect import getfullargspec as fargspec

# longname | shortname | Class | defaultarguments
presets = []
presets.append(['euclidian','e',EuclidianMetric, {'scale': 1}])
presets.append(['earth','r',SphericalMetric, {'radius': EARTH_RADIUS}])

LONG, SHORT, CLASS, DEFARGS = range(4)

def find_preset(metric_name):
    for line in range(len(presets)):
        for column in [LONG, SHORT]:
            if presets[line][column] == metric_name:
                return line, presets[line]
    metric_help_msg = ', '.join([f'{ps[1]} [{ps[0]}]' for ps in presets])
    raise IOError(f"Invalid argument: unknown metric name '{metric_name}'. Choose among: {metric_help_msg}")

def metric_from_preset(metric_name, image=None, dimensions=None):
    _, preset = find_preset(metric_name)
    if dimensions == None:
        dimensions = image.shape
    metric_class = preset[CLASS]
    default_args = preset[DEFARGS]
    all_arguments = {**default_args,'dimensions':dimensions}
    required_args = fargspec(metric_class.__init__).args
    args = dict((k,all_arguments[k]) for k in required_args if k in all_arguments)
    metric = metric_class(**args)
    return metric


