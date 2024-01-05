import random
# Gifs para preguntas correctas
def gifts_correctos():
    gifts = ["Gifs\Correctos\Emoji con lentes.gif",
            "Gifs\Correctos\Simbolo check.gif"
            "Gifs\Correctos\check 2.gif",
            "Gifs\Correctos\Pulgar hacia arriba.gif",
            "Gifs\Correctos\Aplaudiendo.gif"]
    return random.choice(gifts)

# Gifs para preguntas incorrectas
def gifts_incorrectos():
    gifts = ["Gifs\Incorrectos\Emoji decepcionado.gif",
            "Gifs\Incorrectos\Simbolo incorrecto.gif",
            "Gifs\Incorrectos\Emoji triste.gif"]
    return random.choice(gifts)