# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports
import settings
from .entity import AnimatedEntity, Entity


class Hero(AnimatedEntity):

    def __init__(self, world, images, controls):
        super().__init__(world, images)
        self.controls = controls

        self.acceleration = 0.8
        self.invinciblity_time = 0
        self.hearts = settings.HERO_HEARTS
        self.max_hearts = self.hearts
        self.score = 0
        self.facing_right = True

        self.respawn_location = self.location

    @property
    def is_alive(self):
        return self.hearts > 0
    
    @property
    def reached_goal(self):
        hits = pygame.sprite.spritecollide(self, self.world.nearby_goals, False)

        return len(hits) > 0

    @property
    def can_jump(self):
        return self.on_platform   

    # Player controls
    def go_left(self):
        self.velocity.x -= self.acceleration 

        if self.velocity.x < -1 * settings.HERO_SPEED:
            self.velocity.x = -1 * settings.HERO_SPEED

        self.facing_right = False
    
    def go_right(self):
        self.velocity.x += self.acceleration 

        if self.velocity.x > settings.HERO_SPEED:
            self.velocity.x = settings.HERO_SPEED

        self.facing_right = True

    def stop(self):
        if self.velocity.x < -1 * self.acceleration:
            self.velocity.x += self.acceleration 
        elif self.velocity.x > self.acceleration:
            self.velocity.x -= self.acceleration
        else:
            self.velocity.x = 0

    def jump(self):
        if self.can_jump:
            self.velocity.y = -1 * settings.HERO_JUMP_POWER

    def act(self, events, pressed):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls['jump']:
                    self.jump()

        if pressed[self.controls['left']]:
            self.go_left()
        elif pressed[self.controls['right']]:
            self.go_right()
        else:
            self.stop()

    # Automated methods
    def check_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.world.nearby_enemies, False)

        if self.invinciblity_time == 0:
            for enemy in hits:
                self.hearts -= 1
                self.invinciblity_time = settings.HERO_ESCAPE_TIME

                dx = self.location.x - enemy.location.x
                dy = self.location.y - enemy.location.y
                bounce_velocity = pygame.Vector2(dx, dy)
                bounce_velocity.scale_to_length(settings.BOUNCE_SPEED)
                self.velocity = bounce_velocity

        elif self.invinciblity_time > 0:
            self.invinciblity_time -= 1

    def check_items(self):
        hits = pygame.sprite.spritecollide(self, self.world.nearby_items, True)

        for item in hits:
            item.apply(self)
    
    def set_image_list(self):
        if self.facing_right:
            if self.on_platform:
                if self.velocity.x == 0:
                    self.images = self.world.game.hero_imgs_idle_right
                else:
                    self.images = self.world.game.hero_imgs_walk_right
            else:
                self.images = self.world.game.hero_imgs_jump_right
        else:
            if self.on_platform:
                if self.velocity.x == 0:
                    self.images = self.world.game.hero_imgs_idle_left
                else:
                    self.images = self.world.game.hero_imgs_walk_left
            else:
                self.images = self.world.game.hero_imgs_jump_left

    def update(self):
        self.apply_gravity()
        self.check_enemies() # put before movement to override user input and gravity for bounce off enemy
        self.check_items() # put here in case an item is intended to affect player movement
        
        self.move_x()
        hit_platform_x = self.check_platforms_x()
        self.move_y()
        hit_platform_y = self.check_platforms_y()
        at_world_edge = self.check_world_edges()

        if hit_platform_x or at_world_edge:
            self.velocity.x = 0

        if hit_platform_y:
            self.velocity.y = 0

        self.animate()
