"""
Based on an idea from 
https://github.com/Mekire/cabbages-and-kings/blob/master/data/tools.py
"""


import os
import pygame


def load_image(path):
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


def load_sound(path):
    return pygame.mixer.Sound(path)


def load_font(path):
    pass


def has_files_of_type(filenames, accept):
    for filename in filenames:
        name, ext = os.path.splitext(filename)
        
        if ext.lower() in accept:
            return True
    
    return False


def load_all_images(folder, accept=(".png", ".jpg", ".bmp")):
    images = {}

    for root, dirs, filenames in os.walk(folder):
        current_dict = images

        # Get relative path from the assets folder
        relative_path = os.path.relpath(root, folder)
        
        # Split the relative path into subdirectories
        subfolders = relative_path.split(os.path.sep)
        
        # Create nested dictionaries as needed
        for subfolder in subfolders:
            if has_files_of_type(filenames, accept):
                current_dict = current_dict.setdefault(subfolder, {})

        # Load images into the innermost dictionary
        for filename in filenames:
            name, ext = os.path.splitext(filename)

            if ext.lower() in accept:
                path = os.path.join(root, filename)
                current_dict[name] = load_image(path)

    return images
