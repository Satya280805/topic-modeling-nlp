"""
topic_app/apps.py

AppConfig registers our app with Django's application registry.
Django reads this when it boots up to know the app's full name and metadata.
"""

from django.apps import AppConfig


class TopicAppConfig(AppConfig):
    # The default auto-generated primary key type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # Must match the folder name of the app exactly
    name = 'topic_app'

    # Human-readable name shown in Django admin
    verbose_name = 'Topic Modeling App'
