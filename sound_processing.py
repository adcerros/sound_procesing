import speech_recognition as sr
#instalar ffmpeg
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import numpy as np
import wave
from scipy.io import wavfile
import noisereduce as nr
import whisper



AUDIO_FOLDER = "./audios"
AUDIO_PARTS_FOLDER = AUDIO_FOLDER + "/audio_parts"




def init_files_system():
    if not os.path.exists(AUDIO_FOLDER):
        os.mkdir(AUDIO_FOLDER)
    if not os.path.exists(AUDIO_PARTS_FOLDER):
        os.mkdir(AUDIO_PARTS_FOLDER)


def remove_files_system():
    for filename in os.listdir(AUDIO_PARTS_FOLDER):
        os.remove(AUDIO_PARTS_FOLDER + "/" + filename)
    os.remove("my_sound_reduced_noise.wav")
    os.remove("my_sound_mono.wav")
    os.rmdir(AUDIO_PARTS_FOLDER)


# Recibe una pista de audio y retorna la transcripcion
def audio_to_text(audio_file, text_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_listened = r.listen(source)
    try:
        text = r.recognize_google(audio_listened, language="es-ES")
        text_file.write(text + "\n")
        return text
    except sr.UnknownValueError:
        print("El audio es incomprensible")
    except sr.RequestError as e:
        print("No se an obtenido resultados del servidor al realizar el reconocimiento del audio")


# Recibe una pista de audio y retorna la transcripcion
def audio_to_text_transformer(audio_file, text_file):
    model = whisper.load_model("large")
    result = model.transcribe(audio_file)
    return result["text"]


# Recibe los fragmentos de una pista de audio y los convierte en texto
def split_audios_to_text(audio_files, text_file_dir):
    text_file = open(text_file_dir, "a", encoding='utf8')
    print(audio_files)
    text = " ".join([audio_to_text_transformer(audio_file, text_file) for audio_file in audio_files])
    text_file.write("\n")
    return text


def stereo_to_mono(audio_file):
    audio_file_mono = "my_sound_mono.wav"
    audio = AudioSegment.from_wav(audio_file)
    audio = audio.set_channels(1)
    audio.export(audio_file_mono, format="wav")
    return audio_file_mono


# Recibe una pista de audio y almacena por partes basandose en los silencios largos
# Retorna una lista de direcciones a las partes
def split_by_silences(audio_file):  
    audio = AudioSegment.from_wav(audio_file, "r")
    audio_parts = split_on_silence(audio, min_silence_len = 800, silence_thresh = -50, keep_silence=600)
    audio_parts_files = []
    for i, part in enumerate(audio_parts):
        part_name = AUDIO_PARTS_FOLDER + "/audio_filtered_{}.wav".format(i)
        part.export(part_name, format="wav")
        audio_parts_files.append(part_name)
    return audio_parts_files


def noise_reduction(file):
    new_file = "my_sound_reduced_noise.wav"
    rate, data = wavfile.read(file)
    reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=0.65)
    wavfile.write(new_file, rate, reduced_noise)
    return new_file


def process_audio(file):
    try:
        # Se inicializa la estructura de ficheros
        init_files_system()  

        # Transformacion a sonido a mono
        audio_file_mono = stereo_to_mono(file)
        
        # Reduccion de ruido
        audio_file_noise_reduction = noise_reduction(audio_file_mono)
        # Analisis de la reduccion de ruido
        # graph_audio_comparation(audio_file_mono, [audio_file_noise_reduction])

        # Normalizacion del volumen
        # Analisis de la normalizacion del volumen

        # Split por silencios
        audio_parts_files = split_by_silences(audio_file_noise_reduction)
        # Analisis del split por silencios
        graph_audio_comparation(audio_file_mono, audio_parts_files)

        # Se transforman las partes a texto y se almacena en un fichero, se retorna el texto
        text = split_audios_to_text(audio_parts_files, "transcribed_audio.txt")

        remove_files_system()

        return text
    except:
        remove_files_system()


def graph_audio(audio_file):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    plot_audio(audio_file, ax1)
    ax1.set_title("Entry signal")
    plt.show()


def plot_audio(audio_file, plot):
    signal_wave = wave.open(audio_file, "r")
    signal = signal_wave.readframes(-1)
    signal = np.frombuffer(signal, dtype ="int16")
    fs = signal_wave.getframerate()
    # If Stereo
    if signal_wave.getnchannels() >= 2:
        print("Just mono files")
        sys.exit(0)
    my_time = np.linspace(0, len(signal) / fs, num=len(signal))
    plot.plot(my_time, signal)


#Compara dos ondas de sonido graficamente
def graph_audio_comparation(audio_file, parts_files):
    # Graph signal
    gs = gridspec.GridSpec(2, len(parts_files))
    fig = plt.figure()

    ax1 = fig.add_subplot(gs[0, :])
    plot_audio(audio_file, ax1)
    ax1.set_title("Entry signal")
    
    parts_plots = []
    for i, part_file in enumerate(parts_files):
        parts_plots.append(fig.add_subplot(gs[1, i]))
        plot_audio(part_file, parts_plots[i])
        parts_plots[i].set_title("Part_" + str(i + 1))
    plt.show()

    
#Hacer que funcione en un hilo en modo demonio en tiempo real

