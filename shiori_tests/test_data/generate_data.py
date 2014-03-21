# -*- coding: utf-8 -*-
import os
import json
import shortuuid
from datetime import datetime


def generate_data(key):
    return {
        "model": "bookmark.%s" % key,
        "pk": shortuuid.uuid(),
        "fields": {
            "%s" % key: shortuuid.uuid()
        }
    }


def generate_bookmark(owner_id, category_id, is_hide):
    return {
        "model": "bookmark.bookmark",
        "pk": shortuuid.uuid(),
        "fields": {
            "url": "http://%s.example.org/%s" % (shortuuid.uuid()[:4],
                                                 shortuuid.uuid()),
            "title": shortuuid.uuid(),
            "category": category_id,
            "description": shortuuid.uuid(),
            "owner": owner_id,
            "is_hide": is_hide
        }
    }


def bookmark_tag(id, bookmark_id, tag_id):
    return {
        "model": "bookmark.bookmark_tag",
        "pk": id,
        "fields": {
            "bookmark": bookmark_id,
            "tag": tag_id
        }
    }


def feed_subscription(owner_id, category_id):
    return {
        "model": "bookmark.feed_subscription",
        "pk": shortuuid.uuid(),
        "fields": {
            "url": "http://%s.example.org/%s" % (shortuuid.uuid()[:4],
                                                 shortuuid.uuid()),
            "name": shortuuid.uuid(),
            "owner": owner_id,
            "default_category": category_id
        }
    }


def crawling_history(feed_id):
    return {
        "model": "bookmark.crawling_history",
        "pk": shortuuid.uuid(),
        "fields": {
            "id": shortuuid.uuid(),
            "feed": feed_id,
            "update_datetime": datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S+00:00")
        }
    }


def generate_json():
    data_list = []
    for i in range(10):
        data_list.append(generate_data("category"))
        data_list.append(generate_data("tag"))
    return json.dumps(data_list)


def main():
    dirpath = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(dirpath, 'dummy_data.json')

    with open(json_path, 'w') as f:
        f.write(generate_json())


if __name__ == "__main__":
    main()
