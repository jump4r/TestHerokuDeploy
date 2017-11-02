from pprint import pprint
import django
import sys, os, time
sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), '..\\..']))
sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), '..']))
import catalog.parse, catalog.keywords
import praw
import threading

class Streamer:
    running = False

    def stream(self):
        r = self.login()
        thread = threading.Thread(target=self.get_from_stream, args=(r, ))
        thread.start()

    def login(self):
        try: 
            import catalog.reddit_config
            username = os.environ.get("REDDIT_USERNAME", catalog.reddit_config.username)
            password = os.environ.get('REDDIT_PASSWORD', catalog.reddit_config.password)
            client = os.environ.get('REDDIT_CLIENT_ID', catalog.reddit_config.client_id)
            secret = os.environ.get('REDDIT_CLIENT_SECRET', catalog.reddit_config.client_secret)
        except: 
            username = os.environ.get("REDDIT_USERNAME")
            password = os.environ.get('REDDIT_PASSWORD')
            client = os.environ.get('REDDIT_CLIENT_ID')
            secret = os.environ.get('REDDIT_CLIENT_SECRET')

        r = praw.Reddit(username=username,
                password=password,
                client_id=client,
                client_secret=secret,
                user_agent = "WebApp:com.jump4r.RepReviews:v0.1.0 by (/u/jump4r)")

        running = True
        return r

    def get_from_stream(self, reddit):
        pprint('starting stream')
        subreddit = reddit.subreddit('jump4r')
        for submission in subreddit.stream.submissions():
            self.process_submission(submission)
        

    def process_submission(self, post):
        try:
            from catalog.models import Post, Review
        except django.core.exceptions.AppRegistryNotReady:
            return False

        if "[review]" in post.title.lower():
            try:
                p_exists = Post.objects.get(id=post.id)
                print('Post in Database')
                return False
            except Post.DoesNotExist:
                pass

            p = Post(user=post.author.name, date=post.created, link=post.url, id=post.id, title=post.title)
            p.save()

            print(post.title + ' is not in the database, adding')
            split_selftext = post.selftext.split('\n')
            index, review_start_index, review_end_index = 0, -1, -1

            while (index < len(split_selftext)):
                if (review_start_index == review_end_index and "|" in split_selftext[index]):
                    review_start_index = index
                elif (review_start_index != review_end_index and "|" in split_selftext[index]):
                    review_end_index = index
                index += 1

            if (review_start_index == -1 or review_end_index == -1):
                return []

            r_list = catalog.parse.parse_review(split_selftext[review_start_index:review_end_index+1], p)
            for r in r_list:
                p.review_set.create(user=r.user, date=post.created, itemName=r.itemName, itemLink=r.itemLink, itemReview=r.itemReview, itemSize=r.itemSize, itemPic=r.itemPic)


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepReviews.settings')
    django.setup()

    try:
        from catalog.models import Post, Review
        streamer = Streamer()
        reddit = streamer.login()
        stream_thread = threading.Thread(target=streamer.get_from_stream, args=(reddit, ))
        stream_thread.start()
        
    except django.core.exceptions.AppRegistryNotReady:
        print('Cannot Load Models because the aps is not ready')

    print('We are in the best thread')