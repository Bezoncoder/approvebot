import json
from dataclasses import dataclass
from typing import List


@dataclass
class TextButton:
    text_button: str


@dataclass
class InlineButton:
    text_button: str
    url_button: str


@dataclass
class Post:
    delay: int
    post_text: str
    path_media: str = None
    inline_buttons: List[InlineButton] = None
    text_buttons: List[TextButton] = None


@dataclass
class Campaign:
    chat_id: int
    posts: List[Post]


@dataclass
class Database:
    host: int
    user: str
    password: str
    database: str


@dataclass
class Config:
    db: Database
    bot_token: str
    admin_id: int
    campaign: List[Campaign]


def get_config(path_to_file_settings: str = 'settings.json'):
    with open(file=path_to_file_settings, mode='r', encoding='utf-8') as file:
        json_data = json.load(file)
    config_object = Config(
        db=Database(
            host=json_data['db']['host'],
            user=json_data['db']['user'],
            password=json_data['db']['password'],
            database=json_data['db']['database']
        ),
        bot_token=json_data['bot_token'],
        admin_id=json_data.get('admin_id', ''),
        campaign=[Campaign(chat_id=campaign['chat_id'],
                           posts=[Post(path_media=post.get('path_media', None),
                                       post_text=post.get('post_text', None),
                                       delay=post.get('delay', 5),
                                       text_buttons=[TextButton(text_button=button['text_button']) for button in post['text_buttons']] if post.get('text_buttons') else None,
                                       inline_buttons=[InlineButton(text_button=button['text_button'], url_button=button['url_button']) for button in post['inline_buttons']] if post.get('inline_buttons') else None) for post in campaign ['posts']]) for campaign in json_data.get('campaign', [])]
    )
    return config_object


config = get_config()
