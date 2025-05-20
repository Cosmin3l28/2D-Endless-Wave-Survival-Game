from csv import reader
from os import walk
import pygame

WIDTH    = 1440	
HEIGHT  = 810
FPS      = 60
TILESIZE = 64

weapon_data = {
    'AK-47': {
        'fire-rate': 200,
        'damage': 20,
        'graphic': 'graphics/weapons/AK.png'
    },
    'GLOCK': {
        'cooldown': 50,
        'damage': 15,
        'graphic': 'graphics/weapons/GLOCK.png'
    },
    'SHOTGUN': {
        'cooldown': 10,
        'damage': 400,
        'graphic': 'graphics/weapons/SHOTGUN.png'
    }
}

moster_data = {
    'enemy': {
        'health': 100,
        'damage': 10,
        'speed': 2,
        'attack_radius': 100,
        'loot': 1,
        'resistance': 10,
        'graphic': 'graphics/enemies/enemy.png'
    },
    'boss': {
        'health': 500,
        'damage': 20,
        'speed': 1,
        'attack_radius': 200,
        'loot': 3,
        'resistance': 20,
        'graphic': 'graphics/enemies/boss.png'
    }
}


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
