# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 10:57:37 2021

@author: marti
"""
import sys
import os

from numpy import (array, arange, zeros, ones, full,
                   stack, vstack, tile, concatenate,
                   shape, take, meshgrid, diff,
                   ceil, log2, isinf, dot,
                   inf, pi)

## Helper functions
def init_maps(dimensions):
    distance_map = full(dimensions, inf)
    seed_map = zeros((*dimensions,2))
    ancestor_map = zeros((*dimensions,2))
    return distance_map, seed_map,ancestor_map


def step_sequence(dimensions, algorithm):
    """Give the step-size sequence for a given JFA variant.
    
    Available variants are JFA, JFA+1, JFA+2, 1+JFA.
    (https://en.wikipedia.org/wiki/Jump_flooding_algorithm)"""
    # iteration count
    iterations = int(ceil(log2(max(dimensions)/2))) 
    
    # for spherical (dead code)
    # iterations = int(ceil(log2(max(m/2,n)))) - 1)
    
    base_sequence = [2**k for k in range(iterations,-1,-1)]
    
    if algorithm == 'JFA':
        sequence = base_sequence
    elif algorithm == 'JFA+1':
        sequence = [*base_sequence, 1]
    elif algorithm == 'JFA+2':
        sequence = [*base_sequence, 1, 1]
    elif algorithm == '1+JFA':
        sequence = [1, *base_sequence]
    else:
        raise IOError(f"Invalid argument: unknown algorithm variant name '{algorithm}'.")
    
    return sequence

def spread(seeds_coordinates,ancestors,stepsize,metric):
    """Spread seeds in 8 directions.
    
    Spreaded seeds are copies of the original seed displaced in each sky 
    direction (N, NE, E, SE, S...). one copy stays at the same position."""
    n_seeds = seeds_coordinates.shape[-1]
    new_ancestors = tile(ancestors,(1,9))
    new_seeds_coordinates = tile(seeds_coordinates,(1,9))
    n, o, p = ones((1,n_seeds)) * [[-1],[0],[1]]
    i_offset_sign = concatenate((n,n,n,o,o,o,p,p,p))
    j_offset_sign = concatenate((n,o,p,n,o,p,n,o,p))
    offset = stepsize * vstack((i_offset_sign,j_offset_sign))
    new_seeds_coordinates = metric.coordinate_wrap(new_seeds_coordinates + offset).astype(int)
    return new_seeds_coordinates, new_ancestors


def inf_mask(arr):
    return ~isinf(arr)

def voronoi(arr3, method = 'hashed'):
    m,n,p = shape(arr3)
    
    if p !=2:
        raise IOError(f'Invalid dimensions: {(n,m,p)}. Expected (_,_,2)')
    
    hash_func = lambda x:  (x * pi/2) % 1
    
    index = arr3[:,:,0] * n + arr3[:,:,1]
    hashed = hash_func(index)
    
    if method == 'index':
        return index
    elif method == 'hashed':
        return hashed
    else:
        raise IOError(f"Invalid input: unknown method '{method}'"
                      " for indexing voronoi fields."
                      " Expected 'index' or 'hashed'")


def middles(mat,axis=0):
    """Return array of middles. ex: out[0] = (in[0] + in[1]) / 2"""
    indices = arange(mat.shape[axis]-1)
    
    mids = take(mat,indices,axis) + diff(mat,axis=axis)/2
    return mids


def borders(bwimg):
    """Find center location of all edges of a black and white image."""
    height, width = shape(bwimg)
    J, I = meshgrid(range(width), range(height))
    IJ = stack((I,J),axis=2)
    h_lines = middles(IJ,axis=0).reshape((-1,2))[diff(bwimg,axis=0).ravel()!=0,:]
    v_lines = middles(IJ,axis=1).reshape((-1,2))[diff(bwimg,axis=1).ravel()!=0,:]
    lines = vstack((h_lines,v_lines)).T
    return lines

def col_to_gray(image):
    """Convert RGB or RGBA image to grayscale."""
    if len(image.shape) == 3 and image.shape[3] > 1:
        RGB_WEIGHTS = [0.2989, 0.5870, 0.1140] # Rec. 601 Color Transform
        grayscale_image = dot(image[...,:3], RGB_WEIGHTS)
        return grayscale_image
    else: 
        return image

def image_to_boolean(input_image):    
    """Convert RGB or RGBA image to grayscale."""
    arr = col_to_gray(array(input_image.convert('L')))
    return (arr - arr.min()) / (arr.max() - arr.min()) > 0.5

# def add_root_to_path():
#     dirname = os.path.dirname(os.path.realpath(__file__))
#     root_dirname = os.path.realpath(os.path.join(dirname,'..'))
#     if not(root_dirname in sys.path):
#         sys.path.append(root_dirname)