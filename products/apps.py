import imp
from django.apps import AppConfig
from django.conf import settings


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    def ready(self) :
       from django.contrib.auth.models import Group
       from django.db.models.signals import post_save

    #    