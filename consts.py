GET_TOP_STORY_GENERIC_COOKIES = {"edgebucket": "whqdLUny3GkZu5z94Z",
                                 "loid": "000000000znlxhg8jx.2.1714819605801.Z0FBQUFBQm1OaElWWEhMTDQ2bEZ0cXF4ODlQa2xFNXRsUVhzZ3B5WC1CSzI4RlVuOFE5SjRwVEl6cGxIMnNFOXJNempZT0pQQXVzcU5Kd0VINnFMdWVWcUdiakdkZnU0TDBsTkt6b24tb0Vkc0FsaS1jLVo2Ym5meHg1Z25vSzZyN3dycTVjWlgxRXk"}
GET_TOP_STORY_GENERIC_HEADERS = {"Sec-Ch-Ua": "\"Chromium\";v=\"123\", \"Not:A-Brand\";v=\"8\"",
                                 "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"",
                                 "Upgrade-Insecure-Requests": "1",
                                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36",
                                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                 "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                                 "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br",
                                 "Accept-Language": "en-US,en;q=0.9", "Priority": "u=0, i"}

KEY_TO_FIND_TOP_STORY_BODY_HTML_TAG = 'data-post-click-location="text-body"'
KEY_TO_FIND_TOP_STORY_START_OF_BODY = '<p>'
KEY_TO_FIND_TOP_STORY_END_OF_BODY = '</div>'
KEY_TO_FIND_TOP_STORY_TITLE_HTML_TAG = f'post-title'
KEY_TO_FIND_TOP_STORY_START_OF_TITLE = '"'
KEY_TO_FIND_TOP_STORY_END_OF_TITLE = '"'
REMOVE_LAST_UNWANTED_CHARACTER = 1

POLLY_AUDIO_OUTPUT_FILE_PATH = "./media/polly_audio_output.mp3"
# AWS credentials and region
AWS_ACCESS_KEY_ID = ${{ secrets.AWS_ACCESS_KEY_ID }}
AWS_SECRET_ACCESS_KEY = ${{ secrets.AWS_SECRET_ACCESS_KEY }}
AWS_REGION = 'eu-west-2'  # Change this to your AWS region
AWS_S3_BUCKET_NAME = "shitposting-audio-files"
AWS_MP3_POLLY_OUTPUT_FILE_ROUTE = "audio_created_by_polly/polly_output_audio.mp3"
AWS_SRT_TRABSCRIBE_OUTPUT_FILE_ROUTE = "srt_created_by_transcribe/transcribe_output"

TRIMMED_VIDEO_FILE_PATH = "./media/trimmed_video.mp4"
BASE_VIDEOS_FOLDER_PATH = "./media/random_background_videos"
MERGED_CLIP_FILE_PATH = "./media/merged_clip_without_subtitles.mp4"
TRANSCRIBE_SRT_FILE_DESTINATION_PATH = "./media/transcribe_subtitles_output.srt"
FIXED_SRT_FILE_DESTINATION_PATH = "./media/fixed_subtitles.srt"
VIDEO_WITH_SUBTITLES_FILE_PATH = "./media/video_with_subtitles.mp4"
RESULT_VIDEOS_FOLDER_PATH = "./media/videos_to_upload/"
MAXIMUM_TIME_PER_VIDEO = 60
STORY_TITLE_INDEX = 0
TARGET_VIDEO_NAME_POSITION = 1

FINISHED_CREATING_AUDIO_FILE_FROM_TEXT_MESSAGE = "finished creating audio file from text"
TRIMMED_VIDEO_BY_RANDOM_START_POINT_SUCCESSFULLY_MESSAGE = "trimmed video by random start point successfully"
GOT_RANDOM_VIDEO_SUCCESSFULY_MESSAGE = "get_random_video_from_bank finished successfully"
FAILED_GETTING_RANDOM_VIDEO_MESSAGE = "get_random_video_from_bank failed"
CREATED_SRT_FILE_SUCCESSFULLY_MESSAGE = "created srt file from mp3"
SPLITTED_RESULT_VIDEO_SUCCSSFULLY_MESSAGE = "splitted result video successfully"
COPIED_RESULT_VIDEO_TO_RESULT_FOLDER_SUCCESSFULLY_MESSAGE = "copied video_with_subtitles successfully"
UPLOADED_VIDEO_TO_TELEGRAM_SUCCESSFULLY_MESSAGE = "uploaded video to telegram successfully"

# TELEGRAM consts:
BOT_TOKEN = '7076637719:AAGyX-LZ3RywPHvaQ892soCu8RRdUj4pwWw'
CHANNEL_CHAT_ID = '-1002232945611'
TELEGRAM_SEND_MESSAGE_TIMEOUT = 10
TELEGRAM_SEND_VIDEO_TIMEOUT = 50
