from __future__ import absolute_import, unicode_literals
from .celery_app import app as celery_app  # noqa

default_app_config = "skud.apps.SkudAppConfig"
