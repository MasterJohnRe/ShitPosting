from typing import Tuple
import random
import math
import logging
import os
import re

from src import log_config
from src.adapters.reddit_adapter import RedditAdapter
from src.adapters.aws_adapter import AWSAdapter
from src import util_functions
from consts import *

STORY_BODY_INDEX = 1

log_config.setup_logging()
logger = logging.getLogger(__name__)


def get_top_story():
    try:
        aita_subreddit_url = "AmItheAsshole"
        reddit_adapter = RedditAdapter()
        story_tuple = reddit_adapter.get_top_story(aita_subreddit_url)
        logger.info(f"got top story: {story_tuple[STORY_TITLE_INDEX]}")
        return story_tuple
    except Exception as e:
        logger.Error(f"Failed getting top story: {e}")
        raise e


def create_audio_file_from_text(aws_adapter, story_tuple: Tuple[str, str]):
    try:
        polly_output_audio_file_path = aws_adapter.create_audio_file_from_text(story_tuple[STORY_BODY_INDEX])
        logger.info(FINISHED_CREATING_AUDIO_FILE_FROM_TEXT_MESSAGE)
        return polly_output_audio_file_path
    except Exception as e:
        logger.error(f"failed creating audio file from text: {e}")
        raise e


def get_mp3_length(audio_file_path: str):
    try:
        return util_functions.get_mp3_length(audio_file_path)
    except Exception as e:
        logging.error(f"failed getting mp3 length. error: {e}")
        raise e


def trim_video_by_random_start_point(video_file_path, mp3_length):
    try:
        maximum_start_of_video = util_functions.get_mp4_length(video_file_path) - mp3_length
        random_video_start = math.floor(random.randint(0, int(maximum_start_of_video)))
        logger.info(TRIMMED_VIDEO_BY_RANDOM_START_POINT_SUCCESSFULLY_MESSAGE)
        return util_functions.trim_video(video_file_path, random_video_start, random_video_start + mp3_length)
    except Exception as e:
        logger.error(
            f"failed trimming video by random start point. video_file_path: {video_file_path}, mp3_length: {mp3_length}, Error: {e}")
        raise e


def merge_video(mp4_file_path: str, mp3_file_path: str, destination_file_path: str):
    try:
        util_functions.merge_video(mp4_file_path, mp3_file_path, destination_file_path)
        logging.info("finished merging the video")
    except Exception as e:
        logging.error(
            f"failed merging the video with the audio file. mp4_file_path: {mp4_file_path}, mp3_file_path: {mp3_file_path}, destination_file_path: {destination_file_path}. with the error: {e}")
        raise e


def get_random_video_from_bank():
    video_files = [file_name for file_name in os.listdir(BASE_VIDEOS_FOLDER_PATH) if
                   os.path.isfile(os.path.join(BASE_VIDEOS_FOLDER_PATH, file_name))]
    if video_files:
        logger.info(GOT_RANDOM_VIDEO_SUCCESSFULY_MESSAGE)
        return os.path.join(BASE_VIDEOS_FOLDER_PATH, random.choice(video_files))
    else:
        logger.error(f"{FAILED_GETTING_RANDOM_VIDEO_MESSAGE}. for the path: {BASE_VIDEOS_FOLDER_PATH}")
        raise Exception  # TODO: replace this with custom exception


def create_subtitles_from_mp3(aws_adapter, polly_output_audio_file_path):
    try:
        mp3_file_uri_in_s3 = aws_adapter.upload_file_to_s3(polly_output_audio_file_path, AWS_S3_BUCKET_NAME,
                                                           AWS_MP3_POLLY_OUTPUT_FILE_ROUTE)
        srt_file_uri_in_s3 = aws_adapter.transcribe_audio(mp3_file_uri_in_s3, AWS_S3_BUCKET_NAME,
                                                          AWS_SRT_TRABSCRIBE_OUTPUT_FILE_ROUTE)
        aws_adapter.download_file_from_s3(srt_file_uri_in_s3, TRANSCRIBE_SRT_FILE_DESTINATION_PATH)
        logger.info(CREATED_SRT_FILE_SUCCESSFULLY_MESSAGE)
    except Exception as e:
        logger.error(
            f"failed creating subtitles from mp3. polly_output_audio_file_path: {polly_output_audio_file_path} Error: {e} ")
        raise e


def apply_subtitles_on_video(input_video_file_path: str, subtitles_file_path: str, output_video_file_path: str):
    try:
        util_functions.apply_subtitles_on_video(input_video_file_path, subtitles_file_path, output_video_file_path)
        logger.info(
            f"applied subtitles: {subtitles_file_path} on video: {input_video_file_path}. result video placed in: {output_video_file_path}")
    except Exception as e:
        logger.error(
            f"failed applying subtitles: {subtitles_file_path} on video: {input_video_file_path}. result video placed in: {output_video_file_path}. error: {e}")


def get_valid_path(folder_path: str):
    pattern = r'[\\/:*?"<>|]'
    folder_name = folder_path.rsplit('/', 1)[1]
    folder_path_without_name = folder_path.rsplit('/', 1)[0]
    new_folder_name = re.sub(pattern, '', folder_name)
    new_folder_path = folder_path_without_name + '/' + new_folder_name
    return new_folder_path


def split_video_by_maximum_length(video_file_path: str, video_legnth: int, maximum_time_per_video: int,
                                  target_path: str):
    try:
        target_folder_path = target_path.rsplit('/', 1)[0]
        target_folder_path = get_valid_path(target_folder_path)
        os.makedirs(target_folder_path, exist_ok=True)
        target_path = target_folder_path + '/' + target_path.rsplit('/', 1)[TARGET_VIDEO_NAME_POSITION]
        target_path = get_valid_path(target_path)
        util_functions.split_video_by_maximum_length(video_file_path, video_legnth, maximum_time_per_video, target_path)
        logger.info(f"{SPLITTED_RESULT_VIDEO_SUCCSSFULLY_MESSAGE}. placed in folder: {target_path}")
    except Exception as e:
        logging.error(
            f"failed splitting video. video_file_path: {video_file_path}, video_length: {video_legnth}, maximum_time_per_video: {maximum_time_per_video}, target_path: {target_path}. with the error: {e}")


def create_video():
    logger.info("---started creating video task---")
    aws_adapter = AWSAdapter()
    story_tuple = get_top_story()
    output_audio_file_path = create_audio_file_from_text(aws_adapter, story_tuple)
    random_video_file_path = get_random_video_from_bank()
    mp3_length = get_mp3_length(output_audio_file_path)
    trimmed_video_file_path = trim_video_by_random_start_point(random_video_file_path, mp3_length)
    merge_video(trimmed_video_file_path, output_audio_file_path, MERGED_CLIP_FILE_PATH)
    # mp3_length = 165
    # story_tuple = ("how I met your mother, part me", "test")
    create_subtitles_from_mp3(aws_adapter, "D:\git\ShitPosting\media\polly_audio_output.mp3")
    apply_subtitles_on_video(MERGED_CLIP_FILE_PATH, TRANSCRIBE_SRT_FILE_DESTINATION_PATH,
                             VIDEO_WITH_SUBTITLES_FILE_PATH)
    # mp3_length = 64
    # story_tuple = ("AITA for telling my daughter that life isn’t highschool and if it was she would be the loser now",
    #                "AITA for telling my daughter that life isn’t highschool and if it was she would be the loser now")
    split_video_by_maximum_length(VIDEO_WITH_SUBTITLES_FILE_PATH, mp3_length, MAXIMUM_TIME_PER_VIDEO,
                                  f"{RESULT_VIDEOS_FOLDER_PATH}{story_tuple[STORY_TITLE_INDEX]}/{story_tuple[STORY_TITLE_INDEX]}")


def main():
    create_video()


if __name__ == "__main__":
    main()
