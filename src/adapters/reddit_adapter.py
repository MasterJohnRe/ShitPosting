import requests

from consts import *
from typing import Tuple


class RedditAdapter:

    def _get_top_story_title(self, http_response_text: str):
        index = http_response_text.find(KEY_TO_FIND_TOP_STORY_TITLE_HTML_TAG) + len(
            KEY_TO_FIND_TOP_STORY_TITLE_HTML_TAG)
        http_response_text = http_response_text[index:]
        story_title_start_index = http_response_text.find(KEY_TO_FIND_TOP_STORY_START_OF_TITLE) + len(
            KEY_TO_FIND_TOP_STORY_START_OF_TITLE)
        story_title_end_index = http_response_text.find(KEY_TO_FIND_TOP_STORY_END_OF_TITLE)
        top_story_title = http_response_text[story_title_start_index:story_title_end_index]
        return top_story_title

    def _get_top_story_body(self, http_response_text: str):
        index = http_response_text.find(KEY_TO_FIND_TOP_STORY_BODY_HTML_TAG)
        http_response_text = http_response_text[index:]
        story_body_start_index = http_response_text.find(KEY_TO_FIND_TOP_STORY_START_OF_BODY)
        story_body_end_index = http_response_text.find(KEY_TO_FIND_TOP_STORY_END_OF_BODY) - len(
            KEY_TO_FIND_TOP_STORY_END_OF_BODY) - REMOVE_LAST_UNWANTED_CHARACTER
        top_story_body_text = http_response_text[story_body_start_index:story_body_end_index].replace('<p>',
                                                                                                      '').replace(
            '</p>', '')
        return top_story_body_text

    def get_top_story(self, subreddit_name: str) -> Tuple[str, str]:
        subreddit_url = f"https://www.reddit.com:443/r/{subreddit_name}/top/"
        response = requests.get(subreddit_url, headers=GET_TOP_STORY_GENERIC_HEADERS,
                                cookies=GET_TOP_STORY_GENERIC_COOKIES)
        response_text = response.text
        top_story_title = self._get_top_story_title(response_text)
        top_story_body = self._get_top_story_body(response_text)
        return (top_story_title, top_story_body)
