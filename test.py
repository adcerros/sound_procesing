from sound_processing import process_audio


AUDIO_FOLDER = "./audios"



def test(file, expected):
    text = process_audio(file)
    if text == expected:
        print("Test correcto")
        print("Texto:", text, "\n")
        pass
    else:
        print("Error en el test")
        print("Se esperaba:", expected)
        print("Se recibe:", text, "\n")


expecteds = [   "esta es la primera prueba",
                "mañana va a llover y por qué va a llover porque hace mal tiempo",
                "estoy realizando la segunda prueba",
                "no te he entendido demasiado bien",
                "en un lugar de la Mancha de cuyo nombre no quiero acordarme no ha mucho tiempo que vivía un hidalgo de los de lanza y astillero adarga antigua rocín flaco y galgo corredor"]

for i, expected in enumerate(expecteds):
    test(AUDIO_FOLDER + "/prueba_{0}.wav".format(i + 1), expected)

