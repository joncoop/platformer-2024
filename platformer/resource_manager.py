# Standard Library Imports
import os

# Third-Party Imports
import pygame

# Local Imports


class ResourceManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ResourceManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Avoid reinitializing
            self.initialized = True
            
            self.images = {}
            self.sounds = {}
            self.music = {}
            self.fonts = {}

    def load_image(self, path):
        image = pygame.image.load(path)

        if image.get_alpha():
            image = image.convert_alpha()
        else:
            image = image.convert()

        return image


    def flip_img_x(image):
        return pygame.transform.flip(image, True, False)


    def flip_img_y(image):
        return pygame.transform.flip(image, False, True)


    def load_sound(self, path):
        return pygame.mixer.Sound(path)


    def load_font(self, path):
        pass


    def has_files_of_type(self, filenames, accept):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            
            if ext.lower() in accept:
                return True
        
        return False

    def load_all_images(self, folder, accept=(".png", ".jpg", ".bmp")):
        for root, dirs, filenames in os.walk(folder):
            current_dict = self.images

            # Get relative path from the assets folder
            relative_path = os.path.relpath(root, folder)
            
            # Split the relative path into subdirectories
            subfolders = relative_path.split(os.path.sep)
            
            # Create nested dictionaries as needed
            for subfolder in subfolders:
                if self.has_files_of_type(filenames, accept):
                    current_dict = current_dict.setdefault(subfolder, {})

            # Load images into the innermost dictionary
            for filename in filenames:
                name, ext = os.path.splitext(filename)

                if ext.lower() in accept:
                    path = os.path.join(root, filename)
                    current_dict[name] = self.load_image(path)

