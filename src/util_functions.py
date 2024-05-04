from moviepy.editor import *
from mutagen.mp3 import MP3
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from consts import TRIMMED_VIDEO_FILE_PATH, MERGED_CLIP_FILE_PATH


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


def merge_video(mp4_file_path, mp3_file_path):
    # Load the video file
    video = VideoFileClip(mp4_file_path)

    # Load the audio file
    audio = AudioFileClip(mp3_file_path)

    # Set the audio of the video file to the loaded audio file
    video_with_audio = video.set_audio(audio)

    # Write the merged video with audio to a new file
    video_with_audio.write_videofile(MERGED_CLIP_FILE_PATH, codec="libx264",
                                     audio_codec="aac")

