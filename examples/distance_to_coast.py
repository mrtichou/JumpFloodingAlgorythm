# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 20:02:12 2021

@author: marti
"""

if __name__ == '__main__':
    import os, sys
    depth = 1
    root_folder = os.path.realpath(os.path.join(__file__,'../' * (1+depth)))
    os.chdir(root_folder)
    sys.path.append(root_folder)

from tools.metricpresets import metric_from_preset
from jumpflood.jumpflood import SignedJumpFlood

from os import path
from numpy import save

def distance_to_coast(input_path= './examples/input_files/water.jpg', 
                      metric_name= 'r',
                      variant= '1+JFA', 
                      verbose= True):
    ## Input loading
    
    # load input image as PIL Image
    input_image = Image.open(input_path)
    
    ## Setup available metrics
    metric = metric_from_preset(metric_name, dimensions= input_image.size[::-1])
    
    ## Setup initial state
    jf = SignedJumpFlood.from_image(input_image, metric)
    jf.flood(variant = variant, verbose = verbose)

    return jf

def save_distance_to_coast(input_path= './examples/input_files/water.jpg', 
                           output_folder = './examples/output_files/',
                           metric_name= 'r',
                           variant= '1+JFA', 
                           verbose= True):
    # get name of input file without extension
    file_stem = '.'.join(path.basename(input_path).split('.')[:-1])
    
    jf = distance_to_coast(input_path, metric_name, variant, verbose)
    
    outputs = dict(distance= jf.distance_field,
                   signed= jf.signed_distance_field,
                   voronoi= jf.voronoi_diagram)
    
    for map_name, map_values in outputs.items():
        filename = f'{file_stem}_{map_name}.npy'
        filepath = path.join(output_folder, filename)
        save(filepath, map_values)
   
    return jf

if __name__ == '__main__':
    from numpy import nanmax, nanmin, tanh, arange, hstack
    from PIL import Image
    from matplotlib import pyplot as plt, ticker, colors, rc
    
    font = {'family' : 'normal',
            'weight' : 'normal',
            'size'   : 18}

    rc('font', **font)
    
    stem = './examples/input_files/'
    files = ['water.jpg', 'earthspec1k.jpg', 'earthspec2k.jpg']
    
    for file in files:
        filepath = path.join(stem,file)
        jf = save_distance_to_coast(filepath)
        ## Plotting
        
        images_folder = './examples/output_files/'
        filename = '.'.join(file.split('.')[:-1])
        
        
        # plot boolean map
        boolean = jf.bool_array
        plt.figure(figsize=(20,10))
        plt.title('Input image')
        plt.imshow(boolean,
                   extent=[-180,180,-90,90],
                   cmap='bone', vmin=-0.25, vmax=1.25)
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')

        plotname = 'input'
        plt.savefig(f'{images_folder}{filename}_{plotname}.png')
        
        
        # plot distance field
        plt.figure(figsize=(20,10))
        plt.title('Distance field to nearest coastline')
        distance = jf.distance_map
        plt.imshow(distance,
                   extent=[-180,180,-90,90])
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')
        spacing = 1e6
        ticks = arange(0,distance.max(), spacing)
        cbar = plt.colorbar(ticks=ticks)
        cbar.set_label('Distance (km)', rotation=90)
        cbar.ax.set_yticklabels([f'{round(x/1e3):d}' for x in ticks]);
        
        plotname = 'distance'
        plt.savefig(f'{images_folder}{filename}_{plotname}.png')
        
    
        signed = jf.signed_distance_field
        plt.figure(figsize=(20,10))
        plt.title('Signed distance field to nearest coastline')
        plt.imshow(signed, 
                   extent=[-180,180,-90,90],
                   cmap='twilight',
                   norm= colors.TwoSlopeNorm(0.0,
                                        vmin=signed.min(),
                                        vmax=signed.max()))
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')
        pspacing = 5e5
        nspacing = 1e6
        ticks = hstack((arange(0,signed.min(), -nspacing)[::-1],
                        arange(0,signed.max(),  pspacing)[1:]))
        cbar = plt.colorbar(ticks=ticks)
        cbar.set_label('Distance (km)', rotation=90)
        cbar.ax.set_yticklabels([f'{round(x/1e3):d}' for x in ticks]);
        
        plotname = 'signed'
        plt.savefig(f'{images_folder}{filename}_{plotname}.png')
        
        plt.figure(figsize=(20,10))
        plt.title('Voronoi diagram (approximated by JFA)')
        plt.imshow(jf.voronoi_diagram,extent=[-180,180,-90,90],cmap='hsv',
                   interpolation = 'nearest')
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')
        
        plotname = 'voronoi'
        plt.savefig(f'{images_folder}{filename}_{plotname}.png')
    
if __name__ == '__main__':
    sys.path.remove(root_folder)
    # while True: sys.path.remove(root_folder)