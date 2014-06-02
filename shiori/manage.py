# -*- coding: utf-8 -*-
"""
 manager of django.
 'DJANGO_SETTINGS_MODULES' has changed from in default.
"""
import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shiori.core.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
