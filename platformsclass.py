########################################
# Name: Jeffrey Igims
# Andrew Identification: jigims
# Term Project
########################################

# Description: File contains class for platforms in the game

import pygame

class Platforms(pygame.sprite.Sprite):

    # Contains data for all platforms 
    def __init__(self, width, height, coordinates):
        super().__init__()
        self.width = width
        self.height = height
        self.coordinates = coordinates
        self.image = pygame.Surface([width, height])
        self.image.fill([250, 250, 250])
        pygame.draw.rect(self.image, [0, 0, 0], [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
