from typing import Set
from get_data_settings.get_config import config


def get_all_chat_ids() -> Set[int]:
    return {campaign.chat_id for campaign in config.campaign}
