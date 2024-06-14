import telegram
from telegram import InputFile

from consts import TELEGRAM_SEND_MESSAGE_TIMEOUT, TELEGRAM_SEND_VIDEO_TIMEOUT


class TelegramAdapter:
    def __init__(self, bot_token: str, channel_id: str):
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.bot = telegram.Bot(token=bot_token)

    async def send_message(self, text: str):
        async with self.bot:
            await self.bot.send_message(text=text, chat_id=self.channel_id)

    async def send_video(self, video_file_path: str):
        async with self.bot:
            with open(video_file_path, 'rb') as video_file:
                await self.bot.send_video(video=InputFile(video_file), chat_id=self.channel_id)
