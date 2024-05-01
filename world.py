import csv
import pygame

from entities import *
from settings import *


class World:
    
    def __init__(self, game, hero):
        self.filepath = 'assets/levels/map_data.csv'
        self.game = game
        self.hero = hero

        self.print_info = True # Mostly for debugging

        self.load_level()
        
    def load_level(self):
        with open(self.filepath, 'r') as file:
            reader = csv.reader(file)
            map_data = list(reader)

        # Make sprite groups
        self.players = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.width = len(map_data[0]) * GRID_SIZE
        self.height = len(map_data) * GRID_SIZE

        for y, row in enumerate(map_data):
            for x, value in enumerate(row):
                loc = [x, y]

                if value == HERO: # won't work with multiplayer game
                    self.hero.world = self
                    self.hero.move_to(loc)
                    self.players.add(self.hero)
                elif value == BLOCK:
                    self.platforms.add( Platform(self, self.game.block_img, loc) )
                elif value == GRASS:
                    self.platforms.add( Platform(self, self.game.grass_dirt_img, loc) )
                elif value == CLOUD:
                    self.enemies.add( Cloud(self, self.game.cloud_img, loc) )
                elif value == SPIKEBALL:
                    self.enemies.add( SpikeBall(self, self.game.spikeball_img, loc) )
                elif value == SPIKEMAN:
                    self.enemies.add( SpikeMan(self, self.game.spikeman_img, loc) )
                elif value == GEM:
                    self.items.add( Gem(self, self.game.gem_img, loc) )
                elif value == HEART:
                    self.items.add( Heart(self, self.game.heart_img, loc) )
                elif value == FLAG:
                    if len(self.goals) == 0:
                        self.goals.add( Platform(self, self.game.flag_img, loc) )
                    else:
                        self.goals.add( Platform(self, self.game.flagpole_img, loc) )

        self.current_zone = None
        self.find_nearby_sprites()

        if self.print_info:
            self.print_world_info()

    def print_world_info(self):
        print(f'World dimensions in tiles: {self.width // GRID_SIZE}, {self.height // GRID_SIZE}')
        print(f'World dimensions in pixels: {self.width}, {self.height}')
        total_sprites = len(self.players) + len(self.platforms) + len(self.goals) + len(self.enemies) + len(self.items)
        num_enemies = len(self.enemies)
        print(f'Num sprites: {total_sprites}')
        print(f'Num enemies: {num_enemies}')

    def print_zone(self):
        print(f'Entered zone {self.current_zone}')

    def get_current_zone(self):
        x = self.hero.rect.centerx // WIDTH
        y = self.hero.rect.centery // HEIGHT

        return x, y
    
    def find_sprites_in_region(self, sprites, region):
        found = pygame.sprite.Group()

        for sprite in sprites:
            if sprite.rect.colliderect(region):
                found.add(sprite)

        return found

    def find_nearby_sprites(self):
        previous_zone = self.current_zone
        self.current_zone = self.get_current_zone()

        if self.current_zone != previous_zone:
            region = pygame.rect.Rect(0, 0, 3 * WIDTH, 3 * HEIGHT)
            region.center = self.hero.rect.center

            players = self.find_sprites_in_region(self.players, region)
            self.nearby_players = pygame.sprite.Group(players)
            
            platforms = self.find_sprites_in_region(self.platforms, region)
            self.nearby_platforms = pygame.sprite.Group(platforms)
            
            goals = self.find_sprites_in_region(self.goals, region)
            self.nearby_goals = pygame.sprite.Group(goals)
            
            enemies = self.find_sprites_in_region(self.enemies, region)
            self.nearby_enemies = pygame.sprite.Group(enemies)
            
            items = self.find_sprites_in_region(self.items, region)
            self.nearby_items = pygame.sprite.Group(items)
            
            self.nearby_sprites = pygame.sprite.Group()
            self.nearby_sprites.add(players, platforms, goals, enemies, items)

            if self.print_info:
                self.print_zone()

    def update(self):
        self.get_current_zone()
        self.find_nearby_sprites()

        for sprite in self.nearby_sprites:
            sprite.update()