import os
import shutil
import requests
from pydub import AudioSegment  # Install with: pip install pydub

# Define folder names
background_folder = "background/"
clear_background_flag = True  # Set to True to clear the folder contents
background_music_url = "https://example.com/path-to-music.mp3"  # Replace with a valid URL
desired_duration_minutes = 3  # Set the desired duration in minutes

# Ensure the background folder exists
if not os.path.exists(background_folder):
    os.makedirs(background_folder)
    print(f"Folder '{background_folder}' created.")
elif clear_background_flag:
    shutil.rmtree(background_folder)  # Delete the folder and its contents
    os.makedirs(background_folder)   # Recreate the empty folder
    print(f"Folder '{background_folder}' cleared.")

# Download the background music
music_file_path = os.path.join(background_folder, "background_music.mp3")
response = requests.get(background_music_url, stream=True)
if response.status_code == 200:
    with open(music_file_path, "wb") as file:
        file.write(response.content)
    print(f"Background music downloaded to '{music_file_path}'.")
else:
    print(f"Failed to download music. Status code: {response.status_code}")
    exit()

# Load the downloaded audio file
background_music = AudioSegment.from_file(music_file_path)

# Calculate the duration in milliseconds
desired_duration_ms = desired_duration_minutes * 60 * 1000

# Loop the background music to reach the desired duration
looped_music = background_music * (desired_duration_ms // len(background_music) + 1)
final_music = looped_music[:desired_duration_ms]

# Save the looped background music
final_music_file_path = os.path.join(background_folder, "looped_background_music.mp3")
final_music.export(final_music_file_path, format="mp3")
print(f"Looped background music saved to '{final_music_file_path}'.")
