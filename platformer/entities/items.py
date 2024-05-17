# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports
import settings
from .entity import AnimatedEntity, Entity
from platformer.resource_manager import ResourceManager


class Gem(Entity):

    def __init__(self, world, loc):
        resource_manager = ResourceManager()
        image = resource_manager.images['items']['gem']
        super().__init__(world, image, loc)

        self.collect_sound = resource_manager.sounds['collect_point']

    def apply(self, character):
        character.score += settings.GEM_VALUE
        self.collect_sound.play()


class Heart(Entity):

    def __init__(self, world, loc):
        resource_manager = ResourceManager()
        image = resource_manager.images['items']['heart']
        super().__init__(world, image, loc)

    def apply(self, character):
        if character.hearts < character.max_hearts:
            character.hearts += 1
