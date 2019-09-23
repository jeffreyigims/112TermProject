########################################
# Name: Jeffrey Igims
# Andrew Identification: jigims
# Term Project
########################################

# Description: File contains class for players in the game

import pygame
import math

class Players(pygame.sprite.Sprite):

    # Contains data for all players
    def __init__(self):
       super().__init__()
       self.moveSpeed = 20
       self.playerWidth = 50
       self.playerHeight = 100
       self.gravity = 20
       self.gravityIncrement = 2.5

    # Updates the position of the player each time
    def update(self, keys, keysPressed, keyCode = None):
        # Called if player initiates a jump
        if(keyCode == self.keys[2]):
            Players.jump(self)
        # Responsible for player movement due to player action
        if(not Players.checkBounds(self, keysPressed, keys)):
            if(keysPressed != None):
                if(self.keys[3] in keysPressed and keysPressed[self.keys[3]] == True):
                    self.rect.x += self.moveSpeed
                if(self.keys[0] in keysPressed and keysPressed[self.keys[0]] == True):
                    self.rect.x -= self.moveSpeed
                if(self.playerState != "standing"):
                    if(self.keys[1] in keysPressed and keysPressed[self.keys[1]] == True):
                        self.rect.y += self.moveSpeed
        # Responsible for player movement due to gravity
        if(not self.isStanding or self.powerJumpUsed == True):
            if(self.jumpSpeed < 1):
                Players.simulateGravity(self)
            elif(self.jumpSpeed > 0):
                self.rect.y -= self.jumpSpeed
                self.jumpSpeed -= self.gravityIncrement
        if(self.rect.y > self.height):
            self.respawn()

    # Checks if player is tryng to move off of the screen
    def checkBounds(self, keysPressed, keys):
        jumpSpeed = abs(self.jumpSpeed)
        if(self.rect.x + self.playerWidth + self.moveSpeed > self.width and self.keys[3] in keysPressed and keysPressed[self.keys[3]] == True or
           self.rect.x - self.moveSpeed < 0 and self.keys[0] in keysPressed and keysPressed[self.keys[0]] == True): return True

    # Responsible for jumping
    def jump(self):
        if(self.isStanding):
            self.jumpSpeed = 30
            self.isStanding = False
            Players.changeState(self, "jumping")
        elif(self.isStanding == False and self.powerJumpUsed == False):
            self.jumpSpeed = 30
            self.powerJumpUsed = True
            Players.changeState(self, "jumping")

    # Responsible for taking damage and accounting for health
    def takeDamage(self, coordinates, damage):
        attack = 50
        if(coordinates[0] <= self.rect.x):
            self.rect.x += attack
            self.rect.y -= attack
        elif(coordinates[0] > self.rect.x):
            self.rect.x -= attack
            self.rect.y -= attack
        self.health -= damage
        if(self.health < 1):
            self.health = 0
            return True

    # Responsible for changing image of character when player attacks
    def attack(self, valid):
        self.foundAttack = False
        Players.changeState(self, "fighting")

    # Loads and scales an image to be used
    def loadImage(self, image):
        image = pygame.image.load(image).convert_alpha()
        image = pygame.transform.scale(image, (self.playerWidth, self.playerHeight))
        return image

    # Changes and keeps track of state of a player
    def changeState(self, state):
        self.playerState = state
        if(state == "standing"): image = self.imageStanding
        elif(state == "fighting"): image = self.imageFighting
        elif(state == "jumping"): image = self.imageJumping
        #x, y = self.rect.centerx, self.rect.centery
        bottomLeft, bottomRight = self.rect.bottomleft, self.rect.bottomright
        self.image = image
        self.rect = self.image.get_rect()
        #self.rect.centerx, self.rect.centery = x, y
        self.rect.bottomleft, self.rect.bottomright = bottomLeft, bottomRight

    # Pauses player at a location
    def land(self, landingHeight):
        self.rect.bottom = landingHeight
        self.jumpSpeed = 0
        self.isStanding = True
        self.powerJumpUsed = False
        if(self.foundAttack == False):
            Players.changeState(self, "standing")

    # Increases health when a player hits a medical kit
    def increaseHealth(self):
        increment = 8
        full = 100
        if(self.health > full - increment): return
        else: self.health += increment

    # Simulates gravity if player is falling
    def simulateGravity(self):
        self.rect.y -= self.jumpSpeed
        self.jumpSpeed -= self.gravityIncrement

# Class representing the first player
class FirstPlayer(Players):

    keys = [pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT]

    # Contains all data for first player
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        # Picture From https://en.wikipedia.org/wiki/Mario
        self.imageStanding = Players.loadImage(self, "mariostanding.png")
        # Picture From http://fantendo.wikia.com/wiki/File:Mario_Kick_(2).png
        self.imageFighting = Players.loadImage(self, "mariokicking.png")
        # Picture From https://nintenfan.com/jumping-super-mario-bro
        self.imageJumping = Players.loadImage(self, "mariojumping.png")
        self.image = self.imageStanding
        self.rect = self.image.get_rect()
        self.rect.x = width - self.playerWidth - 100
        self.rect.y = height - self.playerHeight - 99
        self.isStanding = True
        self.powerJumpUsed = False
        self.health = 100
        self.playerState = "standing"
        self.jumpSpeed = 0
        self.foundAttack = False
        self.attackTime = 0
        self.hasShell = False

    # Respawns player in original coordinates
    def respawn(self):
        self.rect.y = self.height - self.playerHeight - 99
        self.rect.x = self.width - self.playerWidth - 100

# Class representing the second player
class SecondPlayer(Players):

    keys = [pygame.K_a, pygame.K_s, pygame.K_w, pygame.K_d]

    # Contains all data for the second player
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        # Picture From http://sonic.wikia.com/wiki/File:SFModernSonicRender.png
        self.imageStanding = Players.loadImage(self, "sonicstanding.png")
        # Picture From https://sites.google.com/site/brendansteinerdeep/home/sonic-the-hedgehog
        self.imageFighting = Players.loadImage(self, "sonicfighting.png")
        # Picture From http://www.stickpng.com/img/games/sonic/sonic-hedgehog-jumping-side
        self.imageJumping = Players.loadImage(self, "sonicjumping.png")
        self.image = self.imageStanding
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - self.playerHeight - 99
        self.isStanding = True
        self.powerJumpUsed = False
        self.health = 100
        self.playerState = "standing"
        self.jumpSpeed = 0
        self.foundAttack = False
        self.attackTime = 0
        self.hasShell = False

    # Respawns player in original coordinates
    def respawn(self):
        self.rect.y = self.height - self.playerHeight - 99
        self.rect.x = 100

# Class for a player controlled by the computer
class ComputerPlayer(Players):

    # Contains all data for the player controlled by the computer
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        # Picture From http://sonic.wikia.com/wiki/File:SFModernSonicRender.png
        self.imageStanding = Players.loadImage(self, "sonicstanding.png")
        # Picture From https://sites.google.com/site/brendansteinerdeep/home/sonic-the-hedgehog
        self.imageFighting = Players.loadImage(self, "sonicfighting.png")
        # Picture From http://www.stickpng.com/img/games/sonic/sonic-hedgehog-jumping-side
        self.imageJumping = Players.loadImage(self, "sonicjumping.png")
        self.image = self.imageStanding
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - self.playerHeight - 99
        self.isStanding = True
        self.powerJumpUsed = False
        self.health = 100
        self.playerState = "standing"
        self.jumpSpeed = 0
        # Speed at which computer player can move
        self.moveSpeed = 8
        # The maximum height difference from a jump
        self.jumpHeight = 165
        self.foundAttack = False
        self.attackTime = 0
        self.hasShell = False

    # Updates the position of the player each time
    def update(self, playerCoordinates):
        if(playerCoordinates[1] > self.rect.centery):
            if(self.rect.centerx > self.width / 2):
                self.rect.centerx -= self.moveSpeed
            elif(self.rect.centerx < self.width / 2):
                self.rect.centerx += self.moveSpeed
        else:
            # Accounts for horizontal movement
            if(self.rect.centerx < playerCoordinates[0]):
                self.rect.centerx += self.moveSpeed
            elif(self.rect.centerx > playerCoordinates[0]):
                self.rect.centerx -= self.moveSpeed
        # Accounts for vertical movement
        if(playerCoordinates[1] < self.rect.centery):
            Players.jump(self)
        # Responsible for player movement due to gravity
        if(not self.isStanding or self.powerJumpUsed == True):
            if(self.jumpSpeed < 1):
                Players.simulateGravity(self)
            elif(self.jumpSpeed > 0):
                self.rect.y -= self.jumpSpeed
                self.jumpSpeed -= self.gravityIncrement
        if(self.rect.y > self.height):
            self.respawn()

    # Respawns player in original coordinates
    def respawn(self):
        self.rect.y = self.height - self.playerHeight - 99
        self.rect.x = 100
