import ffmpeg
import wave
import json
from vosk import Model, KaldiRecognizer



# Function to transcribe audio using Vosk
def transcribe_audio_vosk(audio_file_path):
    model = Model("vosk-model-small-en-us-0.15")  # Replace with the path to your Vosk model

    with wave.open(audio_file_path, "rb") as audio_file:
        if audio_file.getnchannels() != 1 or audio_file.getsampwidth() != 2 or audio_file.getframerate() not in [8000, 16000, 32000, 44100, 48000]:
            raise ValueError("Audio file must be WAV format mono PCM.")

        recognizer = KaldiRecognizer(model, audio_file.getframerate())
        data = audio_file.readframes(audio_file.getnframes())

        transcription = ""
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            transcription = result['text']
            print(transcription)
            
        with open("transcribe.txt", "w") as f:
            f.write(transcription)




# Transcribe the converted audio
transcribe_audio_vosk('output_audio_mono.wav')
