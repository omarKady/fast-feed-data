# To integrate Celery with django we must first define an instance of Celery library

import os
from celery import Celery

# Using os module set the default django settings module for 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feed_data_project.settings')

# Instantiate an instance of the Celery class to create the celery_app instance variable
celery_app = Celery('feed_data_project')

# Update the Celery application's configuration with settings I will soon
#  place in the Django project's settings file identifiable with a 'CELERY_' prefix
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules (task.py) from all registered Django apps in our project
celery_app.autodiscover_tasks()
