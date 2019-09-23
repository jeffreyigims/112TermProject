########################################
# Name: Jeffrey Igims
# Andrew Identification: jigims
# Term Project
########################################

# Description: File contains framework for running the game graphics

import pygame

# Framework adapted from Lukas Peraza
# https://qwewy.gitbooks.io/pygame-module-manual/chapter1/framework.html

class TermGameRun(object):

    def init(self):
        pass

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier, keysPressed):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt, keys):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        pass

    def __init__(self, width = 1000, height = 600, fps = 15, title = "Project"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        screen = self.screen
        # Sets title of window
        pygame.display.set_caption(self.title)
        # Stores all current keys
        self._keys = dict()
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time, self._keys)
            for event in pygame.event.get():
                if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    self.mousePressed(*(event.pos))
                elif(event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                    self.mouseReleased(*(event.pos))
                elif(event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif(event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif(event.type == pygame.KEYDOWN):
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod, self._keys)
                elif(event.type == pygame.KEYUP):
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif(event.type == pygame.QUIT):
                    playing = False
                screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()
