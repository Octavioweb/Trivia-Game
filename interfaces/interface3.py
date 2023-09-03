import pygame, sys, random, sqlalchemy, requests
from pygame.locals import *

FPS = 10


#Colors   R    G    B
WHITE = (255, 255, 255)
RED =   (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE =  (  0,   0, 255)
BLACK = (  0,   0,   0)
DARK_GRAY = (40, 40, 40)

BGCOLOR = DARK_GRAY
WINDOWFACTOR = 30

WINDOWHEIGHT = WINDOWFACTOR * 25
WINDOWWIDTH = WINDOWFACTOR * 35
WW = WINDOWWIDTH
WH = WINDOWHEIGHT
WF = WINDOWFACTOR

class Interface3(object):
    #Preguntas de true/false
    def __init__(self, WINDOWFACTOR):
        self.textColor = WHITE
        self.objectList = []
        self.fontSize = int(WW /15)
        self.smallerFontSize =  int(WW/25)

        self.font = pygame.font.Font("REM-VariableFont_wght.ttf", self.fontSize)
        self.smallerFont = pygame.font.Font("REM-VariableFont_wght.ttf", self.smallerFontSize)

    def getFigures(self):
        # INTRODUCTION TEXT
        self.presentText = self.font.render("Estás jugando a 10 preguntas!", True, self.textColor, BGCOLOR)
        self.presentText_r = self.presentText.get_rect()
        self.presentText_r.center = (WW/2, WH/8)

        self.questionText = self.smallerFont.render("1. Puedes leer esto?", True, self.textColor, BGCOLOR)
        self.questionText_r = self.questionText.get_rect()
        self.questionText_r.center = (WW/2, WH/4)
        
        self.questionTrue = SquareButton(WW/12               , WH/3    , (WW/3)+2*WF, (WH/3), text= "Jugar1", textType = 1, textColor = GREEN, textSize= WF)
        self.questionFalse = SquareButton(WW/12 + WW/2 - 2*WF, WH/3    , (WW/3)+2*WF, (WH/3), text= "Jugar2", textType = 1, textColor = GREEN, textSize= WF)
        
        
        self.quit = SquareButton((2*WW/3), 4*WH/5, (WW/3)-WINDOWFACTOR, (WH/6)-6, text= "Salir", color = RED, textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)

        self.objectList = [self.questionTrue, self.questionFalse, self.quit]

    def selfDraw(self):
        DISPLAYSURF.blit (self.presentText, self.presentText_r)
        DISPLAYSURF.blit (self.questionText, self.questionText_r)

        for object in self.objectList:
            object.selfDraw()

    def checkHighlight(self, mousex,mousey, click, release):
        for i in range (len(self.objectList)):
            if self.objectList[i].collidePoint(mousex,mousey):
                if click:
                    pass
                
                elif release:
                    pass
                
                else:
                    self.objectList[i].highlight = True
            
            else: self.objectList[i].highlight = False
