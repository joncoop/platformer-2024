# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports
import settings

import platformer.camera
import platformer.overlays
import platformer.entities
import platformer.world


# Main game class 
class Game:

    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()

        self.screen = pygame.display.set_mode([settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT])
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.load_assets()
        self.make_overlays()
        self.new_game()

    def load_assets(self):
        ''' platform tiles '''
        self.grass_dirt_img = pygame.image.load(settings.GRASS_IMG).convert_alpha()
        self.block_img = pygame.image.load(settings.BLOCK_IMG).convert_alpha()
        
        ''' hero '''
        self.hero_images = {}
        for key, paths in settings.HERO_IMGS.items():
            self.hero_images[key] = [pygame.image.load(path).convert_alpha() for path in paths]

        self.hero_images['idle_left'] = [pygame.transform.flip(image, True, False) for image in self.hero_images['idle_right']]
        self.hero_images['walk_left'] = [pygame.transform.flip(image, True, False) for image in self.hero_images['walk_right']]
        self.hero_images['jump_left'] = [pygame.transform.flip(image, True, False) for image in self.hero_images['jump_right']]

        ''' enemies '''
        self.cloud_img = pygame.image.load(settings.CLOUD_IMG).convert_alpha()

        self.spikeball_imgs = {}
        for key, paths in settings.SPIKEBALL_IMGS.items():
            self.spikeball_imgs[key] = [pygame.image.load(path).convert_alpha() for path in paths]
        
        self.spikeman_imgs = {}
        for key, paths in settings.SPIKEMAN_IMGS.items():
            self.spikeman_imgs[key] = [pygame.image.load(path).convert_alpha() for path in paths]
        
        self.spikeman_imgs['walk_left'] = [pygame.transform.flip(image, True, False) for image in self.spikeman_imgs['walk_right']]    

        ''' items '''
        self.gem_img = pygame.image.load(settings.GEM_IMG).convert_alpha()
        self.heart_img = pygame.image.load(settings.HEART_IMG).convert_alpha()
        
        ''' goals '''
        self.flag_img = pygame.image.load(settings.FLAG_IMG).convert_alpha()
        self.flagpole_img = pygame.image.load(settings.FLAGPOLE_IMG).convert_alpha()

    def make_overlays(self):
        self.title_screen = platformer.overlays.TitleScreen(self)
        self.win_screen = platformer.overlays.WinScreen(self)
        self.lose_screen = platformer.overlays.LoseScreen(self)
        self.level_complete_screen = platformer.overlays.LevelCompleteScreen(self)
        self.pause_screen = platformer.overlays.PauseScreen(self)
        self.hud = platformer.overlays.HUD(self)
        self.grid = platformer.overlays.Grid(self)
        
    def new_game(self):
        # Make the hero here so it persists across levels
        self.hero = platformer.entities.Hero(None, self.hero_images, settings.CONTROLS)

        # Go to first level
        self.status = settings.START
        self.level = settings.STARTING_LEVEL
        self.world = platformer.world.World(self, self.hero)
        self.current_zone = None

        # maybe move this?
        self.camera = platformer.camera.ScrollingCamera(self.screen, self.world, self.hero, 0.9)

    def start_level(self):
        self.status = settings.PLAYING

    def toggle_pause(self):
        if self.status == settings.PLAYING:
            self.status = settings.PAUSE
        elif self.status == settings.PAUSE:
            self.status = settings.PLAYING

    def complete_level(self):
        self.status = settings.LEVEL_COMPLETE

    def advance(self):
        self.level += 1
        self.world = platformer.world.World(self, self.hero)
        self.start_level()

    def win(self):
        self.status = settings.WIN

    def lose(self):
        self.status = settings.LOSE

    def check_status(self):
        if self.status == settings.PLAYING:
            if self.hero.reached_goal:
                self.complete_level()
                self.level_complete_time = pygame.time.get_ticks()
            elif not self.hero.is_alive:
                self.lose()

        elif self.status == settings.LEVEL_COMPLETE:
            current_time = pygame.time.get_ticks()

            if current_time - self.level_complete_time > settings.LEVEL_TRANSITION_TIME:
                if self.level < len(settings.LEVELS):
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
                if self.status == settings.START:
                    if event.key == pygame.K_SPACE:
                        self.start_level() 
                        processed = True
                elif self.status in [settings.WIN, settings.LOSE]:
                    if event.key == pygame.K_r:
                        self.new_game()
                        processed = True
                elif self.status in [settings.PLAYING, settings.PAUSE]:
                    if event.key == pygame.K_p:
                        self.toggle_pause() 
                        processed = True

                # for world editing
                if event.key == pygame.K_g:
                    self.grid.toggle()
                    processed = True
                elif event.key == pygame.K_c:
                    self.camera.toggle()
                    processed = True

            if not processed:
                filtered_events.append(event)

        for player in self.world.players:
            player.act(filtered_events, pressed)
        
    def update(self):
        if self.status == settings.PLAYING:
            self.world.update()

        self.camera.update()
        self.check_status()
    
    def render(self):
        self.screen.fill(settings.SKY_BLUE)
        
        offset_x, offset_y = self.camera.get_offsets()

        for sprite in self.world.nearby_sprites:
            x = sprite.rect.x - offset_x
            y = sprite.rect.y - offset_y
            self.screen.blit(sprite.image, [x, y])

        self.hud.draw(self.screen)

        if self.status == settings.START:
            self.title_screen.draw(self.screen)
        elif self.status == settings.LEVEL_COMPLETE:
            self.level_complete_screen.draw(self.screen)
        elif self.status == settings.WIN:
            self.win_screen.draw(self.screen)
        elif self.status == settings.LOSE:
            self.lose_screen.draw(self.screen)
        elif self.status == settings.PAUSE:
            self.pause_screen.draw(self.screen)

        self.camera.draw(self.screen)
        self.grid.draw(self.screen, offset_x, offset_y)

    def play(self):
        while self.running:            
            self.process_input()     
            self.update()     
            self.render()

            fps = int(self.clock.get_fps())
            pygame.display.set_caption(f'{settings.TITLE} - FPS={fps}')

            pygame.display.update()
            self.clock.tick(settings.FPS)

        pygame.quit()
