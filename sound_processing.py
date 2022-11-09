import speech_recognition as sr
#instalar ffmpeg
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

AUDIO_FOLDER = "./audios"
AUDIO_PARTS_FOLDER = AUDIO_FOLDER + "/audio_parts"


# Recibe una pista de audio y retorna la transcripcion
def audio_to_text(audio_folder=AUDIO_PARTS_FOLDER):
    text_file = open("transcribed_audio.txt", "a", encoding='utf8')
    # create a speech recognition object
    r = sr.Recognizer()
    for audio_file in os.listdir(audio_folder):
        # recognize the chunk
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
    audio = AudioSegment.from_wav(audio_file)
    audio_parts = split_on_silence(audio, min_silence_len = 1000, silence_thresh = -60, keep_silence=400)
    if not os.path.exists(AUDIO_FOLDER):
        os.mkdir(AUDIO_FOLDER)
    if not os.path.exists(AUDIO_PARTS_FOLDER):
        os.mkdir(AUDIO_PARTS_FOLDER)
    for i, part in enumerate(audio_parts):
        part.export(AUDIO_PARTS_FOLDER + "/audio_filtered_{0}.wav".format(i), format="wav")


def process_audio(file):
    split_by_silences(file)
    audio_to_text()


process_audio(AUDIO_FOLDER + "/prueba_2.wav")

# # a function that splits the audio file into chunks
# # and applies speech recognition
# def silence_based_conversion(path = "alice-medium.wav"):
  
#     # open the audio file stored in
#     # the local system as a wav file.
#     song = AudioSegment.from_wav(path)
  
#     # open a file where we will concatenate  
#     # and store the recognized text
#     fh = open("recognized.txt", "w+")
          
#     # split track where silence is 0.5 seconds 
#     # or more and get chunks
#     chunks = split_on_silence(song,
#         # must be silent for at least 0.5 seconds
#         # or 500 ms. adjust this value based on user
#         # requirement. if the speaker stays silent for 
#         # longer, increase this value. else, decrease it.
#         min_silence_len = 500,
  
#         # consider it silent if quieter than -16 dBFS
#         # adjust this per requirement
#         silence_thresh = -16
#     )
  
#     # create a directory to store the audio chunks.
#     try:
#         os.mkdir('audio_chunks')
#     except(FileExistsError):
#         pass
  
#     # move into the directory to
#     # store the audio files.
#     os.chdir('audio_chunks')
  
#     i = 0
#     # process each chunk
#     for chunk in chunks:
              
#         # Create 0.5 seconds silence chunk
#         chunk_silent = AudioSegment.silent(duration = 10)
  
#         # add 0.5 sec silence to beginning and 
#         # end of audio chunk. This is done so that
#         # it doesn't seem abruptly sliced.
#         audio_chunk = chunk_silent + chunk + chunk_silent
  
#         # export audio chunk and save it in 
#         # the current directory.
#         print("saving chunk{0}.wav".format(i))
#         # specify the bitrate to be 192 k
#         audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
  
#         # the name of the newly created chunk
#         filename = 'chunk'+str(i)+'.wav'
  
#         print("Processing chunk "+str(i))
  
#         # get the name of the newly created chunk
#         # in the AUDIO_FILE variable for later use.
#         file = filename
  
#         # create a speech recognition object
#         r = sr.Recognizer()
  
#         # recognize the chunk
#         with sr.AudioFile(file) as source:
#             # remove this if it is not working
#             # correctly.
#             r.adjust_for_ambient_noise(source)
#             audio_listened = r.listen(source)
  
#         try:
#             # try converting it to text
#             rec = r.recognize_google(audio_listened)
#             # write the output to the file.
#             fh.write(rec+". ")
  
#         # catch any errors.
#         except sr.UnknownValueError:
#             print("Could not understand audio")
  
#         except sr.RequestError as e:
#             print("Could not request results. check your internet connection")
  
#         i += 1
  
#     os.chdir('..')
  
  
# if __name__ == '__main__':
#     silence_based_conversion("./prueba_2.wav")