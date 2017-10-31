from django.apps import AppConfig
import os, sys

class CatalogConfig(AppConfig):
    name = 'catalog'

    sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), 'RepScraper']))
    from catalog.streamer import Streamer

    s = Streamer()
    # s.stream()
