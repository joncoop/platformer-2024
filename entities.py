import pygame

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

# Tiles
class Platform(Entity):

    def __init__(self, world, image, loc):
        super().__init__(world, image, loc)


# Characters
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


# Enemies
class Cloud(Entity):

    def __init__(self, world, image, loc):
        super().__init__(world, image, loc)

        self.velocity.x = -1 * settings.CLOUD_SPEED

    def update(self):
        self.move_x()
        at_edge = self.check_world_edges()

        if at_edge:
            self.turn_around()


class SpikeBall(AnimatedEntity):

    def __init__(self, world, images, loc):
        super().__init__(world, images, loc)

        self.velocity.x = -1 * settings.SPIKEBALL_SPEED

    def update(self):
        self.apply_gravity()
        self.move_x()
        hit_platform_x = self.check_platforms_x()
        self.move_y()
        hit_platform_y = self.check_platforms_y()
        at_world_edge = self.check_world_edges()

        if at_world_edge or hit_platform_x:
            self.turn_around()

        if hit_platform_y:
            self.velocity.y = 0

        self.animate()


class SpikeMan(AnimatedEntity):

    def __init__(self, world, images, loc):
        super().__init__(world, images, loc)

        self.velocity.x = -1 * settings.SPIKEMAN_SPEED

    def set_image_list(self):
        if self.velocity.x > 0:
            self.images = self.world.game.spikeman_imgs_right
        else:
            self.images = self.world.game.spikeman_imgs_left

    def update(self):
        self.apply_gravity()
        self.move_x()
        hit_platform_x = self.check_platforms_x()
        self.move_y()
        hit_platform_y = self.check_platforms_y()
        at_world_edge = self.check_world_edges()
        at_platform_edge = self.check_platform_edges()

        if at_world_edge or hit_platform_x or at_platform_edge:
            self.turn_around()

        if hit_platform_y:
            self.velocity.y = 0

        self.animate()


# Items
class Gem(Entity):

    def __init__(self, world, image, loc):
        super().__init__(world, image, loc)

    def apply(self, character):
        character.score += settings.GEM_VALUE


class Heart(Entity):

    def __init__(self, world, image, loc):
        super().__init__(world, image, loc)

    def apply(self, character):
        if character.hearts < character.max_hearts:
            character.hearts += 1
