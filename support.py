"""Support functions and constants for the game."""
import pygame
from os import walk
from csv import reader

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
        'speed': 1,
        'attack_radius': 100,
        'loot': 1,
        'resistance': 10,
        'graphic': 'graphics/enemies/enemy.png'
    },
    
    'shooter': {
        'health': 80,
        'damage': 8,
        'speed': 0.8,
        'shoot_interval': 1200,
        'loot': 2,
        'graphic': 'graphics/enemies/enemy.png'
    },

    'boss': {
        'health': 500,
        'damage': 20,
        'speed': 0.5,
        'attack_radius': 200,
        'loot': 3,
        'resistance': 20,
        'graphic': 'graphics/enemies/boss.png'
    }
}

upgrade_pool = [
            {
                'name': 'Health +20',
                'cost': 5,
                'rarity': 'common',
                'apply': lambda p: setattr(p, 'health', p.health + 20),
            },
            {
                'name': 'Damage +10',
                'cost': 6,
                'rarity': 'common',
                'apply': lambda p: setattr(p, 'damage', p.damage + 10),
            },
            {
                'name': 'Speed +0.5',
                'cost': 6,
                'rarity': 'common',
                'apply': lambda p: setattr(p, 'speed', p.speed + 0.5),
            },
            {
                'name': 'Health +50',
                'cost': 15,
                'rarity': 'rare',
                'apply': lambda p: setattr(p, 'health', p.health + 50),
            },
            {
                'name': 'Damage +25',
                'cost': 18,
                'rarity': 'rare',
                'apply': lambda p: setattr(p, 'damage', p.damage + 25),
            },
            {
                'name': 'Speed +1',
                'cost': 20,
                'rarity': 'rare',
                'apply': lambda p: setattr(p, 'speed', p.speed + 1),
            },
]


def import_csv_layout(path) -> list[list[str]]:
    """Import a CSV layout file.

    Args:
        path (str): The file path to the CSV layout.

    Returns:
        list[list[str]]: A 2D list representing the tile layout.
    """
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            # print(row) # debug
            terrain_map.append(list(row))
        return terrain_map
    
def import_folder(path) -> list[pygame.Surface]:
    """Import all images from a folder.

    Args:
        path (str): The file path to the folder.

    Returns:
        list[pygame.Surface]: A list of surfaces representing the images.
    """
    surface_list = [] # list of surfaces
    for data in walk(path):
        image_files = data[2] # we get the image files from the data
        for image in image_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    
    return surface_list
