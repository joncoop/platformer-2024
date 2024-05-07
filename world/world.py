# Standard Library Imports
import csv

# Third-Party Imports
import pygame

# Local Imports
import settings
import platformer.entities


class World:
    
    def __init__(self, game, hero):
        self.filepath = 'assets/levels/map_data.csv'
        self.game = game
        self.hero = hero

        self.print_info = True # Mostly for debugging

        self.load()
        
    def load(self):
        with open(self.filepath, 'r') as file:
            reader = csv.reader(file)
            map_data = list(reader)

        # Make sprite groups
        self.players = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.width = len(map_data[0]) * settings.GRID_SIZE
        self.height = len(map_data) * settings.GRID_SIZE

        for y, row in enumerate(map_data):
            for x, value in enumerate(row):
                loc = [x, y]

                if value == settings.HERO: # won't work with multiplayer game
                    self.hero.world = self
                    self.hero.move_to(loc)
                    self.players.add(self.hero)
                elif value == settings.BLOCK:
                    self.platforms.add( platformer.entities.Tile(self, self.game.block_img, loc) )
                elif value == settings.GRASS:
                    self.platforms.add( platformer.entities.Tile(self, self.game.grass_dirt_img, loc) )
                elif value == settings.CLOUD:
                    self.enemies.add( platformer.entities.Cloud(self, self.game.cloud_img, loc) )
                elif value == settings.SPIKEBALL:
                    self.enemies.add( platformer.entities.SpikeBall(self, self.game.spikeball_imgs, loc) )
                elif value == settings.SPIKEMAN:
                    self.enemies.add( platformer.entities.SpikeMan(self, self.game.spikeman_imgs_right, loc) )
                elif value == settings.GEM:
                    self.items.add( platformer.entities.Gem(self, self.game.gem_img, loc) )
                elif value == settings.HEART:
                    self.items.add( platformer.entities.Heart(self, self.game.heart_img, loc) )
                elif value == settings.FLAG:
                    if len(self.goals) == 0:
                        self.goals.add( platformer.entities.Tile(self, self.game.flag_img, loc) )
                    else:
                        self.goals.add( platformer.entities.Tile(self, self.game.flagpole_img, loc) )

        self.current_zone = None
        self.find_nearby_sprites()

        if self.print_info:
            self.print_world_info()

    def print_world_info(self):
        print(f'World dimensions in tiles: {self.width // settings.GRID_SIZE}, {self.height // settings.GRID_SIZE}')
        print(f'World dimensions in pixels: {self.width}, {self.height}')

        total_sprites = len(self.players) + len(self.platforms) + len(self.goals) + len(self.enemies) + len(self.items)
        num_enemies = len(self.enemies)
        print(f'Num sprites: {total_sprites}')
        print(f'Num enemies: {num_enemies}')

        self.print_zone()

    def print_zone(self):
        if self.print_info:
            print(f'Current zone: {self.current_zone}')

    def get_current_zone(self):
        x = self.hero.rect.centerx // settings.SCREEN_WIDTH
        y = self.hero.rect.centery // settings.SCREEN_HEIGHT

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
            # The inner_region must extend 1.5 screen widths and heights from the center.
            inner_region = pygame.rect.Rect(0, 0, 3 * settings.SCREEN_WIDTH, 3 * settings.SCREEN_HEIGHT)
            inner_region.center = self.hero.rect.center

            outer_region = inner_region.inflate(2 * settings.GRID_SIZE, 2 * settings.GRID_SIZE)

            # Things that interact with other objects should be in the inner region.
            players = self.find_sprites_in_region(self.players, inner_region)
            self.nearby_players = pygame.sprite.Group(players)

            enemies = self.find_sprites_in_region(self.enemies, inner_region)
            self.nearby_enemies = pygame.sprite.Group(enemies)

            # Things that don't interact with other objects should be in the inner region.
            platforms = self.find_sprites_in_region(self.platforms, outer_region)
            self.nearby_platforms = pygame.sprite.Group(platforms)
            
            goals = self.find_sprites_in_region(self.goals, outer_region)
            self.nearby_goals = pygame.sprite.Group(goals)
                        
            items = self.find_sprites_in_region(self.items, outer_region)
            self.nearby_items = pygame.sprite.Group(items)
            
            # Put everyone in nearby_sprites for drawing and updating.
            self.nearby_sprites = pygame.sprite.Group()
            self.nearby_sprites.add(players, platforms, goals, enemies, items)

            self.print_zone()

    def update(self):
        self.get_current_zone()
        self.find_nearby_sprites()

        for sprite in self.nearby_sprites:
            sprite.update()
