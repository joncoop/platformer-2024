# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports



# Window settings
GRID_SIZE = 64
SCREEN_WIDTH = 16 * GRID_SIZE
SCREEN_HEIGHT = 9 * GRID_SIZE
TITLE = "My Awesome Game"
FPS = 60


# Define colors
SKY_BLUE = (135, 200, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Fonts
PRIMARY_FONT = 'assets/fonts/Dinomouse-Regular.otf'
SECONDARY_FONT = 'assets/fonts/Dinomouse-Regular.otf'


# Music
TITLE_MUSIC = 'assets/music/calm_happy.ogg'
MAIN_THEME = 'assets/music/cooking_mania.wav'


# Levels
STARTING_LEVEL = 1

LEVELS = ['assets/levels/map_data.csv',
          'assets/levels/map_data.csv',
          'assets/levels/map_data.csv']


# Entity types
HERO = '0'
GRASS = '1'
BLOCK = '2'
FLAG = 'F'
CLOUD = 'C'
SPIKEBALL = 'B'
SPIKEMAN = 'M'
GEM = 'G'
HEART = 'H'


# Stages
START = 0
PLAYING = 1
PAUSE = 2
LEVEL_COMPLETE = 3
WIN = 4
LOSE = 5


# Physics
GRAVITY = 1.0
TERMINAL_VELOCITY = 20


# Hero attributes
HERO_HEARTS = 3
HERO_SPEED = 7
HERO_JUMP_POWER = 22
HERO_ESCAPE_TIME = 30
BOUNCE_SPEED = 10


# Enemy attributes
SPIKEMAN_SPEED = 2
SPIKEBALL_SPEED = 2
CLOUD_SPEED = 3


# Scoring
GEM_VALUE = 10


# Gameplay settings
CONTROLS = {
        'left': pygame.K_a,
        'right': pygame.K_d,
        'jump': pygame.K_SPACE,
}

LEVEL_TRANSITION_TIME = 2000 # In milliseconds
