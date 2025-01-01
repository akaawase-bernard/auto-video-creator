import os
import shutil
from gtts import gTTS
from pydub import AudioSegment  # Install using: pip install pydub
from pydub.playback import play

# Define folder names
script_folder = "scripts"
audio_folder = "audio"
clear_audio_flag = True  # Set to True to clear the audio folder contents

# Ensure the audio folder exists
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)
    print(f"Folder '{audio_folder}' created.")
elif clear_audio_flag:
    shutil.rmtree(audio_folder)  # Delete the folder and its contents
    os.makedirs(audio_folder)   # Recreate the empty folder
    print(f"Folder '{audio_folder}' cleared.")

# Read text from the script file
script_file_path = os.path.join(script_folder, "script.txt")
if not os.path.exists(script_file_path):
    print(f"Script file '{script_file_path}' does not exist.")
else:
    with open(script_file_path, "r") as file:
        script_text = file.read()

    # Convert text to speech
    tts = gTTS(script_text)
    
    # Save the audio file
    temp_audio_path = os.path.join(audio_folder, "temp_output.mp3")
    tts.save(temp_audio_path)
    print(f"Audio saved to temporary file '{temp_audio_path}'.")

    # Load the audio file using pydub
    audio = AudioSegment.from_file(temp_audio_path)

    # Adjust speed (playback rate)
    speed_factor = 1.5  # Increase speed by 50%
    faster_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed_factor)
    }).set_frame_rate(audio.frame_rate)

    # Adjust pitch (change in semitones, positive for higher pitch)
    pitch_semitones = -6  # Increase pitch by 3 semitones
    pitch_audio = faster_audio._spawn(faster_audio.raw_data, overrides={
        "frame_rate": int(faster_audio.frame_rate * (2 ** (pitch_semitones / 12)))
    }).set_frame_rate(audio.frame_rate)

    # Save the adjusted audio file
    final_audio_path = os.path.join(audio_folder, "final_speech.mp3")
    pitch_audio.export(final_audio_path, format="mp3")
    print(f"Final audio saved to '{final_audio_path}'.")
