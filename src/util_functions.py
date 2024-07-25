import subprocess

from mutagen.mp3 import MP3
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pysrt

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


def split_srt_to_one_word_per_line(input_srt_path: str, output_srt_path: str):
    # Load the original SRT file
    subs = pysrt.open(input_srt_path)

    new_subs = pysrt.SubRipFile()

    for sub in subs:
        words = sub.text.split()
        word_count = len(words)
        if word_count > 1:
            # Calculate the duration each word should be displayed
            start_time = sub.start.ordinal
            end_time = sub.end.ordinal
            total_duration = end_time - start_time
            word_duration = total_duration // word_count

            for i, word in enumerate(words):
                start = pysrt.SubRipTime(milliseconds=start_time + i * word_duration)
                end = pysrt.SubRipTime(
                    milliseconds=start_time + (i + 1) * word_duration if i < word_count - 1 else end_time)
                new_subs.append(pysrt.SubRipItem(index=len(new_subs) + 1, start=start, end=end, text=word))
        else:
            new_subs.append(sub)

    # Save the new SRT file
    new_subs.save(output_srt_path, encoding='utf-8')


def apply_subtitles_on_video(input_video_file_path: str, subtitles_file_path: str, output_video_file_path: str):
    subprocess.run(
        ['ffmpeg', '-y', '-i', input_video_file_path, '-vf',
         f"subtitles={subtitles_file_path}:force_style='Alignment=10'",
         output_video_file_path])


def split_video_by_maximum_length(video_file_path: str, video_legnth: int, maximum_time_per_video: int,
                                  target_path: str):
    number_of_pieces = int(video_legnth / maximum_time_per_video)
    remainder = video_legnth % maximum_time_per_video
    if remainder > 0:
        number_of_pieces += 1
    time_for_each_video = video_legnth / number_of_pieces
    for i in range(number_of_pieces):
        if i == 0:
            start_time = 0
            command = f"ffmpeg -y -i {video_file_path} -ss {str(start_time)}  -t  {str(time_for_each_video)} " + '"' + f"{target_path}-{str(i)}.mp4" + '"'
            os.system(command)
        else:
            start_time = (i * time_for_each_video) - 1  # let the video start before the last video ended
            command = f"ffmpeg -y -i {video_file_path} -ss {str(start_time)}  -t  {str(time_for_each_video + 1)} " + '"' + f"{target_path}-{str(i)}.mp4" + '"'
            os.system(command)
        # end_time = (i * time_for_each_video) + time_for_each_video
        # ffmpeg_extract_subclip(video_file_path, start_time, end_time, targetname=f"{target_path}-{str(i)}.mp4")
