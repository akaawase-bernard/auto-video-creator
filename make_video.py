import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import time

# Define folder names
video_folder = "videos"
audio_folder = "audio"
work_folder = "work"  # Folder where 3-second clips will be saved
output_folder = "final_video"

# Ensure the work folder exists, where we will store the 3-second clips
if not os.path.exists(work_folder):
    os.makedirs(work_folder)
    print(f"Folder '{work_folder}' created.")

# Ensure the output folder exists for the final video
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Folder '{output_folder}' created.")

# Load the final speech audio
final_speech_path = os.path.join(audio_folder, "final_speech.mp3")
audio = AudioFileClip(final_speech_path)

# Get the duration of the final audio (in seconds)
audio_duration = audio.duration
print('The audio is ', audio_duration)

#time.sleep(10)

# Define desired dimensions (e.g., 1920x1080 for landscape)
desired_width = 1920
desired_height = 1080

# Randomly select video files from the videos folder
video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]

# Trim each video into 3-second clips and save them to the work folder
clip_duration = 3  # seconds
for video_file in video_files:
    video_path = os.path.join(video_folder, video_file)
    video_clip = VideoFileClip(video_path)

    # Get the total duration of the video
    video_duration = video_clip.duration

    # Split the video into 3-second clips
    for start_time in range(0, int(video_duration), clip_duration):
        end_time = min(start_time + clip_duration, video_duration)
        subclip = video_clip.subclip(start_time, end_time)

        # Resize the clip to the desired dimensions
        resized_clip = subclip.resize(newsize=(desired_width, desired_height))

        # Save the resized subclip to the work folder
        clip_filename = os.path.join(work_folder, f"{video_file}_clip_{start_time}_{end_time}.mp4")
        resized_clip.write_videofile(clip_filename, codec="libx264", audio_codec="aac", fps=24)

# Load all the 3-second clips from the work folder
clip_files = [f for f in os.listdir(work_folder) if f.endswith('.mp4')]

# Check if there are enough clips to match the audio duration
if len(clip_files) == 0:
    raise ValueError("No clips found in the work folder!")

# Select a random number of clips to concatenate based on the audio duration
n_clips = int(audio_duration / clip_duration)

# Ensure there are enough clips, or repeat the clips if necessary
if len(clip_files) < n_clips:
    print(f"Not enough clips. Repeating the available clips to reach {n_clips} clips.")
    clip_files = clip_files * (n_clips // len(clip_files)) + clip_files[:n_clips % len(clip_files)]
else:
    clip_files = random.sample(clip_files, n_clips)

# Load the selected clips and apply fade effects
clips = []
for clip_file in clip_files:
    clip_path = os.path.join(work_folder, clip_file)
    clip = VideoFileClip(clip_path)
    
    # Apply fade-in and fade-out effects
    faded_clip = clip.crossfadein(0.5).crossfadeout(0.5)
    clips.append(faded_clip)

# Concatenate the clips with fade effects
final_video = concatenate_videoclips(clips, method="compose", padding=-0.5)

# Resize the final video to match the audio duration (set the final video duration to the audio duration)
final_video = final_video.subclip(0, audio_duration)

# Set the audio of the final video to be the final speech
final_video = final_video.set_audio(audio)

# Save the final combined video
final_video_path = os.path.join(output_folder, "final_video.mp4")
final_video.write_videofile(final_video_path, codec="libx264", audio_codec="aac", fps=24)

print(f"Final video saved to '{final_video_path}'.")

# # Load the selected clips and concatenate them
# clips = []
# for clip_file in clip_files:
#     clip_path = os.path.join(work_folder, clip_file)
#     clip = VideoFileClip(clip_path)
#     clips.append(clip)

# # Concatenate the clips to form the final video with "compose" method to handle different resolutions or frame rates
# final_video = concatenate_videoclips(clips, method="compose")

# # Resize the final video to match the audio duration (set the final video duration to the audio duration)
# final_video = final_video.subclip(0, audio_duration)

# # Set the audio of the final video to be the final speech
# final_video = final_video.set_audio(audio)

# # Save the final combined video
# final_video_path = os.path.join(output_folder, "final_video.mp4")
# final_video.write_videofile(final_video_path, codec="libx264", audio_codec="aac", fps=24)

# print(f"Final video saved to '{final_video_path}'.")
