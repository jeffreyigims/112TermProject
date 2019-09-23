########################################
# Name: Jeffrey Igims
# Andrew Identification: jigims
# Term Project
########################################

# Description: File contains class for medical kits in the game

import pygame
import random

class Kit(pygame.sprite.Sprite):

    # Contains data for medical kits
    def __init__(self, height, width):
       super().__init__()
       self.kitWidth = 70
       self.kitHeight = 70
       # Picture From http://www.stickpng.com/img/miscellaneous/first-aid-kits/green-first-aid-kit-box
       self.image = Kit.loadImage(self, "medicalkit.png")
       self.rect = self.image.get_rect()
       self.rect.x = random.randint(0, width - self.kitWidth)
       self.rect.y = random.randint(0, height - self.kitHeight - 100)

    # Loads and scales an image to be used
    def loadImage(self, image):
        image = pygame.image.load(image).convert_alpha()
        image = pygame.transform.scale(image, (self.kitWidth, self.kitHeight))
        return image
