from catalog.streamer import Streamer
import os 

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepReviews.settings')

    s = Streamer()
    s.stream()