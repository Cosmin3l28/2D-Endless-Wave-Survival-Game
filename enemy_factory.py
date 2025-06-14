"""Factory function to create enemy instances."""
from enemy import Enemy

def create_enemy(enemy_type, pos, **kwargs):
    """Factory function to create an enemy instance."""
    groups = kwargs.get('groups', [])
    obstacle_sprites = kwargs.get('obstacle_sprites')
    player = kwargs.get('player')
    bullet_group = kwargs.get('bullet_group')
    return Enemy(enemy_type, pos, groups, obstacle_sprites, player, bullet_group)
