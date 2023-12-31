##Este es el primer boceto de programa que jugariá un juego de trivias!
# Usa los módulos de pygame, sqlalchemy y requests para hacerlo posible!
# Más información contactar al creador via github. github/Octavioweb.com

import pygame, sys, random, sqlalchemy, requests
from pygame.locals import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from requests_funcionalidad import GameEngine
GameEngine = GameEngine()

import webbrowser


FPS = 20

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
    global WINDOWFACTOR, WINDOWWIDTH, WINDOWHEIGHT, WINDOWFACTOR, WW, WH, WF, interface
    click = False
    mouseRelease = False

    mousex = 0
    mousey = 0
    DISPLAYSURF.fill(BGCOLOR)
    interface = Interface1(WINDOWFACTOR)
    interface.getFigures()
    
    #testSquare = SquareButton(10, 10, 200, 100, text= "Hola mundo", textType = 1, textColor = GREEN, textSize= 30)

    while True:

        mouseRelease = False

        #testSquare.selfDraw()
        for event in pygame.event.get():

            if event.type == 256:
                terminate()
            elif event.type == WINDOWSIZECHANGED:
                WINDOWWIDTH = event.x
                WINDOWHEIGHT = event.y
                #print(event.x, event.y)
                WINDOWFACTOR = int(WINDOWHEIGHT/25)
                WW =  WINDOWWIDTH
                WH = WINDOWHEIGHT
                WF = WINDOWFACTOR
                interface.getFigures()

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            
            elif event.type == MOUSEBUTTONDOWN:
                click= True

            elif event.type == MOUSEBUTTONUP:
                click = False
                mouseRelease = True
            #print(click, mouseRelease)

        if interface.checkHighlight(mousex, mousey, click, mouseRelease):
            code = clickActions(interface.clickAction())
            eval(str(code))
        interface.selfDraw()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def clickActions(clickAction):
    global interface
    match clickAction:
        case 'changeInterface':
            newInterface = interface.newInterface
            interface = newInterface
            interface.getFigures()
            DISPLAYSURF.fill(BGCOLOR)
        case 'quit':
            terminate()
        case 'openGithub':
            openGithub()
        case 'reset':
            resetLeaderboard()
        case 'startGame':
            question_temp = GameEngine.nextQuestion()

            if len(question_temp['options']) == 4:
                interface = Interface2(WINDOWFACTOR, question_temp['options'], question_temp['question'])
            else:
                interface = Interface3(WINDOWFACTOR, question_temp['question'], question_temp['options'])
            interface.getFigures()
            DISPLAYSURF.fill(BGCOLOR)

        case 'checkAnswer':
            GameEngine.checkAnswer(interface.answer)
            question_temp = GameEngine.nextQuestion()
            if len(question_temp['options']) == 4:
                interface = Interface2(WINDOWFACTOR, question_temp['options'], question_temp['question'])
            else:
                interface = Interface3(WINDOWFACTOR, question_temp['question'], question_temp['options'])
            interface.getFigures()
            DISPLAYSURF.fill(BGCOLOR)

    

class Interface1(object):
    #Interfaz de bienvenida
    def __init__(self, WINDOWFACTOR):
        self.question10Bool = True
        self.textColor = WHITE
        self.objectList = []
        self.questionsColors = [200,0,150]
        self.fontSize = int(WINDOWFACTOR *2.5)
        
        self.font = pygame.font.Font("REM-VariableFont_wght.ttf", self.fontSize)

    def getFigures(self):
        # INTRODUCTION TEXT
        self.introductionText = self.font.render("Bienvenido a Octo-trivia!", True, self.textColor, BGCOLOR)
        self.introductionText_r = self.introductionText.get_rect()
        self.introductionText_r.center = (WW/2, WH/5)
        
        self.playButton = SquareButton(WINDOWFACTOR, WH/3, (WW/3)-WINDOWFACTOR, (WH/3), text= "Jugar", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)
        self.question10 = SquareButton(WW/3  + WINDOWFACTOR/2, WH/3, (WW/3)-WINDOWFACTOR, (WH/6)-6, text= "10 Preguntas", 
                                       textType = 1, textColor = GREEN, textSize= WINDOWFACTOR, color = self.questionsColors)
        
        self.question15 = SquareButton(WW/3  + WINDOWFACTOR/2, 6+WH/2, (WW/3)-WINDOWFACTOR, WH/6-6, text= "15 Preguntas", 
                                       textType = 1, textColor = GREEN, textSize= WINDOWFACTOR, color = WHITE)
        
        self.seeLeaderboard = SquareButton((2*WW/3), WH/3, (WW/3)-WINDOWFACTOR, WH/3, text= "Marcadores", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)

        self.reset = SquareButton(WINDOWFACTOR, 4*WH/5, (WW/3)-WINDOWFACTOR, (WH/6)-6, text= "Reiniciar", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)
        self.source = SquareButton(WW/3  + WINDOWFACTOR/2, 4*WH/5, (WW/3)-WINDOWFACTOR, WH/6-6, text= "GitHub", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)
        self.quit = SquareButton((2*WW/3), 4*WH/5, (WW/3)-WINDOWFACTOR, (WH/6)-6, text= "Salir", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)

        self.objectList = [self.playButton, self.question10, self.question15, self.seeLeaderboard, self.reset, self.source, self.quit]

    def selfDraw(self):
        DISPLAYSURF.blit (self.introductionText, self.introductionText_r)
        for object in self.objectList:
            object.selfDraw()

    def checkHighlight(self, mousex,mousey, click, release):
        for i in range (len(self.objectList)):
            if self.objectList[i].collidePoint(mousex,mousey):
                if click:
                    self.objectList[i].press = True

                elif release:
                    self.i = i
                    if self.i not in [1,2]:
                        return True
                    
                    elif self.i == 1:
                        self.question15.changeColor(WHITE)
                        self.question10.changeColor(self.questionsColors)
                        self.question10Bool = True
                        return False
                    
                    elif self.i == 2:
                        self.question15.changeColor(self.questionsColors)
                        self.question10.changeColor(WHITE)
                        self.question10Bool = False

                        return False
                    
                else:
                    self.objectList[i].highlight = True
            else: 
                self.objectList[i].highlight = False
                self.objectList[i].press = False
    
    def clickAction(self):
        if self.i == 0:
            if self.question10Bool:
                GameEngine.startGame(10)
            else:
                GameEngine.startGame(15)

            
            
            return 'startGame'
        
        elif self.i == 3:
            self.newInterface = Interface4(WINDOWFACTOR) # Interface que aun no se hace para visualizar tablero
            getLeaderboard()
            return 'changeInterface'
        
        elif self.i == 4:
            resetLeaderboard()

        elif self.i ==5:
            openGithub()
        
        elif self.i ==6:
            terminate()

class Interface2(object):
    # Preguntas de opcion multiple
    def __init__(self, WINDOWFACTOR, question, options):
        self.question = str(question)
        self.options = options
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

        self.questionText = self.smallerFont.render(self.question, True, self.textColor, BGCOLOR)
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

    def checkHighlight(self, mousex,mousey, click, release):
        for i in range (len(self.objectList)):
            if self.objectList[i].collidePoint(mousex,mousey):
                self.objectList[i].highlight = True
            else: self.objectList[i].highlight = False


class Interface3(object):
    #Preguntas de true/false
    def __init__(self, WINDOWFACTOR, question, options):
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
                    self.objectList[i].press = True

                elif release:
                    self.i = i
                    if self.i not in [1,2]:
                        return True
                    
                    elif self.i == 1:
                        self.question15.changeColor(WHITE)
                        self.question10.changeColor(self.questionsColors)
                        return False
                    
                    elif self.i == 2:
                        self.question15.changeColor(self.questionsColors)
                        self.question10.changeColor(WHITE)
                        return False
                    
                else:
                    self.objectList[i].highlight = True
            else: 
                self.objectList[i].highlight = False
                self.objectList[i].press = False

class Interface4(object):
    # Marcadores
    def __init__(self, WINDOWFACTOR):
        self.textColor = WHITE
        self.bgColor = BLUE
        self.squareColor = [200,240,240]

        self.objectList = []
        self.fontSize = int(WW /15)
        self.smallerFontSize =  int(WW/25)

        self.font = pygame.font.Font("REM-VariableFont_wght.ttf", self.fontSize)
        self.smallerFont = pygame.font.Font("REM-VariableFont_wght.ttf", self.smallerFontSize)
        self.actionDict = {0: False, 1:False, 2:'changeInterface', 3:'quit'}


    def getAction(self):
        return self.actionDict[self.i]
    
    def getFigures(self):
        self.fontSize = int(WW /15)
        self.smallerFontSize =  int(WW/25)
        self.font = pygame.font.Font("REM-VariableFont_wght.ttf", self.fontSize)
        self.smallerFont = pygame.font.Font("REM-VariableFont_wght.ttf", self.smallerFontSize)

        # INTRODUCTION TEXT
        self.leaderboardText = TextObj(WW/2, WH/6, text= "Leaderboard")
        self.q10Text = TextObj(WW/4, WH/5, text = "10 questions")
        self.q15Text = TextObj(3*WW/4, WH/5, text = "15 questions")

        self.leaderboardQ10 = SquareButton(WW/20, WH/4, (4*WW)/10, WH/2)
        self.leaderboardQ15 = SquareButton(WW-WW/20-(4*WW/10), WH/4, (4*WW)/10, WH/2)
        
        self.back = SquareButton((1*WW/3), 4*WH/5, (WW/3)-WINDOWFACTOR, (WH/6)-6, text= "Volver", textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)
        self.quit = SquareButton((2*WW/3), 4*WH/5, (WW/3)-WINDOWFACTOR, (WH/6)-6, text= "Salir", color = RED, textType = 1, textColor = GREEN, textSize= WINDOWFACTOR)

        self.Q10_1 = TextObj(WW/4 , WH/3, text = "1:       Name = {0:15} Score = {1}/10".format('Octavio', 9), color = BLACK,  BGCOLOR =  [240,240,240])
        self.Q10_2 = TextObj(WW/4 - 5*WW/20 + WW/15, WH/3+WH/8, '2:')
        self.Q10_3 = TextObj(WW/4 - 5*WW/20 + WW/15, WH/3+2*WH/8, '3:')
        self.Q10_4 = TextObj(WW/4 - 5*WW/20 + WW/15, WH/3+3*WH/8, '4:')
        
        # Textos
        self.Q10_arr = [self.Q10_1, self.Q10_2, self.Q10_3, self.Q10_4]

        self.objectList = [self.leaderboardQ10, self.leaderboardQ15, self.back, self.quit]
        self.textList = [self.leaderboardText, self.q10Text, self.q15Text] + self.Q10_arr

    def selfDraw(self):
        for object in self.objectList:
            object.selfDraw()

        for object in self.textList:
            object.selfDraw()
        

    def checkHighlight(self, mousex,mousey,click,release):
        for i in range (2,len(self.objectList)):
            if self.objectList[i].collidePoint(mousex,mousey):
                if click:
                    self.objectList[i].press = True

                elif release:
                    self.i = i
                    if self.i not in [0,1]:
                        return True
                    return True
                    
                else:
                    self.objectList[i].highlight = True
            else: 
                self.objectList[i].highlight = False
                self.objectList[i].press = False

    def clickAction(self):
        if self.i == 2:
            self.newInterface = Interface1(WINDOWFACTOR)
            return 'changeInterface'
        
        elif self.i == 3:
            terminate()

class TextObj(object):
    def __init__(self, x, y, text=None, color=[240,240,240], size=20, font = False, BGCOLOR = BGCOLOR):
        if not font:
            self.font = pygame.font.Font("REM-VariableFont_wght.ttf", size)
            self.text = self.font.render(text, True, color, BGCOLOR)
        else: 
            self.text = font.render(text, True, color, BGCOLOR)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (x,y)


    def selfDraw(self):
        DISPLAYSURF.blit (self.text, self.text_rect)

class SquareButton(object):
    def __init__(self, x, y, width, height, text=None, color=[240,240,240], textSize=20, textType=None, textColor=BLACK, center = False):
        
        if center:
            self.x = x - 0.5*width
            self.y = y - 0.5*height
        else:
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
                              self.color[1]-self.highlightfactor if self.color[1] > self.highlightfactor else 0, 
                              self.color[2]-self.highlightfactor if self.color[2] > self.highlightfactor else 0)
        
        self.pressFactor = 100
        self.pressColor = (self.color[0]-self.pressFactor if self.color[0] > self.pressFactor else 0, 
                              self.color[1]-self.pressFactor if self.color[1] > self.pressFactor else 0, 
                              self.color[2]-self.pressFactor if self.color[2] > self.pressFactor else 0)

    def selfDraw(self):
        # textType = 1: 
        #   Se imprime el texto a la izquierda
        # textType = 2:
        #   Se imprime el texto centrado
        
        
        if self.press:
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
                    self.squareText_r.center = (self.x+self.width/2, self.y+self.height/2)
                    DISPLAYSURF.blit (self.squareText, self.squareText_r)

        elif self.highlight:
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
                    self.squareText_r.center = (self.x+self.width/2, self.y+self.height/2)
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
                    self.squareText_r.center = (self.x+self.width/2, self.y+self.height/2)
                    DISPLAYSURF.blit (self.squareText, self.squareText_r)

    def changeText(self, text:str):
        self.text = text
    
    def changeColor(self, color):
        self.color = color
        self.highlightfactor = 50
        self.highlightcolor =(self.color[0]-self.highlightfactor if self.color[0] > self.highlightfactor else 0, 
                              self.color[1]-self.highlightfactor if self.color[1] > self.highlightfactor else 0, 
                              self.color[2]-self.highlightfactor if self.color[2] > self.highlightfactor else 0)
        
        self.pressFactor = 100
        self.pressColor = (self.color[0]-self.pressFactor if self.color[0] > self.pressFactor else 0, 
                              self.color[1]-self.pressFactor if self.color[1] > self.pressFactor else 0, 
                              self.color[2]-self.pressFactor if self.color[2] > self.pressFactor else 0)

    def collidePoint(self, mousex, mousey):
        if mousex > self.x and mousex < self.x+self.width and mousey > self.y and mousey < self.y+ self.height:
            return True

def terminate():
    pygame.quit()
    sys.exit()

def getLeaderboard():
    #Aqu[i] tambi[en habr[a demasiada sangre]]
    pass

def resetLeaderboard():
    #Poca sangre
    pass

def openGithub():
    # tambi[en poca violencia en esta funci[on]
    webbrowser.open("https://github.com/Octavioweb/Trivia-Game")


if __name__ == '__main__':
    main()