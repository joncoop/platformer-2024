# Standard Library Imports
import math

# Third-Party Imports
import pygame

# Local Imports


class ScrollingCamera:

    def __init__(self, surface, world, target, lag=0.0):
        self.surface = surface
        self.world = world
        self.target = target # sprite object to track
        #self.lag = lag - 1
        self.lag = math.sqrt(lag) # 0 <= lag < 1, sqrt makes it more sensitive at low numbers

        self.last_position = self.target.rect.center
        self.focus = self.last_position
        self.visibile = False

    def toggle(self):
        self.visibile = not self.visibile

    def get_offsets(self):
        #x, y = self.target.rect.center
        x, y = self.focus

        screen_width = self.surface.get_width()
        screen_height = self.surface.get_height()

        if x < screen_width // 2:
            offset_x = 0
        elif x > self.world.width - screen_width // 2:
            offset_x = self.world.width - screen_width
        else:
            offset_x = x - screen_width // 2

        if y < screen_height // 2:
            offset_y = 0
        elif y  > self.world.height - screen_height // 2:
            offset_y = self.world.height - screen_height
        else:
            offset_y = y - screen_height // 2
            
        return offset_x, offset_y
        
    def draw(self, surface):
        if self.visibile:
            offset_x, offset_y = self.get_offsets()
            screen_width = self.surface.get_width()
            screen_height = self.surface.get_height()

            # Midlines of screen
            pygame.draw.line(surface, pygame.Color('lightgray'), [screen_width // 2, 0], [screen_width // 2, screen_height], 1)
            pygame.draw.line(surface, pygame.Color('lightgray'), [0, screen_height // 2], [screen_width , screen_height // 2], 1)
            
            # Target rect
            top = self.target.rect.y - offset_y
            left = self.target.rect.x - offset_x
            width = self.target.rect.width
            height = self.target.rect.height

            offset_target_rect = pygame.rect.RectType(left, top, width, height)
            pygame.draw.rect(surface, pygame.Color('red'), offset_target_rect, 1)

            # Crosshairs at focus
            x, y = self.focus
            x -= offset_x
            y -= offset_y

            pygame.draw.line(surface, pygame.Color('red'), [x, y - 10], [x, y + 10], 1)
            pygame.draw.line(surface, pygame.Color('red'), [x - 10, y], [x + 10, y], 1)

    def snap_to_target(self):
        self.focus = self.target.rect.center
        self.last_position = self.focus

    def update(self):
        dx = self.target.rect.centerx - self.last_position[0]
        dy = self.target.rect.centery - self.last_position[1]

        between_x = self.target.rect.centerx - dx * self.lag
        between_y = self.target.rect.centery - dy * self.lag

        self.focus = between_x, between_y
        self.last_position = self.focus
        