from typing import Tuple
import random
import math

from src.adapters.reddit_adapter import RedditAdapter
from src.adapters.aws_adapter import AWSAdapter
from src.util_functions import *
from consts import *

STORY_BODY_INDEX = 1


def get_top_story():
    aita_subreddit_url = "AmItheAsshole"
    reddit_adapter = RedditAdapter()
    story_tuple = reddit_adapter.get_top_story(aita_subreddit_url)
    return story_tuple


def create_audio_file_from_text(aws_adapter, story_tuple: Tuple[str, str]):
    polly_output_audio_file_path = aws_adapter.create_audio_file_from_text(story_tuple[STORY_BODY_INDEX])
    return polly_output_audio_file_path


def trim_video_by_random_start_point(video_file_path, mp3_length):
    maximum_start_of_video = get_mp4_length(video_file_path) - mp3_length
    random_video_start = math.floor(random.randint(0, int(maximum_start_of_video)))
    return trim_video(video_file_path, random_video_start, random_video_start + mp3_length)


def get_random_video_from_bank():
    video_files = [file_name for file_name in os.listdir(BASE_VIDEOS_FOLDER_PATH) if
                   os.path.isfile(os.path.join(BASE_VIDEOS_FOLDER_PATH, file_name))]
    if video_files:
        return os.path.join(BASE_VIDEOS_FOLDER_PATH, random.choice(video_files))
    else:
        return None


def create_subtitles_from_mp3(aws_adapter, polly_output_audio_file_path):
    mp3_file_uri_in_s3 = aws_adapter.upload_file_to_s3(polly_output_audio_file_path, AWS_S3_BUCKET_NAME,
                                                       AWS_MP3_POLLY_OUTPUT_FILE_ROUTE)
    srt_file_uri_in_s3 = aws_adapter.transcribe_audio(mp3_file_uri_in_s3, AWS_S3_BUCKET_NAME,
                                                      AWS_SRT_TRABSCRIBE_OUTPUT_FILE_ROUTE)
    aws_adapter.download_file_from_s3(srt_file_uri_in_s3, TRANSCRIBE_SRT_FILE_DESTINATION_PATH)


def main():
    aws_adapter = AWSAdapter()
    # story_tuple = get_top_story()
    # output_audio_file_path = create_audio_file_from_text(aws_adapter, story_tuple)
    # mp3_length = get_mp3_length(output_audio_file_path)
    # random_video_file_path = get_random_video_from_bank()
    # trimmed_video_file_path = trim_video_by_random_start_point(random_video_file_path, mp3_length)
    # merge_video(trimmed_video_file_path, output_audio_file_path)
    # create_video_with_subtitles(aws_adapter, output_audio_file_path)
    create_subtitles_from_mp3(aws_adapter, "D:\git\ShitPosting\media\polly_audio_output.mp3")
    # print(trimmed_video_file_path)


if __name__ == "__main__":
    main()
