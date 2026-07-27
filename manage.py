#!/usr/bin/env python
"""
manage.py

Django's command-line utility for administrative tasks.

Usage examples:
    python manage.py runserver          ← Start development server
    python manage.py makemigrations     ← Create DB migration files
    python manage.py migrate            ← Apply migrations to DB
    python manage.py createsuperuser    ← Create admin user
    python manage.py shell              ← Open interactive Django shell
"""

import os
import sys


def main():
    """Run administrative tasks."""

    # Tell Django which settings module to use
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'topic_modeling_project.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Pass all command-line arguments to Django's management command executor
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
