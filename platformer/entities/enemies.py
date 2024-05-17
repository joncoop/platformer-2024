# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports
import settings
from .entity import AnimatedEntity, Entity
from platformer.resource_manager import ResourceManager


# Enemies
class Cloud(Entity):

    def __init__(self, world, loc):
        self.resource_manager = ResourceManager()
        image = self.resource_manager.images['characters']['cloud']

        super().__init__(world, image, loc)

        self.velocity.x = -1 * settings.CLOUD_SPEED

    def update(self):
        self.move_x()
        at_edge = self.check_world_edges()

        if at_edge:
            self.turn_around()


class SpikeBall(AnimatedEntity):

    def __init__(self, world, loc):
        self.resource_manager = ResourceManager()
        super().__init__(world, self.build_animation(), loc)

        self.velocity.x = -1 * settings.SPIKEBALL_SPEED

    def build_animation(self):
        images = {'rolling': [self.resource_manager.images['characters']['spikeball1'], self.resource_manager.images['characters']['spikeball2']]}

        return images
    
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

    def __init__(self, world, loc):
        self.resource_manager = ResourceManager()
        super().__init__(world, self.build_animation(), loc)

        self.velocity.x = -1 * settings.SPIKEMAN_SPEED

    def build_animation(self):
        images = {'walk_right': [self.resource_manager.images['characters']['spikeman_walk1'], self.resource_manager.images['characters']['spikeman_walk2']]}
        images['walk_left'] = [pygame.transform.flip(image, True, False) for image in images['walk_right']]

        return images
    
    def set_image_list(self):
        if self.velocity.x > 0:
            self.current_image_list = self.images['walk_right']
        else:
            self.current_image_list = self.images['walk_left']

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
