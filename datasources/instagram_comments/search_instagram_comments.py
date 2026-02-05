"""
Import scraped Instagram comment data
"""
from datetime import datetime
from urllib.parse import urlsplit

from backend.lib.search import Search
from common.lib.item_mapping import MappedItem
from common.lib.helpers import normalize_url_encoding


class SearchInstagramComments(Search):
    """
    Import scraped Instagram comment data
    """
    type = "instagram-comments-search"  # job ID
    category = "Search"  # category
    title = "Import scraped Instagram comment data"  # title displayed in UI
    description = \
        "Import Instagram comment data collected with an external " \
        "tool such as Zeeschuimer."  # description displayed in UI
    extension = "ndjson"  # extension of result file, used internally and in UI
    is_from_zeeschuimer = True

    # not available as a processor for existing datasets
    accepts = [None]
    references = [
        "[Zeeschuimer browser extension]"
        "(https://github.com/digitalmethodsinitiative/zeeschuimer)"
    ]

    def get_items(self, query):
        """
        Run custom search

        Not available for Instagram comments
        """
        raise NotImplementedError(
            "Instagram comment datasets can only be created by importing data "
            "from elsewhere"
        )

    @staticmethod
    def map_item(item):
        url = normalize_url_encoding(
            item.get("__import_meta", {}).get("source_platform_url", "")
        )  # Zeeschuimer metadata
        path_parts = urlsplit(url).path.rstrip("/").split("/p/")
        thread_id = path_parts[1] if len(path_parts) > 1 else ""

        return MappedItem({
            "collected_from_url": url,
            "id": item["pk"],
            "thread_id": thread_id,
            "timestamp":
                datetime
                .fromtimestamp(item["created_at"])
                .strftime("%Y-%m-%d %H:%M:%S"),
            "author": item["user"]["username"],
            "author_full": item["user"].get("full_name", ""),
            "body": item["text"],
            "verified": item["user"].get("is_verified", ""),
            "author_is_mentionable": item["user"].get("is_mentionable", ""),
            "author_is_private": item["user"].get("is_private", ""),
            "author_avatar_url": item["user"]["profile_pic_url"],
            "num_likes": item["comment_like_count"],
            "num_replies": item.get("child_comment_count", ""),
            "is_reply": "parent_comment_id" in item,
            "reply_to": item.get("parent_comment_id", ""),
            "is_liked_by_media_owner": item.get("is_liked_by_media_owner", ""),
            "is_edited": item.get("is_edited", ""),
            "is_ranked_comment": item.get("is_ranked_comment", ""),
            "liked_by_media_coauthors": ",".join(
                item.get("liked_by_media_coauthors", [])
            ),
            "unix_timestamp": item["created_at"]
        })
