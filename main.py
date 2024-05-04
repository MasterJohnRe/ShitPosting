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


def create_audio_file_from_text(story_tuple: Tuple[str, str]):
    aws_adapter = AWSAdapter()
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


def main():
    story_tuple = get_top_story()
    output_audio_file_path = create_audio_file_from_text(story_tuple)
    mp3_length = get_mp3_length(output_audio_file_path)
    random_video_file_path = get_random_video_from_bank()
    trimmed_video_file_path = trim_video_by_random_start_point(random_video_file_path, mp3_length)
    merge_video(trimmed_video_file_path, output_audio_file_path)
    # print(trimmed_video_file_path)


if __name__ == "__main__":
    main()
