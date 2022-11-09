import speech_recognition as sr
#instalar ffmpeg
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import matplotlib.pyplot as plt
import sys
import numpy as np
import wave

AUDIO_FOLDER = "./audios"
AUDIO_PARTS_FOLDER = AUDIO_FOLDER + "/audio_parts"


# Recibe una pista de audio y retorna la transcripcion
def audio_to_text(audio_folder=AUDIO_PARTS_FOLDER):
    text_file = open("transcribed_audio.txt", "a", encoding='utf8')
    r = sr.Recognizer()
    for audio_file in os.listdir(audio_folder):
        with sr.AudioFile(AUDIO_PARTS_FOLDER + "/" + audio_file) as source:
            audio_listened = r.listen(source)
        try:
            text = r.recognize_google(audio_listened, language="es-ES")
            print(text)
            text_file.write(text + "\n")
            os.remove(AUDIO_PARTS_FOLDER + "/" + audio_file)
        except sr.UnknownValueError:
            print("El audio es incomprensible")
        except sr.RequestError as e:
            print("No se an obtenido resultados del servidor al realizar el reconocimiento del audio")
    text_file.write("\n")
    os.rmdir(AUDIO_PARTS_FOLDER)


# Recibe una pista de audio y la retorna sin silencios
def split_by_silences(audio_file):
    init_files_system()
    # Convert to mono
    audio = AudioSegment.from_wav(audio_file)
    audio = audio.set_channels(1)
    audio.export("my_sound_mono.wav", format="wav")

    # Graph signal
    signal_wave = wave.open("my_sound_mono.wav", "r")
    graph_audio(signal_wave)
    
    audio = AudioSegment.from_wav("my_sound_mono.wav", "r")
    audio_parts = split_on_silence(audio, min_silence_len = 1000, silence_thresh = -60, keep_silence=400)
    for i, part in enumerate(audio_parts):
        part.export(AUDIO_PARTS_FOLDER + "/audio_filtered_{0}.wav".format(i), format="wav")

    


def init_files_system():
    if not os.path.exists(AUDIO_FOLDER):
        os.mkdir(AUDIO_FOLDER)
    if not os.path.exists(AUDIO_PARTS_FOLDER):
        os.mkdir(AUDIO_PARTS_FOLDER)


def process_audio(file):
    #Reduccion de ruido
    #Analisis de la reduccion de ruido
    split_by_silences(file)
    #Analisis del split por silencios
    audio_to_text()


def graph_audio(signal_wave):
    # Extract Raw Audio from Wav File
    signal = signal_wave.readframes(-1)
    signal = np.frombuffer(signal, dtype ="int16")
    fs = signal_wave.getframerate()
    # If Stereo
    if signal_wave.getnchannels() == 2:
        print("Just mono files")
        sys.exit(0)
    Time = np.linspace(0, len(signal) / fs, num=len(signal))
    plt.figure(1)
    plt.title("Signal Wave...")
    plt.plot(Time, signal)
    plt.show()


    
#Hacer que funcione en un hilo en modo demonio en tiempo real
process_audio(AUDIO_FOLDER + "/prueba_2.wav")
