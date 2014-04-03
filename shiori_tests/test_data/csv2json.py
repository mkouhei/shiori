# -*- coding: utf-8 -*-
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shiori_tests.settings")
from django.contrib.auth.models import User


def convert_format(row):
    return {
        "model": "auth.user",
        "pk": int(row[0]),
        "fields": {
            "first_name": row[1],
            "last_name": row[2],
            "username": row[4],
            "email": row[3],
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "password": convert_hash_password(row[5])
        }
    }


def convert_hash_password(plaintext_password):
    u = User()
    u.set_password(plaintext_password)
    return u.password


def main():
    dirpath = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(dirpath, 'FakeNameGenerator.com_2a6e893c.csv')
    json_path = os.path.join(dirpath, 'dummy_users.json')
    if sys.version_info < (3, 0):
        with open(csv_path, 'rb') as f:
            reader = csv.reader(f)
            with open(json_path, 'w') as f:
                f.write(json.dumps([convert_format(row) for row in reader
                                    if row[0] != '\xef\xbb\xbfNumber']))
    else:
        with open(csv_path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f)
            with open(json_path, 'w') as f:
                f.write(json.dumps([convert_format(row) for row in reader
                                    if row[0] != '\ufeffNumber']))


if __name__ == "__main__":
    main()
