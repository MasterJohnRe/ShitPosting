import boto3
from consts import POLLY_AUDIO_OUTPUT_FILE_PATH, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, \
    AWS_S3_BUCKET_NAME, AWS_MP3_POLLY_OUTPUT_FILE_ROUTE


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

    def transcribe_audio(self, file_uri):
        transcribe = boto3.client('transcribe', region_name=AWS_REGION)

        response = transcribe.start_transcription_job(
            TranscriptionJobName='ShitPostingJob',
            Media={'MediaFileUri': file_uri},
            MediaFormat='mp3',  # Adjust according to your file format
            LanguageCode='en-US',  # Adjust according to the language of your audio
            OutputFormat='srt'
        )

        # Wait for transcription job to complete
        while True:
            status = transcribe.get_transcription_job(
                TranscriptionJobName=response['TranscriptionJob']['TranscriptionJobName'])
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break

        # Get transcription results
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            pass

    def upload_file(self, file_path):
        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file(file_path, AWS_S3_BUCKET_NAME, AWS_MP3_POLLY_OUTPUT_FILE_ROUTE)
            print(
                f"File uploaded successfully to S3 bucket '{AWS_S3_BUCKET_NAME}' with key '{AWS_MP3_POLLY_OUTPUT_FILE_ROUTE}'")
            uploaded_file_uri = "s3://shitposting-audio-files/" + AWS_MP3_POLLY_OUTPUT_FILE_ROUTE
            return uploaded_file_uri
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
