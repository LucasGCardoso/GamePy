import pygame


class SpriteSheet():

    def __init__(self, img):
        self.sheet = img

    def get_image(self, frame, width, height, scale, colour):
        # Creates an empty surface that will contain the image.
        img = pygame.Surface((width, height)).convert_alpha()
        # Takes the specified frame from the sheet and puts into the surface created before.
        img.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        # Scales up the image.
        img = pygame.transform.scale(img, (width*scale, height*scale))
        # Removes the black image background.
        img.set_colorkey(colour)
        return img
