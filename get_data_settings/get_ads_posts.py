import logging
from typing import Optional, List
from get_data_settings.get_config import config, Post

logger = logging.getLogger(__name__)


def get_posts_by_chat_id(target_chat_id: int) -> Optional[List[Post]]:
    for campaign in config.campaign:
        if campaign.chat_id == target_chat_id:
            logger.info(f'Posts found for chat ID {target_chat_id}.')
            return campaign.posts
    logger.warning(f'No posts found for chat ID {target_chat_id}.')
    return []
