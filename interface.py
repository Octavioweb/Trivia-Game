##Este es el primer boceto de programa que jugariá un juego de trivias!
# Usa los módulos de pygame, sqlalchemy y requests para hacerlo posible!
# Más información contactar al creador via github. github/Octavioweb.com

import pygame, sys, random, sqlalchemy, requests
from pygame.locals import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

FPS = 30

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

pygame.background = BGCOLOR
pygame.init()

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
pygame.display.set_caption('Hola Mundo')


"""
url = "https://opentdb.com/api.php?amount=10"
response = requests.get(url)
print(response.json())
"""


def main():
    global WINDOWFACTOR, WINDOWWIDTH, WINDOWHEIGHT, WINDOWFACTOR, WW, WH, WF
    mousex = 0
    mousey = 0
    DISPLAYSURF.fill(BGCOLOR)
    interface = Interface1(WINDOWFACTOR)
    interface.getFigures()
    
    #testSquare = SquareButton(10, 10, 200, 100, text= "Hola mundo", textType = 1, textColor = GREEN, textSize= 30)

    while True:
        #testSquare.selfDraw()
        for event in pygame.event.get():
            if event.type == 256:
                pygame.quit()
                sys.exit()
            elif event.type == WINDOWSIZECHANGED:
                WINDOWWIDTH = event.x
                WINDOWHEIGHT = event.y
                #print(event.x, event.y)
                WINDOWFACTOR = int(WINDOWHEIGHT/25)
                WW =  WINDOWWIDTH
                WH = WINDOWHEIGHT
                WF = WINDOWFACTOR
                del interface
                interface = Interface2(WINDOWFACTOR)
                interface.getFigures()

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            
            elif event.type == MOUSEBUTTONDOWN:
                click= True

            elif event.type == MOUSEBUTTONUP:
                click = False
                mouseRelease = True
            mouseRelease = False
            print(event)

        interface.checkHighlight(mousex, mousey)
        interface.selfDraw()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

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
                self.objectList[i].highlight = True
            
            else: self.objectList[i].highlight = False


class Interface2(object):
    # Preguntas de opcion multiple
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
        
        self.question1 = SquareButton(WW/12       , WH/3    , (WW/3)+2*WF, (WH/4.5), text= "Jugar1", textType = 1, textColor = GREEN, textSize= WF)
        self.question2 = SquareButton(WW/12 + WW/2 - 2*WF, WH/3    , (WW/3)+2*WF, (WH/4.5), text= "Jugar2", textType = 1, textColor = GREEN, textSize= WF)
        self.question3 = SquareButton(WW/12       , (2*WH/3.5), (WW/3)+2*WF, (WH/4.5), text= "Jugar3", textType = 1, textColor = GREEN, textSize= WF)
        self.question4 = SquareButton(WW/12 + WW/2 - 2*WF, (2*WH/3.5), (WW/3)+2*WF, (WH/4.5), text= "Jugar4", textType = 1, textColor = GREEN, textSize= WF)
        
        self.quit = SquareButton((2*WW/3), 4*WH/5, (WW/3)-WINDOWFACTOR, (WH/6)-6, text= "Salir", color = RED, textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)

        self.objectList = [self.question1, self.question2, self.question3, self.question4, self.quit]

    def selfDraw(self):
        DISPLAYSURF.blit (self.presentText, self.presentText_r)
        DISPLAYSURF.blit (self.questionText, self.questionText_r)

        for object in self.objectList:
            object.selfDraw()

    def checkHighlight(self, mousex,mousey):
        for i in range (len(self.objectList)):
            if self.objectList[i].collidePoint(mousex,mousey):
                self.objectList[i].highlight = True
            else: self.objectList[i].highlight = False

class Interface1(object):
    #Interfaz de bienvenida
    def __init__(self, WINDOWFACTOR):
        self.textColor = WHITE
        self.objectList = []
        self.fontSize = int(WINDOWFACTOR *2.5)

        self.font = pygame.font.Font("REM-VariableFont_wght.ttf", self.fontSize)

    def getFigures(self):
        # INTRODUCTION TEXT
        self.introductionText = self.font.render("Bienvenido a Octo-trivia!", True, self.textColor, BGCOLOR)
        self.introductionText_r = self.introductionText.get_rect()
        self.introductionText_r.center = (WW/2, WH/5)
        
        self.playButton = SquareButton(WINDOWFACTOR, WH/3, (WW/3)-WINDOWFACTOR, (WH/3), text= "Jugar", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)
        self.question10 = SquareButton(WW/3  + WINDOWFACTOR/2, WH/3, (WW/3)-WINDOWFACTOR, (WH/6)-6, text= "10 Preguntas", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)
        self.question15 = SquareButton(WW/3  + WINDOWFACTOR/2, 6+WH/2, (WW/3)-WINDOWFACTOR, WH/6-6, text= "15 Preguntas", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)
        self.seeLeaderboard = SquareButton((2*WW/3), WH/3, (WW/3)-WINDOWFACTOR, WH/3, text= "Marcadores", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)

        self.reset = SquareButton(WINDOWFACTOR, 4*WH/5, (WW/3)-WINDOWFACTOR, (WH/6)-6, text= "Reiniciar", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)
        self.source = SquareButton(WW/3  + WINDOWFACTOR/2, 4*WH/5, (WW/3)-WINDOWFACTOR, WH/6-6, text= "GitHub", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)
        self.quit = SquareButton((2*WW/3), 4*WH/5, (WW/3)-WINDOWFACTOR, (WH/6)-6, text= "Salir", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)

        self.objectList = [self.playButton, self.question10, self.question15, self.seeLeaderboard, self.reset, self.source, self.quit]

    def selfDraw(self):
        DISPLAYSURF.blit (self.introductionText, self.introductionText_r)

        for object in self.objectList:
            object.selfDraw()

    def checkHighlight(self, mousex,mousey):
        for i in range (len(self.objectList)):
            if self.objectList[i].collidePoint(mousex,mousey):
                self.objectList[i].highlight = True
            else: self.objectList[i].highlight = False

class SquareButton(object):
    def __init__(self, x, y, width, height, text=None, color=WHITE, textSize=20, textType=None, textColor=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.textSize = textSize
        self.textType = textType
        self.textColor = textColor
        self.highlight = False
        self.press = False
        self.font = pygame.font.Font("REM-VariableFont_wght.ttf", textSize)

        
        self.highlightfactor = 50
        self.highlightcolor =(self.color[0]-self.highlightfactor if self.color[0] > self.highlightfactor else 0, 
                              self.color[0]-self.highlightfactor if self.color[1] > self.highlightfactor else 0, 
                              self.color[0]-self.highlightfactor if self.color[2] > self.highlightfactor else 0)
        
        self.pressFactor = 100
        self.pressColor = (self.color[0]-self.pressFactor if self.color[0] > self.pressFactor else 0, 
                              self.color[0]-self.pressFactor if self.color[1] > self.pressFactor else 0, 
                              self.color[0]-self.pressFactor if self.color[2] > self.pressFactor else 0)

    def selfDraw(self):
        # textType = 1: 
        #   Se imprime el texto a la izquierda
        # textType = 2:
        #   Se imprime el texto centrado
        
        if self.highlight:
            pygame.draw.rect(DISPLAYSURF, self.highlightcolor, ((self.x, self.y, self.width, self.height)))
            if self.textType:
                if self.textType ==1:

                    self.squareText = self.font.render(self.text, True, self.textColor, self.highlightcolor)
                    self.squareText_r = self.squareText.get_rect()
                    self.squareText_r.center = (self.x+self.width/3, self.y+self.height/2)
                    DISPLAYSURF.blit (self.squareText, self.squareText_r)
                
                elif self.textType ==2:
                    self.squareText = self.font.render(self.text, True, self.textColor, self.highlightcolor)
                    self.squareText_r = self.squareText.get_rect()
                    self.squareText_r.center = (self.x+self.height/2, self.y+self.width/2)
                    DISPLAYSURF.blit (self.squareText, self.squareText_r)
        elif self.press:
            pygame.draw.rect(DISPLAYSURF, self.pressColor, ((self.x, self.y, self.width, self.height)))
            if self.textType:
                if self.textType ==1:

                    self.squareText = self.font.render(self.text, True, self.textColor, self.pressColor)
                    self.squareText_r = self.squareText.get_rect()
                    self.squareText_r.center = (self.x+self.width/3, self.y+self.height/2)
                    DISPLAYSURF.blit (self.squareText, self.squareText_r)
                    
                elif self.textType ==2:
                    self.squareText = self.font.render(self.text, True, self.textColor, self.pressColor)
                    self.squareText_r = self.squareText.get_rect()
                    self.squareText_r.center = (self.x+self.height/2, self.y+self.width/2)
                    DISPLAYSURF.blit (self.squareText, self.squareText_r)
        else:
            pygame.draw.rect(DISPLAYSURF, self.color, ((self.x, self.y, self.width, self.height)))
            if self.textType:
                if self.textType ==1:

                    self.squareText = self.font.render(self.text, True, self.textColor, self.color)
                    self.squareText_r = self.squareText.get_rect()
                    self.squareText_r.center = (self.x+self.width/3, self.y+self.height/2)
                    DISPLAYSURF.blit (self.squareText, self.squareText_r)
                
                elif self.textType ==2:
                    self.squareText = self.font.render(self.text, True, self.textColor, self.color)
                    self.squareText_r = self.squareText.get_rect()
                    self.squareText_r.center = (self.x+self.height/2, self.y+self.width/2)
                    DISPLAYSURF.blit (self.squareText, self.squareText_r)

    def changeText(self, text:str):
        self.text = text
    
    def changeColor(self, color):
        self.color = color

    def collidePoint(self, mousex, mousey):
        if mousex > self.x and mousex < self.x+self.width and mousey > self.y and mousey < self.y+ self.height:
            return True

if __name__ == '__main__':
    main()