# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 15:56:57 2021

@author: marti

For image metrics, coordinates are supposed to be positive integers

"""
# import numpy as np
from numpy import array
from numpy import pi, cos, sin, arcsin, sqrt, abs as npabs, subtract
from numpy.linalg import norm


class ImageMetric:
    def __init__(self):
        pass
    
    def distance(self,coord_1,coord_2):
        pass
    
    def coordinate_wrap(self,coord):
        pass


class EuclidianMetric(ImageMetric):
    def __init__(self,scale=1):
        self.scale = scale
        
    def distance(self,coord_1,coord_2):
        return norm(subtract(coord_1, coord_2),axis=0)
    
    def coordinate_wrap(self,coord,**kwargs):
        return coord
    
class SphericalMetric(ImageMetric):
    """Metric associated to a sphere (haversine metric). 
        
    Used for calculating voronoi or distance fields for equirectangular maps."""
    
    def __init__(self,radius,dimensions):
        self.radius = radius
        self.dimensions = dimensions
    
    def distance(self,coord_1,coord_2,**kwargs):
        lon1, lat1 = self.to_lon_lat(coord_1)
        lon2, lat2 = self.to_lon_lat(coord_2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2.0)**2
        c = 2 * arcsin(sqrt(a))
        dist = c * self.radius
        return dist
    
    def coordinate_wrap(self,coord):
        i,j = coord
        height, width = self.dimensions
        reflect = (i // height) % 2 == 1
        new_i = height - npabs(height - (i % (2 * height)))
        new_j = (j + reflect * width / 2) % width
        
        new_coord = array([new_i,new_j], like=coord)
        
        return new_coord
    
    def to_lon_lat(self, coord):
        """Converts coordinates into a custom longitude and latitude coordinate system."""
        lon = 2 * pi * (coord[1] / self.dimensions[1] - 1/2)
        lat =    -pi * (coord[0] / self.dimensions[0] - 1/2)
        return lon, lat
    
    
if __name__ == '__main__':
    # from matplotlib import pyplot as plt
    # from PIL import Image
    # water_image = Image.open(r"./input/water.jpg")
    # land_map = 1-array(water_image.convert('L'))/255 > 0.5
    # p1 = (10,30)
    # plt.figure(figsize=(20,10))
    # plt.imshow(land_map)
    # plt.plot(p1[0],p1[1],'xg',markersize=10)
    # print(land_map.shape)
    

    # plt.gca().invert_yaxis()

    import numpy as np
    from matplotlib import pyplot as plt
    dimensions = (6,13)
    p1 = np.array([[5,1.5]]).T
    coords = p1 + np.tile(np.arange(0,13,0.1),(2,1))
    m = SphericalMetric(1,dimensions)
    plt.plot(*m.coordinate_wrap(coords)[::-1],'-x')
    plt.gca().invert_yaxis()
    