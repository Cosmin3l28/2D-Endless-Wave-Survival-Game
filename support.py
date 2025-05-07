from csv import reader
from os import walk
import pygame

WIDTH    = 1440	
HEIGTH   = 810
FPS      = 60
TILESIZE = 64

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            # print(row) # debug
            terrain_map.append(list(row))
        return terrain_map
    
def import_folder(path):

    surface_list = [] # list of surfaces
    for data in walk(path):
        image_files = data[2] # we get the image files from the data
        for image in image_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    
    return surface_list
