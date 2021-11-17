# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 18:28:47 2021

@author: marti
"""
import sys, os
dirname = os.path.dirname(os.path.realpath(__file__))
root_dirname = os.path.realpath(os.path.join(dirname,'../' * 2))
sys.path.append(root_dirname)

import numpy as np
from matplotlib import pyplot as plt
from tools.metricpresets import metric_from_preset
from jumpflood.jumpflood import JumpFlood

def exact_solve(dimensions, points, metric):
    height, width = dimensions
    J, I = np.meshgrid(range(width), range(height))
    distance = np.full(dimensions,np.inf)
    for point in zip(*points):
        coord1 = np.array([point]).T
        coords2 = np.vstack((I.ravel(), J.ravel()))
        new_distance = metric.distance(coord1,coords2).reshape(dimensions)
        distance = np.min(np.stack((distance,new_distance),axis=2),axis=2)
    return distance

def generate_bool_image(dimensions,points):
    bool_image = np.full(dimensions,False)
    for point in points:
        bool_image[point] = True
    return bool_image
    
    
def single_point_test(dimensions, p1, 
                      metric_name = 'r',
                      variant = '1+JFA', 
                      verbose = False):

    # bool_image = generate_bool_image(dimensions,p1)
    
    ## Setup available metrics
    
    metric = metric_from_preset(metric_name, dimensions=dimensions)
    
    ## Setup initial state
    jf = JumpFlood(dimensions, p1 ,metric)
    jf.flood(variant = variant, verbose = verbose)
    
    jf_distance = jf.distance_field
    
    ex_distance = exact_solve(dimensions, p1,metric)
    
    # plt.figure()
    # plt.imshow(jf_distance)
    
    # plt.figure()
    # plt.imshow(ex_distance)
    
    plt.figure()
    plt.imshow(jf.voronoi_diagram,cmap = 'gist_rainbow',
               interpolation = 'nearest')
    
    plt.figure()
    plt.imshow(np.abs(ex_distance - jf_distance))
    plt.colorbar()
    plt.title(f'Error {variant}')
    
if __name__ == '__main__':
    dimensions = (60,130)
    n_pts = 100
    points = np.vstack((np.random.randint(0,dimensions[0],n_pts),
                        np.random.randint(0,dimensions[1],n_pts)))
    single_point_test(dimensions,points,
                      variant = 'JFA',
                      verbose=True,
                      metric_name = 'r')
    
    single_point_test(dimensions,points,
                      variant = 'JFA+1',
                      verbose=True,
                      metric_name = 'r')
    
    single_point_test(dimensions,points,
                      variant = 'JFA+2',
                      verbose=True,
                      metric_name = 'r')
    
    single_point_test(dimensions,points,
                      variant = '1+JFA',
                      verbose=True,
                      metric_name = 'r')
    