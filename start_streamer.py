from catalog.streamer import Streamer
import catalog.scraper
import os 

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepReviews.settings')

    try:
        from catalog.models import Post, Review
        if (sys.argv[1] == 'stream'):
             s = Streamer()
             s.stream()

        elif (sys.argv[1] == 'scrape'):
            r = catalog.scraper.scrape_reddit_post(sys.argv[2])

    except:
        pass