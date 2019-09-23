########################################
# Name: Jeffrey Igims
# Andrew Identification: jigims
# Term Project
########################################

# Description: File contains main game to be played

import pygame
from runfunction import *
from playerclass import *
from platformsclass import *
from medicalkits import *
from shells import *

black = [0, 0, 0]
white = [255, 255, 255]
blue = [0, 0, 255]
green = [0, 255, 0]
red = [255, 0, 0]

class SuperSmash(TermGameRun):

    # Contains all data for the main game
    def init(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.backgroundScreen = pygame.Surface([self.width, self.height])
        # Mode differentiates between playing against computer or other player
        self.mode = "titleMode"
        # Picture From https://www.deviantart.com/livingdeadsuperstar/art/NEW-Super-Smash-Bros-Title-Screen-680942519
        self.titleMode = pygame.image.load("titleScreen.png").convert_alpha()
        self.titleMode = pygame.transform.scale(self.titleMode, (self.width, self.height))
        # Picture From https://www.pexels.com/photo/blue-universe-956981/
        self.background = pygame.image.load("space.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        # Picture From http://es.videojuegos.wikia.com/wiki/Archivo:GAME_OVER.jpg
        self.gameOver = pygame.image.load("gameover.jpg").convert_alpha()
        self.gameOver = pygame.transform.scale(self.gameOver, (600, 500))
        # Picture From http://sburngdl.weebly.com/rules-of-game.html
        self.keys =  pygame.image.load("keys.png").convert_alpha()
        self.keys = pygame.transform.scale(self.keys, (380, 110))
        # Players are put into single sprite groups that can be updated and drawn
        self.player1 = pygame.sprite.GroupSingle()
        self.player2 = pygame.sprite.GroupSingle()
        # The keys players can use to basic attack
        self.player1Attack = pygame.K_p
        self.player2Attack = pygame.K_SPACE
        # Platform for the game
        self.mainPlatform = Platforms(850, 35, [75, 500])
        self.firstPlatform = Platforms(300, 20, [50, 250])
        self.secondPlatform = Platforms(300, 20, [650, 250])
        self.mainPlatformGroup = pygame.sprite.Group()
        self.mainPlatformGroup.add(self.mainPlatform)
        self.mainPlatformGroup.add(self.firstPlatform)
        self.mainPlatformGroup.add(self.secondPlatform)
        # Group contains medical kits added to the game
        self.medicalKits = pygame.sprite.Group()
        self.shells = pygame.sprite.Group()
        self.attackTimer = 0
        self.possibleAttack = True
        self.winner = None
        self.instructions = 0
        self.level = 1
        self.computerMoveSpeed = 5
        self.computerHitSpeed = 500
        self.gameSpeed = True
        self.gameSpeedHeight = 140

    # Called when player presses a key
    def keyPressed(self, keyCode, modifier, keysPressed):
        SuperSmash.possibleSkip(self, keyCode)
        if(self.mode == "titleMode"):
            SuperSmash.titleKeyPressed(self, keyCode)
        elif(self.mode == "playerMode"):
            SuperSmash.playerModeKeyPressed(self, keyCode, modifier, keysPressed)
        elif(self.mode == "computerMode"):
            SuperSmash.computerModeKeyPressed(self, keyCode, modifier, keysPressed)
        elif(self.mode == "overMode"):
            SuperSmash.overModeKeyPressed(self, keyCode, modifier, keysPressed)

    # Implemented every time timer function is called
    def timerFired(self, dt, keysPressed):
        if(self.mode == "titleMode"):
            pass
        elif(self.mode == "playerMode"):
            SuperSmash.playerModeTimerFired(self, dt, keysPressed)
        elif(self.mode == "computerMode"):
            SuperSmash.computerModeTimerFired(self, dt, keysPressed)
        elif(self.mode == "overMode"):
            pass

    # Directory for drawing the screen based on the mode
    def redrawAll(self, screen):
        if(self.mode == "titleMode"):
            SuperSmash.titleRedrawAll(self, screen)
        elif(self.mode == "playerMode"):
            SuperSmash.gameRedrawAll(self, screen)
        elif(self.mode == "computerMode"):
            SuperSmash.gameRedrawAll(self, screen)
        elif(self.mode == "overMode"):
            SuperSmash.gameRedrawAll(self, screen)

    # Called for keys pressed after the game is over
    def overModeKeyPressed(self, keyCode, modifier, keysPressed):
        if(pygame.K_SPACE == keyCode):
            self.mode = "titleMode"
            self.instructions = 0

    # Called when a player presses a key
    def playerModeKeyPressed(self, keyCode, modifier, keysPressed):
        if(keyCode == pygame.K_RETURN):
            self.instructions += 2
        elif(self.instructions < 2):
            return
        else:
            if(keyCode == self.player1Attack or keyCode == self.player2Attack):
                SuperSmash.playerAttack(self, keyCode)
            self.player1.update(FirstPlayer.keys, keysPressed, keyCode)
            self.player2.update(FirstPlayer.keys, keysPressed, keyCode)

    # Called when a player presses a key
    def computerModeKeyPressed(self, keyCode, modifier, keysPressed):
        if(keyCode == pygame.K_RETURN):
            self.instructions += 1
        elif(self.instructions < 2):
            return
        else:
            if(keyCode == self.player1Attack):
                SuperSmash.playerAttack(self, keyCode)
            self.player1.update(FirstPlayer.keys, keysPressed, keyCode)
            self.player2.update([self.first.rect.centerx, self.first.rect.centery])

    # Called when a key is pressed in the title screen
    def titleKeyPressed(self, keyCode):
        if(keyCode == pygame.K_1):
            self.mode = "computerMode"
            SuperSmash.prepareComputerMode(self)
        elif(keyCode == pygame.K_2):
            self.mode = "playerMode"
            SuperSmash.preparePlayerMode(self)

    # Implemented every time timer function is called
    def playerModeTimerFired(self, dt, keysPressed):
        if(self.instructions < 2):
            return
        timePassed = pygame.time.get_ticks()
        # Creates a medical kit and checks if player collides with the kits
        if(timePassed % 100 == 0):
            SuperSmash.createMedicalKit(self)
        if(timePassed % 100 == 0):
            SuperSmash.createShell(self)
        SuperSmash.checkMedicalKits(self)
        # Updates and takes in what keys are pressed to determine movement
        self.player1.update(FirstPlayer.keys, keysPressed)
        self.player2.update(SecondPlayer.keys, keysPressed)
        # Changes player states
        if(self.first.playerState == "fighting"):
            SuperSmash.pausePicture(self, self.first, timePassed)
        if(self.second.playerState == "fighting"):
            SuperSmash.pausePicture(self, self.second, timePassed)
        # Checks if any players land on any platforms in the game
        SuperSmash.checkPlatformLandings(self)
        SuperSmash.shells(self)

    # Contains all shell functions
    def shells(self):
        SuperSmash.checkShells(self)
        SuperSmash.moveShells(self)
        SuperSmash.checkShellCollisions(self)

    # Checks shell platform collisions
    def checkShellCollisions(self):
        for shell in self.shells:
            if(shell.shellThrown == False):
                continue
            for platform in self.mainPlatformGroup:
                if(platform.rect.colliderect(shell.rect)):
                    self.shells.remove(shell)
                    break
            if(shell.shellThrown == True):
                for player in [self.first, self.second]:
                    if(shell.owner == "first" and player == self.first):
                        continue
                    if(shell.owner == "second" and player == self.second):
                        continue
                    if(player.rect.colliderect(shell.rect)):
                        self.shells.remove(shell)
                        if(player == self.first):
                            if(player.takeDamage([self.second.rect.x, self.second.rect.y], 25) == True):
                                self.player1.remove(self.first)
                                self.winner = self.second
                                self.mode = "overMode"
                        else:
                            if(player.takeDamage([self.first.rect.x, self.first.rect.y], 25) == True):
                                self.player2.remove(self.second)
                                self.winner = self.first
                                self.mode = "overMode"

    # Moves shells
    def moveShells(self):
        self.shells.update([self.first.rect.x, self.first.rect.y], [self.second.rect.x, self.second.rect.y])

    # Checks for shells taken by players
    def checkShells(self):
        for player in [self.second, self.first]:
            for shell in self.shells:
                if(shell.shellThrown == True):
                    continue
                if(shell.rect.colliderect(player.rect)):
                    player.hasShell = True
                    shell.shellTaken = True
                    if(player == self.first):
                        shell.owner = "first"
                    else:
                        shell.owner = "second"

    # Creates shells for the game
    def createShell(self):
        newShell = Shell(self.height, self.width)
        self.shells.add(newShell)

    # Responsible for delaying picture of player fighting
    def pausePicture(self, player, timePassed):
        if(player.foundAttack == False):
            player.foundAttack = True
            player.attackTimer = timePassed + 200
        if(player.foundAttack == True):
            if(timePassed > player.attackTimer - 50 and timePassed < player.attackTimer + 50):
                player.changeState("standing")
                player.foundAttack = False

    # Implemented every time timer function is called
    def computerModeTimerFired(self, dt, keysPressed):
        self.computerHitSpeed = 200 + (self.gameSpeedHeight * 1.42837143)
        self.second.moveSpeed = 10 - (self.gameSpeedHeight * .025)
        if(self.instructions == 1):
            if(pygame.K_UP in keysPressed and keysPressed[pygame.K_UP] == True):
                if(self.gameSpeedHeight == 0):
                    return
                self.gameSpeedHeight -= 20
            elif(pygame.K_DOWN in keysPressed and keysPressed[pygame.K_DOWN] == True):
                if(self.gameSpeedHeight == 280):
                    return
                self.gameSpeedHeight += 20
        if(self.instructions < 2):
            return
        timePassed = pygame.time.get_ticks()
        # Creates a medical kit and checks if player collides with the kits
        if(timePassed % 100 == 0):
            SuperSmash.createMedicalKit(self)
        if(timePassed % 100 == 0):
            SuperSmash.createShell(self)
        SuperSmash.checkMedicalKits(self)
        # Updates and takes in what keys are pressed to determine movement
        self.player1.update(FirstPlayer.keys, keysPressed)
        self.player2.update([self.first.rect.centerx, self.first.rect.centery])
        # Changes player states
        if(self.first.playerState == "fighting"):
            SuperSmash.pausePicture(self, self.first, timePassed)
        if(self.second.playerState == "fighting"):
            SuperSmash.pausePicture(self, self.second, timePassed)
        # Checks if any players land on any platforms in the game
        SuperSmash.checkPlatformLandings(self)
        # Accounts for computer attacking the player
        if(self.possibleAttack == True):
            if(pygame.sprite.groupcollide(self.player1, self.player2, False, False)):
                self.attackTimer = timePassed + self.computerHitSpeed
                self.possibleAttack = False
        if(self.possibleAttack == False):
            if(timePassed > self.attackTimer - 100 and timePassed < self.attackTimer + 100):
                SuperSmash.playerAttack(self)
                self.possibleAttack = True
        SuperSmash.shells(self)
        if(self.second.hasShell == True):
            SuperSmash.playerAttack(self)

    # Draws all items on the game screen
    def gameRedrawAll(self, screen):
        screen.blit(self.background, (0, 0))
        self.player1.draw(screen)
        self.player2.draw(screen)
        self.mainPlatformGroup.draw(screen)
        self.medicalKits.draw(screen)
        self.shells.draw(screen)
        SuperSmash.displayHealth(self, screen)
        if(self.instructions == 0):
            SuperSmash.instructions(self, screen)
        elif(self.instructions == 1):
            SuperSmash.gameSpeed(self, screen)
        if(self.mode == "overMode"):
            SuperSmash.drawOverScreen(self, screen)

    # Draws all items on title screen
    def titleRedrawAll(self, screen):
        screen.blit(self.titleMode, (0, 0))
        SuperSmash.drawCommand(self, screen, True)

    # Draws the command in the title screen
    def drawCommand(self, screen, confirm):
        if(confirm == True):
            pygame.draw.rect(screen, black, (300, 475, 400, 50))
            SuperSmash.createText(self, screen, "PRESS 1 OR 2 FOR NUMBER OF PLAYERS", (500, 500), 27, white)

    # Called if player initiates an attack and checks if the attack is valid
    def playerAttack(self, keyCode = None):
        if(keyCode == self.player1Attack):
            if(self.first.hasShell == True):
                for shell in self.shells:
                    if(shell.owner == "first"):
                        shell.shellThrown = True
                        shell.shellTaken = False
                        self.first.hasShell = False
            if(pygame.sprite.groupcollide(self.player1, self.player2, False, False)):
                self.first.attack(True)
                coordinates = [self.first.rect.x, self.first.rect.y]
                if(self.second.takeDamage(coordinates, 10) == True):
                    self.player2.remove(self.second)
                    self.winner = self.first
                    self.mode = "overMode"
            else:
                self.first.attack(False)
        else:
            if(self.second.hasShell == True):
                for shell in self.shells:
                    if(shell.owner == "second"):
                        shell.shellThrown = True
                        shell.shellTaken = False
                        self.second.hasShell = False
            if(pygame.sprite.groupcollide(self.player1, self.player2, False, False)):
                self.second.attack(True)
                coordinates = [self.second.rect.x, self.second.rect.y]
                if(self.first.takeDamage(coordinates, 10) == True):
                    self.player1.remove(self.first)
                    self.winner = self.second
                    self.mode = "overMode"
            else:
                self.second.attack(False)

    # Displays health of players
    def displayHealth(self, screen):
        margin = 50
        player1Health = self.first.health
        player2Health = self.second.health
        pygame.draw.circle(screen, black, (margin, margin), margin)
        pygame.draw.circle(screen, black, (self.width - margin, margin), margin)
        SuperSmash.createText(self, screen, str(player2Health), [margin, margin], 48, red)
        SuperSmash.createText(self, screen, str(player1Health), [self.width - margin, margin], 48, red)

    # Renders and creates a surface for text
    def createText(self, screen, text, location, size, color):
        basicfont = pygame.font.SysFont(None, size)
        text = basicfont.render(text, True, color)
        textLocation = text.get_rect()
        textLocation.centerx = location[0]
        textLocation.centery = location[1]
        screen.blit(text, textLocation)

    # Checks if a player grabs a medical kit
    def checkMedicalKits(self):
        if(pygame.sprite.groupcollide(self.player1, self.medicalKits, False, True)):
            self.first.increaseHealth()
        if(pygame.sprite.groupcollide(self.player2, self.medicalKits, False, True)):
            self.second.increaseHealth()

    # Creates medical kits
    def createMedicalKit(self):
        medicalKit = Kit(self.height, self.width)
        self.medicalKits.add(medicalKit)

    # Checks for players landing on platforms
    def checkPlatformLandings(self):
        for player in [self.second, self.first]:
            for platform in self.mainPlatformGroup:
                if(platform.rect.colliderect(player.rect)):
                    if(player.jumpSpeed < 0):
                        player.land(platform.rect.top + 1)
                        break
            player.simulateGravity()

    # Prepares computer mode
    def prepareComputerMode(self):
        self.first = FirstPlayer(self.width, self.height)
        self.second = ComputerPlayer(self.width, self.height)
        self.player1.add(self.first)
        self.player2.add(self.second)

    # Prepares player mode
    def preparePlayerMode(self):
        self.first = FirstPlayer(self.width, self.height)
        self.second = SecondPlayer(self.width, self.height)
        self.player1.add(self.first)
        self.player2.add(self.second)

    # Draws the screen when the game ends
    def drawOverScreen(self, screen):
        altitude = 350
        screen.blit(self.gameOver, (200, 50))
        SuperSmash.createText(self, screen, "PRESS SPACE TO RETURN TO TITLE", (500, 400), 27, red)
        if(self.winner == self.first):
            SuperSmash.createText(self, screen, "PLAYER 1 WINS", (500, altitude), 27, red)
        elif(self.winner == self.second):
            SuperSmash.createText(self, screen, "PLAYER 2 WINS", (500, altitude), 27, red)
        else:
            SuperSmash.createText(self, screen, "PLAYER 1 WINS", (500, altitude), 27, red)

    # Accounts for shortcuts
    def possibleSkip(self, keyCode):
        if(keyCode == pygame.K_8):
            if(self.mode == "playerMode" or self.mode == "computerMode"):
                self.mode = "overMode"
            elif(self.mode == "overMode"):
                self.instructions = 0
                self.mode = "titleMode"

    # Displays instructions
    def instructions(self, screen):
        pygame.draw.rect(screen, white, (200, 50, 600, 500))
        screen.blit(self.keys, (310, 200))
        SuperSmash.createText(self, screen, "PLAYER 2 KEYS", (400, 100), 27, black)
        SuperSmash.createText(self, screen, "PLAYER 1 KEYS", (600, 100), 27, black)
        SuperSmash.createText(self, screen, "MOVE KEYS:", (400, 180), 27, black)
        SuperSmash.createText(self, screen, "MOVE KEYS:", (600, 180), 27, black)
        SuperSmash.createText(self, screen, "FIGHT KEY: 'SPACE'", (400, 350), 27, black)
        SuperSmash.createText(self, screen, "FIGHT KEY: 'P'", (600, 350), 27, black)
        SuperSmash.createText(self, screen, "Instructions", (500, 416), 27, black)
        SuperSmash.createText(self, screen, "MEDICAL KITS: INCREASE HEALTH WHEN CAPTURED", (500, 446), 20, black)
        SuperSmash.createText(self, screen, "SHELLS: TRACK OPPONENT WHEN THROWN", (500, 464), 20, black)
        SuperSmash.createText(self, screen, "PRESS ENTER TO CONTINUE", (500, 482), 20, black)

    # Selected difficulty
    def gameSpeed(self, screen):
        pygame.draw.rect(screen, white, (200, 50, 600, 500))
        SuperSmash.createText(self, screen, "USE KEYS TO SELECT DIFFICULTY", (500, 440), 27, black)
        SuperSmash.createText(self, screen, "PRESS ENTER TO CONTINUE", (500, 482), 27, black)
        pygame.draw.rect(screen, red, (470, 100, 60, 280))
        pygame.draw.rect(screen, white, (470, 100, 60, self.gameSpeedHeight))
        pygame.draw.rect(screen, black, (465, 100, 5, 280))
        pygame.draw.rect(screen, black, (530, 100, 5, 280))
        pygame.draw.rect(screen, black, (465, 97, 70, 5))
        pygame.draw.rect(screen, black, (465, 380, 70, 5))

game = SuperSmash()
game.run()
