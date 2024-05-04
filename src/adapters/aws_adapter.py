import boto3
from consts import POLLY_AUDIO_OUTPUT_FILE_PATH, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class AWSAdapter:

    def __init__(self):
        self.polly_client = boto3.client('polly', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def initialize_session(self):
        # Initialize the Polly client
        self.polly_client = boto3.client('polly', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def create_audio_file_from_text(self, text):
        response = self.polly_client.synthesize_speech(
            Engine='neural',
            Text=text,
            OutputFormat='mp3',
            VoiceId='Stephen'# Change the voice ID as needed
        )

        # Save the audio stream to a file
        with open(POLLY_AUDIO_OUTPUT_FILE_PATH, 'wb') as f:
            f.write(response['AudioStream'].read())
