import requests, random

class GameEngine(object):
    def __init__(self):
        self.correct_answers = 0
        print("""Bienvenido a este juego de trivia""")

    def startGame(self, gameMode):
        self.numPreguntas = gameMode
        self.url = f"https://opentdb.com/api.php?amount={self.numPreguntas}&difficulty=easy&encode=url3986"

        self.response = self.requests.get(self.url)
        #response.encoding = 'ISO-8859-1'
        self.response_json = self.response.json()
        self.questionIndex = -1
        print(self.response_json)

    def nextQuestion(self):
        self.questionIndex +=1
        self.question_json = self.response_json['results'][self.questionIndex]
        self.question_decode = requests.utils.unquote(self.question_json['question'])

        self.opciones = list(self.question_json['incorrect_answers'])
        self.correct_index = random.randint(0,len(self.opciones))
        self.opciones.insert(self.correct_index, str(self.question_json['correct_answer']))

        return {'opciones': self.opciones}
    
    def checkAnswer(self, answer):
        if answer == self.correct_index:
            self.correct_answers +=1

    def getStats(self):
        #msgPreguntas = f"Estás jugando a {numPreguntas} preguntas!.  Pregunta : {n+1}/{numPreguntas}. Correctas = {correct_answers}/{numPreguntas}."
        return {'numPreguntas': self.numPreguntas, 'nPregunta': self.questionIndex, 'correctas':self.correct_answers}





# def Main():
#     correct_answers = 0
#     print(msgBienvenida)
#     modoJuego = input(
#         """1 para 10 preguntas
# 2 para jugar 15 preguntas
# """)

#     if modoJuego == '1':
#         numPreguntas = 10
#         #print(response.json())

#     else:
#         numPreguntas = 15
#         #print(response.json())
    
#     url = f"https://opentdb.com/api.php?amount={numPreguntas}&difficulty=easy&encode=url3986"

#     response = requests.get(url)
#     #response.encoding = 'ISO-8859-1'
#     response_json = response.json()
#     print(response_json)

#     msgPreguntas = f"Estás jugando a {numPreguntas}!"

#     for n in range(numPreguntas):
#         os.system('cls')
#         msgPreguntas = f"Estás jugando a {numPreguntas} preguntas!.  Pregunta : {n+1}/{numPreguntas}. Correctas = {correct_answers}/{numPreguntas}."

#         print(msgPreguntas, end = '\n\n')   
#         question_json = response_json['results'][n]

#         question_decode = requests.utils.unquote(question_json['question'])

#         print(f"Pregunta: {question_decode} \n")

    
#         opciones = list(question_json['incorrect_answers'])
#         correct_index = random.randint(0,len(opciones))
#         opciones.insert(correct_index, str(question_json['correct_answer']))
        
#         for m in range (len(opciones)):
            
#             print(f"{m+1}: {requests.utils.unquote(opciones[m])}")
        

#         #print(question_json)

#         respuesta = int(input())-1
#         #Se le quita uno a respuesta ya que se suma uno para que no se imprima un 0 en las preguntas
        
#         if respuesta == correct_index:
#             correct_answers+= 1

#     print (f"Tuviste un total de {correct_answers}/ {numPreguntas} respuestas correctas. ¡Adios!")
    

# msgBienvenida = """Bienvenido a este juego para trivia"""


# if __name__ == '__main__':
#     Main()


