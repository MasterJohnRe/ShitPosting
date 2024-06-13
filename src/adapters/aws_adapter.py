import boto3
from urllib.parse import urlparse
from consts import POLLY_AUDIO_OUTPUT_FILE_PATH, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from src.exceptions import DownloadFileFromS3Error


class AWSAdapter:

    def __init__(self):
        self.polly_client = boto3.client('polly', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def initialize_session(self):
        # Initialize the Polly client
        self.polly_client = boto3.client('polly', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def create_audio_file_from_text(self, text: str) -> str:
        response = self.polly_client.synthesize_speech(
            Engine='neural',
            Text=text,
            OutputFormat='mp3',
            VoiceId='Stephen',  # Change the voice ID as needed
        )

        # Save the audio stream to a file
        with open(POLLY_AUDIO_OUTPUT_FILE_PATH, 'wb') as f:
            f.write(response['AudioStream'].read())
        return POLLY_AUDIO_OUTPUT_FILE_PATH

    def transcribe_audio(self, mp3_file_uri: str, destination_bucket_name: str, destination_file_route: str):

        transcribe = boto3.client('transcribe', region_name=AWS_REGION)

        response = transcribe.start_transcription_job(
            TranscriptionJobName='ShitPostingJob',
            Media={'MediaFileUri': mp3_file_uri},
            MediaFormat='mp3',  # Adjust according to your file format
            LanguageCode='en-US',  # Adjust according to the language of your audio
            OutputBucketName=destination_bucket_name,
            OutputKey=destination_file_route,
            Subtitles={
                'Formats': ['srt'],
                'OutputStartIndex': 1
            }
        )

        # Wait for transcription job to complete
        while True:
            status = transcribe.get_transcription_job(
                TranscriptionJobName=response['TranscriptionJob']['TranscriptionJobName'])
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break

        # return uploaded srt file uri in s3
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            srt_file_uri = f"s3://{destination_bucket_name}/{destination_file_route}.srt"
            transcribe.delete_transcription_job(TranscriptionJobName='ShitPostingJob')
            return srt_file_uri

    def upload_file_to_s3(self, file_path: str, aws_s3_bucket_name: str, aws_s3_destination_key: str):
        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file(file_path, aws_s3_bucket_name, aws_s3_destination_key)
            uploaded_file_uri = f"s3://{aws_s3_bucket_name}/{aws_s3_destination_key}"
            return uploaded_file_uri
        except Exception as e:
            raise e

    def download_file_from_s3(self, file_uri: str, destination_local_path: str):
        s3 = boto3.client('s3')
        parsed_uri = urlparse(file_uri)
        if parsed_uri.scheme != 's3':
            raise DownloadFileFromS3Error("Invalid URI scheme. Only 's3' scheme is supported.")
        bucket_name = parsed_uri.netloc
        key = parsed_uri.path.lstrip('/')
        try:
            s3.download_file(bucket_name, key, destination_local_path)
        except Exception as e:
            raise e
