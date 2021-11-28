# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 10:50:55 2021

@author: marti
"""
if __name__ == '__main__':
    import os, sys
    depth = 1
    root_folder = os.path.realpath(os.path.join(__file__,'../' * (1+depth)))
    os.chdir(root_folder)
    sys.path.append(root_folder)
    
from jumpflood.helpers import (init_maps, 
                               step_sequence, 
                               spread, 
                               inf_mask, 
                               borders, 
                               voronoi,
                               image_to_boolean)

class JumpFlood:
    def __init__(self,dimensions,seeds_ancestor,metric):
        
        self.dimensions = dimensions
        self.seeds_ancestor = seeds_ancestor
        self.metric = metric
        
        # initial seed coordinates
        self.seeds_coordinates = seeds_ancestor.astype(int)
        
        # instanciate maps used to store most promising seeds
        self.distance_map, \
        self.seed_map, \
        self.ancestor_map = init_maps(dimensions)
        
    
    @property
    def height(self):
        return self.dimensions[0]
    
    @property
    def width(self):
        return self.dimensions[1]
    
    @property
    def distance_field(self):
        return self.distance_map
    
    @property
    def voronoi_diagram(self):
        return voronoi(self.ancestor_map)
    
    def sequence(self, variant):
        return step_sequence(self.dimensions, variant)
    
    def message(self,verbose,index,end,stepsize):
        if verbose:
                print((f'Iteration: {index:2d}/{end:2d} \t'
                       f'Step size: {stepsize:5d} \t '
                       f'Active seeds: {self.seeds_coordinates.shape[1]:10d}'))
    
    def spread_seeds(self,stepsize):
        return spread(self.seeds_coordinates,
                      self.seeds_ancestor,
                      stepsize,
                      self.metric)
    
    def pin_on_map(self, seeds_candidates, candidates_ancestors):
         # calculate new distances from each seed to its ancestor
        distances = self.metric.distance(seeds_candidates, candidates_ancestors)
        
        for k, d in enumerate(distances):
            i,j = seeds_candidates[:,k]
            
            # skip seed if out of bounds
            if not(0 <= i < self.height and 0 <= j < self.width):
                continue
            
            # replace current seed on the map if better than already existing one
            if d < self.distance_map[i,j]:
                self.ancestor_map[i,j,:] = candidates_ancestors[:,k]
                self.seed_map[i,j,:] = seeds_candidates[:,k]
                self.distance_map[i,j] = d
    
    def list_from_map(self):
        # mask map where no seed has arrived yet
        seed_mask = inf_mask(self.distance_map)
        
        # extract all remaining seed from the maps
        self.seeds_coordinates = self.seed_map[seed_mask].T
        self.seeds_ancestor = self.ancestor_map[seed_mask].T
    
    def iterate(self,stepsize):
        # 1. spread seeds in all directions by a distance equal to the stepsize
        seeds_candidates, candidates_ancestors = self.spread_seeds(stepsize)
        
        # 2. pin all seeds on a 2D-map and keep only best candidates
        self.pin_on_map(seeds_candidates, candidates_ancestors)
        
        # 3. lookup all remaining seeds on the map
        self.list_from_map()
    
    def flood(self, variant = 'JFA', verbose = False):
        sequence = self.sequence(variant)
        for index, stepsize in enumerate(sequence, start=1):
            self.message(verbose, index, len(sequence), stepsize)
            self.iterate(stepsize)


class SignedJumpFlood(JumpFlood):
    def __init__(self, bool_array, metric):
        self.bool_array = bool_array
        super().__init__(bool_array.shape,borders(bool_array),metric)
    
    @classmethod
    def from_image(cls, input_image, metric):
        """Instanciate SignedJumpFlood from PIL bw image."""
        bool_array = image_to_boolean(input_image)
        return cls(bool_array, metric)
    
    @property
    def signed_distance_field(self):
        sign = (1 - 2 * self.bool_array)
        return sign * self.distance_field



def _test(input_path= './jumpflood/test/water.jpg', metric_name= 'r',variant= '1+JFA', verbose= True):
    from numpy import array, nanmax, nanmin, tanh, save
    from PIL import Image
    from tools.metricpresets import metric_from_preset
    from matplotlib import pyplot as plt

    
    ## Input loading
    
    # load input image as PIL Image
    input_image = Image.open(input_path)
    
    ## Setup available metrics
    metric = metric_from_preset(metric_name, bool_image)
    
    ## Setup initial state
    jf = SignedJumpFlood.from_image(input_image, metric)
    jf.flood(variant = variant, verbose = verbose)
    
    ## Plotting
    
    plt.figure(figsize=(20,10))
    plt.imshow(bool_image)
    # plt.plot(coast_lines[:,0],coast_lines[:,1],'xg',markersize=1)
    
    plt.figure(figsize=(20,10))
    plt.imshow(jf.distance_map/nanmax(jf.distance_map),extent=[-180,180,-90,90])
    
    
    beautyful_signed = -jf.signed_distance_field
    beautyful_signed[beautyful_signed< 0] /= -nanmin(beautyful_signed)
    beautyful_signed[beautyful_signed>=0] /=  nanmax(beautyful_signed)
    beautyful_signed = tanh(beautyful_signed * 1.5)
    
    plt.figure(figsize=(20,10))
    plt.imshow(beautyful_signed,extent=[-180,180,-90,90],
               cmap='twilight')
    
    plt.figure(figsize=(20,10))
    plt.imshow(jf.voronoi_diagram,extent=[-180,180,-90,90],cmap='hsv',
               interpolation = 'nearest')
    
    save('./jumpflood/test/signed_tst.npy',jf.signed_distance_field)
    save('./jumpflood/test/voronoi_tst.npy',jf.voronoi_diagram)

if __name__ == '__main__':
    _test('./jumpflood/test/water.jpg')


if __name__ == '__main__':
    sys.path.remove(root_folder)