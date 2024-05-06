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
KEY_TO_FIND_TOP_STORY_TITLE_HTML_TAG = f'slot="title"'
KEY_TO_FIND_TOP_STORY_START_OF_TITLE = '>'
KEY_TO_FIND_TOP_STORY_END_OF_TITLE = '<'
REMOVE_LAST_UNWANTED_CHARACTER = 1

POLLY_AUDIO_OUTPUT_FILE_PATH = "./media/polly_audio_output.mp3"
# AWS credentials and region
AWS_ACCESS_KEY_ID = 'AKIAWO5H2OD3OERIK3XM'
AWS_SECRET_ACCESS_KEY = '3YvZ+2UoFjeFDFOgCEXiXbKYQY0ofs7OsAfdqjFX'
AWS_REGION = 'eu-west-2'  # Change this to your AWS region
AWS_S3_BUCKET_NAME = "shitposting-audio-files"
AWS_MP3_POLLY_OUTPUT_FILE_ROUTE = "audio_created_by_polly/polly_output_audio.mp3"
AWS_SRT_TRABSCRIBE_OUTPUT_FILE_ROUTE = "srt_created_by_transcribe/transcribe_output"

TRIMMED_VIDEO_FILE_PATH = "./media/trimmed_video.mp4"
BASE_VIDEOS_FOLDER_PATH = r"C:\Users\Amit\Downloads\videos"  # TODO: edit this on production
MERGED_CLIP_FILE_PATH = "./media/merged_clip_without_subtitles.mp4"
TRANSCRIBE_SRT_FILE_DESTINATION_PATH = "./media/transcribe_subtitles_output.srt"
VIDEO_WITH_SUBTITLES_FILE_PATH = "./media/video_with_subtitles.mp4"
RESULT_VIDEOS_FOLDER_PATH = "./media/videos_to_upload/"
MAXIMUM_TIME_PER_VIDEO = 60
STORY_TITLE_INDEX = 0