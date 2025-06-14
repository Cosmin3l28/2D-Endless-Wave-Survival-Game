import os
import pygame
import pytest
from unittest import mock

from bullet import Bullet
from enemy import Enemy
from player import Player
from weapon import Weapon
from level import Level
from tile import Tile
import support

@pytest.fixture(autouse=True)
def pygame_setup():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

class DummyLevel:
    def __init__(self):
        self.visible_sprites = mock.Mock()
        self.visible_sprites.offset = pygame.math.Vector2()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

class DummyPlayer:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.level = DummyLevel()
        self.gold = 0
        self.health = 100

def test_bullet_normalizes_direction():
    b = Bullet((0, 0), (0, 0), pygame.sprite.Group(), [], [], DummyPlayer())
    assert round(b.direction.length(), 5) == 1.0

def test_bullet_hits_obstacle_and_kills():
    obstacle = Tile((10, 0), [])
    b = Bullet((0, 0), (1, 0), pygame.sprite.Group(), [obstacle], [], DummyPlayer())
    b.update()
    assert not b.alive()

def test_player_take_damage_flags():
    player = Player((0, 0), [pygame.sprite.Group()], pygame.sprite.Group())
    player.take_damage(30)
    assert player.health == 70
    assert player.damaged is True

def test_player_dash_speed_changes():
    player = Player((0, 0), [pygame.sprite.Group()], pygame.sprite.Group())
    player.is_dashing = True
    player.dash_start_time = pygame.time.get_ticks()
    player.dash()
    assert player.speed == 16
    player.dash_start_time -= player.dash_duration + 1
    player.dash()
    assert player.is_dashing is False
    assert player.speed == 4

def test_weapon_updates_direction():
    p = DummyPlayer()
    w = Weapon(p, [pygame.sprite.Group()])
    with mock.patch('pygame.mouse.get_pos', return_value=(50, 50)):
        w.update_weapon()
    assert round(w.direction.length(), 5) == 1.0

def test_level_spawn_random_enemy(monkeypatch):
    def dummy_create_map(self):
        self.player = Player((0,0), [self.visible_sprites], self.obstacle_sprites)
    monkeypatch.setattr(Level, 'create_map', dummy_create_map)
    level = Level()
    initial = len(level.enemies)
    level.spawn_random_enemy('enemy')
    assert len(level.enemies) == initial + 1

def test_level_start_wave_calls_spawn(monkeypatch):
    calls = []
    def dummy_create_map(self):
        self.player = Player((0,0), [self.visible_sprites], self.obstacle_sprites)
    monkeypatch.setattr(Level, 'create_map', dummy_create_map)
    level = Level()
    def fake_spawn(t):
        calls.append(t)
    monkeypatch.setattr(level, 'spawn_random_enemy', fake_spawn)
    level.start_wave(2)
    assert len(calls) == 5 + (2 - 1) * 2

def test_import_csv_layout(tmp_path):
    file = tmp_path / "map.csv"
    file.write_text("1,2\n3,4")
    data = support.import_csv_layout(str(file))
    assert data == [['1','2'], ['3','4']]

def test_import_folder():
    surfaces = support.import_folder('graphics/player/down')
    assert len(surfaces) > 0

def test_player_shoot_adds_bullet(monkeypatch):
    level = DummyLevel()
    player = Player((0,0), [pygame.sprite.Group()], pygame.sprite.Group())
    player.level = level
    monkeypatch.setattr('pygame.mouse.get_pressed', lambda: (0,0,1))
    monkeypatch.setattr(pygame.time, 'get_ticks', lambda: 1000)
    player.last_shot = 0
    player.shoot()
    assert len(level.bullets) == 1