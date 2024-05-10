import os
import pygame

def load_images_from_folder(folder, accept=(".png", ".jpg", ".bmp")):
    images = {}
    i = 0
    for root, dirs, files in os.walk(folder):
        current_dict = images
        
        # Get relative path from the assets folder
        relative_path = os.path.relpath(root, folder)
        
        # Split the relative path into subdirectories
        subfolders = relative_path.split(os.path.sep)
        print(subfolders)
        
        # Create nested dictionaries as needed
        for subfolder in subfolders:
            current_dict = current_dict.setdefault(subfolder, {})
        
        # Load images into the innermost dictionary
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext.lower() in accept:
                path = os.path.join(root, filename)
                img = pygame.image.load(path)

                if img.get_alpha():
                    img = img.convert_alpha()
                else:
                    img = img.convert()

                current_dict[name] = img

        print(i, root, dirs, files)
        i += 1
    return images


# Example usage:
screen = pygame.display.set_mode([64, 64])

assets_folder = "assets/images/"
image_dict = load_images_from_folder(assets_folder)
print()
print(image_dict)
print(image_dict['characters']['player_idle'])
