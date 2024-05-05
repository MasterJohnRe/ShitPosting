import subprocess

from mutagen.mp3 import MP3
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from consts import TRIMMED_VIDEO_FILE_PATH


def get_mp4_length(file_path):
    clip = VideoFileClip(file_path)
    duration = clip.duration
    clip.close()
    return duration


def get_mp3_length(file_path):
    audio = MP3(file_path)
    return audio.info.length


def trim_video(video_file_path: str, start_time: int, end_time: int) -> str:
    ffmpeg_extract_subclip(video_file_path, start_time, end_time, targetname=TRIMMED_VIDEO_FILE_PATH)
    return TRIMMED_VIDEO_FILE_PATH


def merge_video(mp4_file_path: str, mp3_file_path: str, destination_file_path: str):
    # Load the video file
    video = VideoFileClip(mp4_file_path)

    # Load the audio file
    audio = AudioFileClip(mp3_file_path)

    # Set the audio of the video file to the loaded audio file
    video_with_audio = video.set_audio(audio)

    # Write the merged video with audio to a new file
    video_with_audio.write_videofile(destination_file_path, codec="libx264",
                                     audio_codec="aac")


def apply_subtitles_on_video(input_video_file_path: str, subtitles_file_path: str, output_video_file_path: str):
    try:
        subprocess.run(
            ['ffmpeg', '-i', input_video_file_path, '-vf', f'subtitles={subtitles_file_path}', output_video_file_path])
        print(f"Subtitles added successfully to: {output_video_file_path}")
    except Exception as e:
        print(f"Error adding subtitles: {e}")
