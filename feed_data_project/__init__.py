# Import celey app to ensure that the app is loaded when django starts

from .celery import celery_app

__all__ = ('celery_app',)
