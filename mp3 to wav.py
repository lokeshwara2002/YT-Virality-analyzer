import ffmpeg

# Function to convert any audio format to mono PCM WAV
def convert_to_mono_pcm(input_audio, output_audio):
    try:
        ffmpeg.input(input_audio).output(output_audio, ac=1, ar=16000).overwrite_output().run()
        print(f"Conversion successful: {output_audio}")
    except ffmpeg.Error as e:
        print(f"Error occurred: {e}")
        raise

# Example usage:
# Convert any audio format (e.g., .mp3, .wav) to mono PCM WAV
convert_to_mono_pcm('audio.mp3', 'output_audio_mono.wav')
