import requests, random, os

# The API endpoint


def Main():
    correct_answers = 0
    print(msgBienvenida)
    modoJuego = input(
        """1 para 10 preguntas
2 para jugar 15 preguntas
""")

    if modoJuego == '1':
        numPreguntas = 10
        #print(response.json())

    else:
        numPreguntas = 15
        #print(response.json())
    

    url = f"https://opentdb.com/api.php?amount={numPreguntas}&difficulty=easy&encode=url3986"

    response = requests.get(url)
    #response.encoding = 'ISO-8859-1'
    response_json = response.json()
    print(response_json)

    msgPreguntas = f"Estás jugando a {numPreguntas}!"

    for n in range(numPreguntas):
        os.system('cls')
        msgPreguntas = f"Estás jugando a {numPreguntas} preguntas!.  Pregunta : {n+1}/{numPreguntas}. Correctas = {correct_answers}/{numPreguntas}."

        print(msgPreguntas, end = '\n\n')   
        question_json = response_json['results'][n]

        question_decode = requests.utils.unquote(question_json['question'])

        print(f"Pregunta: {question_decode} \n")

    
        opciones = list(question_json['incorrect_answers'])
        correct_index = random.randint(0,len(opciones))
        opciones.insert(correct_index, str(question_json['correct_answer']))
        
        for m in range (len(opciones)):
            
            print(f"{m+1}: {requests.utils.unquote(opciones[m])}")
        

        #print(question_json)

        respuesta = int(input())-1
        #Se le quita uno a respuesta ya que se suma uno para que no se imprima un 0 en las preguntas
        
        if respuesta == correct_index:
            correct_answers+= 1

    print (f"Tuviste un total de {correct_answers}/ {numPreguntas} respuestas correctas. ¡Adios!")
    

msgBienvenida = """Bienvenido a este juego para trivia"""


if __name__ == '__main__':
    Main()


