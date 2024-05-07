# Standard Library Imports


# Third-Party Imports
import pygame

# Local Imports
import settings


class Entity(pygame.sprite.Sprite):

    def __init__(self, world, image, loc=[0, 0]):
        super().__init__()

        self.world = world
        self.image = image
        self.rect = self.image.get_rect()

        self.move_to(loc)

    def move_to(self, loc):
        center_x = loc[0] * settings.GRID_SIZE + settings.GRID_SIZE // 2
        center_y = loc[1] * settings.GRID_SIZE + settings.GRID_SIZE // 2
        
        self.location = pygame.Vector2(center_x, center_y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect.center = self.location

    def apply_gravity(self):
        self.velocity.y += settings.GRAVITY
        self.velocity.y = min(self.velocity.y, settings.TERMINAL_VELOCITY)

    @property
    def on_platform(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.world.nearby_platforms, False)
        self.rect.y -= 1

        return len(hits) > 0

    def move_x(self):
        self.location.x += self.velocity.x
        self.rect.center = self.location

    def move_y(self):
        self.location.y += self.velocity.y
        self.rect.center = self.location

    def check_platforms_x(self):
        hits = pygame.sprite.spritecollide(self, self.world.nearby_platforms, False)

        for platform in hits:
            if self.velocity.x < 0:
                self.rect.left = platform.rect.right
            elif self.velocity.x > 0:
                self.rect.right = platform.rect.left

            self.location.update(self.rect.center)

        return len(hits) > 0

    def check_platforms_y(self):
        hits = pygame.sprite.spritecollide(self, self.world.nearby_platforms, False)

        for platform in hits:
            if self.velocity.y < 0:
                self.rect.top = platform.rect.bottom
            elif self.velocity.y > 0:
                self.rect.bottom = platform.rect.top

            self.location.update(self.rect.center)

        return len(hits) > 0
    
    def check_platform_edges(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.world.nearby_platforms, False)
        self.rect.y -= 1

        at_edge = True

        for platform in hits:
            if self.velocity.x < 0:
                if platform.rect.left <= self.rect.left:
                    at_edge = False
            elif self.velocity.x > 0:
                if platform.rect.right >= self.rect.right:
                    at_edge = False

        return at_edge

    def check_world_edges(self):
        at_edge = False

        if self.rect.left < 0:
            self.rect.left = 0
            at_edge = True
        elif self.rect.right > self.world.width:
            self.rect.right = self.world.width
            at_edge = True

        if at_edge:
            self.location.update(self.rect.center)
            
        return at_edge
    
    def turn_around(self):
        self.velocity.x *= -1


class AnimatedEntity(Entity):

    def __init__(self, world, images, loc=[0, 0]):        
        super().__init__(world, images[0], loc)
        
        self.images = images
        self.animation_speed = 150 # Milliseconds
        self.last_time = pygame.time.get_ticks()
        self.image_index = 0

    def set_image_list(self):
        self.images = self.images

    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_time > self.animation_speed:
            self.set_image_list()

            self.image_index += 1
            if self.image_index >= len(self.images):
                self.image_index = 0

            self.image = self.images[self.image_index]
            self.last_time = current_time
