# Imports
import csv
import pygame

from entities import *
from overlays import *
from settings import *
from world import *


# Main game class 
class Game:

    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()

        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.load_assets()
        self.make_overlays()
        self.new_game()

    def load_assets(self):
        self.hero_img = pygame.image.load(HERO_IMG).convert_alpha()

        self.grass_dirt_img = pygame.image.load(GRASS_IMG).convert_alpha()
        self.block_img = pygame.image.load(BLOCK_IMG).convert_alpha()

        self.cloud_img = pygame.image.load(CLOUD_IMG).convert_alpha()
        self.spikeball_img = pygame.image.load(SPIKEBALL_IMG).convert_alpha()
        self.spikeman_img = pygame.image.load(SPIKEMAN_IMG).convert_alpha()

        self.gem_img = pygame.image.load(GEM_IMG).convert_alpha()
        self.heart_img = pygame.image.load(HEART_IMG).convert_alpha()
        
        self.flag_img = pygame.image.load(FLAG_IMG).convert_alpha()
        self.flagpole_img = pygame.image.load(FLAGPOLE_IMG).convert_alpha()

    def make_overlays(self):
        self.title_screen = TitleScreen(self)
        self.win_screen = WinScreen(self)
        self.lose_screen = LoseScreen(self)
        self.level_complete_screen = LevelCompleteScreen(self)
        self.pause_screen = PauseScreen(self)
        self.hud = HUD(self)
        self.grid = Grid(self)
        
    def new_game(self):
        # Make the hero here so it persists across levels
        self.hero = Hero(None, self.hero_img, CONTROLS)

        # Go to first level
        self.status = START
        self.level = STARTING_LEVEL
        self.world = World(self, self.hero)
        self.current_zone = None

    def start_level(self):
        self.status = PLAYING

    def toggle_pause(self):
        if self.status == PLAYING:
            self.status = PAUSE
        elif self.status == PAUSE:
            self.status = PLAYING

    def complete_level(self):
        self.status = LEVEL_COMPLETE

    def advance(self):
        self.level += 1
        self.world = World(self, self.hero)
        self.start_level()

    def win(self):
        self.status = WIN

    def lose(self):
        self.status = LOSE

    def check_status(self):
        if self.status == PLAYING:
            if self.hero.reached_goal:
                self.complete_level()
                self.level_complete_time = pygame.time.get_ticks()
            elif not self.hero.is_alive:
                self.lose()

        elif self.status == LEVEL_COMPLETE:
            current_time = pygame.time.get_ticks()

            if current_time - self.level_complete_time > TRANSITION_TIME:
                if self.level < len(LEVELS):
                    self.advance()
                else:
                    self.win()

    def process_input(self):
        filtered_events = []
        pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            processed = False

            if event.type == pygame.QUIT:
                self.running = False
                processed = True

            elif event.type == pygame.KEYDOWN:
                if self.status == START:
                    if event.key == pygame.K_SPACE:
                        self.start_level() 
                        processed = True
                elif self.status in [WIN, LOSE]:
                    if event.key == pygame.K_r:
                        self.new_game()
                        processed = True
                elif self.status in [PLAYING, PAUSE]:
                    if event.key == pygame.K_p:
                        self.toggle_pause() 
                        processed = True

                # for world editing
                if event.key == pygame.K_g:
                    self.grid.toggle()
                    processed = True

            if not processed:
                filtered_events.append(event)

        for player in self.world.players:
            player.act(filtered_events, pressed)
        
    def update(self):
        if self.status == PLAYING:
            self.world.update()

        self.check_status()

    def get_offsets(self):
        if self.hero.rect.centerx < WIDTH // 2:
            offset_x = 0
        elif self.hero.rect.centerx > self.world.width - WIDTH // 2:
            offset_x = self.world.width - WIDTH
        else:
            offset_x = self.hero.rect.centerx - WIDTH // 2

        if self.hero.rect.centery < HEIGHT // 2:
            offset_y = 0
        elif self.hero.rect.centery > self.world.height - HEIGHT // 2:
            offset_y = self.world.height - HEIGHT
        else:
            offset_y = self.hero.rect.centery - HEIGHT // 2

        return offset_x, offset_y
    
    def render(self):
        self.screen.fill(SKY_BLUE)
        
        offset_x, offset_y = self.get_offsets()

        for sprite in self.world.nearby_sprites:
            x = sprite.rect.x - offset_x
            y = sprite.rect.y - offset_y
            self.screen.blit(sprite.image, [x, y])

        self.hud.draw(self.screen)

        if self.status == START:
            self.title_screen.draw(self.screen)
        elif self.status == LEVEL_COMPLETE:
            self.level_complete_screen.draw(self.screen)
        elif self.status == WIN:
            self.win_screen.draw(self.screen)
        elif self.status == LOSE:
            self.lose_screen.draw(self.screen)
        elif self.status == PAUSE:
            self.pause_screen.draw(self.screen)

        self.grid.draw(self.screen, offset_x, offset_y)

    def play(self):
        while self.running:            
            self.process_input()     
            self.update()     
            self.render()

            fps = int(self.clock.get_fps())
            pygame.display.set_caption(f'{TITLE} - FPS={fps}')

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
