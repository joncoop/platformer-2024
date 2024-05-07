import pygame


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


# Images
''' hero '''
HERO_IMG_IDLE = 'assets/images/characters/player_idle.png'
HERO_IMG_WALK1 = 'assets/images/characters/player_walk1.png'
HERO_IMG_WALK2 = 'assets/images/characters/player_walk2.png'
HERO_IMG_JUMP = 'assets/images/characters/player_jump.png'

''' tiles '''
GRASS_IMG = 'assets/images/tiles/grass_dirt.png'
BLOCK_IMG = 'assets/images/tiles/block.png'
FLAG_IMG = 'assets/images/tiles/flag.png'
FLAGPOLE_IMG = 'assets/images/tiles/flagpole.png'

''' items '''
GEM_IMG = 'assets/images/items/gem.png'
HEART_IMG = 'assets/images/items/heart.png'

''' enemies '''
CLOUD_IMG = 'assets/images/characters/cloud.png'
SPIKEBALL_IMG1 = 'assets/images/characters/spikeball1.png'
SPIKEBALL_IMG2 = 'assets/images/characters/spikeball2.png'
SPIKEMAN_IMG1 = 'assets/images/characters/spikeman_walk1.png'
SPIKEMAN_IMG2 = 'assets/images/characters/spikeman_walk2.png'

# Sounds
JUMP_SND = 'assets/sounds/jump.wav'
GEM_SND = 'assets/sounds/collect_point.wav'

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

HERO_HEARTS = 3
HERO_SPEED = 7
HERO_JUMP_POWER = 22
HERO_ESCAPE_TIME = 30
BOUNCE_SPEED = 10

SPIKEMAN_SPEED = 2
SPIKEBALL_SPEED = 2
CLOUD_SPEED = 3

TRANSITION_TIME = 2000 # In milliseconds

# Scoring
GEM_VALUE = 10

# Gameplay settings
CONTROLS = {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'jump': pygame.K_SPACE,
}

