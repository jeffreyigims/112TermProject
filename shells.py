########################################
# Name: Jeffrey Igims
# Andrew Identification: jigims
# Term Project
########################################

# Description: File contains class for shells in the game

import pygame
import random

class Shell(pygame.sprite.Sprite):

    # Contains data for shells
    def __init__(self, height, width):
       super().__init__()
       self.shellWidth = 30
       self.shellHeight = 30
       # Picture From https://www.mariowiki.com/Red_Shell
       self.image = Shell.loadImage(self, "shell.png")
       self.rect = self.image.get_rect()
       self.rect.centerx = random.randint(0, width - self.shellWidth)
       self.rect.y = random.randint(0, height - self.shellHeight - 100)
       self.shellThrown = False
       self.shellSpeed = 10
       self.shellTaken = False
       self.owner = None

    # Loads and scales an image to be used
    def loadImage(self, image):
        image = pygame.image.load(image).convert_alpha()
        image = pygame.transform.scale(image, (self.shellWidth, self.shellHeight))
        return image

    # Throws shell
    def throwShell(self):
        self.shellThrown = True

    # Updates shell
    def update(self, coordinatesFirst, coordinatesSecond):
        if(self.owner == None):
            return
        elif(self.owner == "first"):
            coordinatesPlayer = coordinatesFirst
            coordinatesOpposing = coordinatesSecond
        else:
            coordinatesPlayer = coordinatesSecond
            coordinatesOpposing = coordinatesFirst
        if(self.shellTaken == True):
            self.rect.x = coordinatesPlayer[0] + 35
            self.rect.y = coordinatesPlayer[1] + 45
        if(self.shellThrown):
            if(self.rect.x < coordinatesOpposing[0] + 5 and self.rect.x > coordinatesOpposing[0] - 5):
                pass
            else:
                if(self.rect.x < coordinatesOpposing[0]):
                    self.rect.x += self.shellSpeed
                elif(self.rect.x > coordinatesOpposing[0]):
                    self.rect.x -= self.shellSpeed
            if(self.rect.y < coordinatesOpposing[1] + 20 and self.rect.y > coordinatesOpposing[1] - 20):
                pass
            else:
                if(self.rect.y < coordinatesOpposing[1]):
                    self.rect.y += self.shellSpeed
                elif(self.rect.y > coordinatesOpposing[1]):
                    self.rect.y -= self.shellSpeed
