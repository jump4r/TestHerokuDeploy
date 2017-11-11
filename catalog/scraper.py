from pprint import pprint
import praw
import os, sys
import django
sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), '..\\..']))
sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), '..']))
import catalog.parse, catalog.timer
from RepReviews import settings

def login():
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

    return r

def get_reviews(reddit):
    for post in reddit.subreddit("jump4r").hot(limit=15):
        print(post.title)
        scrape_post(post)

def get_reviews_from_post(reddit, post_id):
    post = praw.models.Submission(reddit, post_id)
    print (post.title)
    scrape_post(post)

def scrape_post(post):

    from catalog.models import Post, Review

    if post.link_flair_text != None:
        if post.link_flair_text.lower() in post.title.lower():
            try:
                p_exists = Post.objects.get(id=post.id)
                return
            except Post.DoesNotExist:
                pass

    elif "[review]" in post.title.lower():
        try:
            p_exists = Post.objects.get(id=post.id)
            print('Post in Database')
            return False
        except Post.DoesNotExist:
            pass

        p = Post(user=post.author.name, date=catalog.parse.parse_date(post.created), link=post.url, id=post.id, title=post.title)
        p.save()
        
        pprint(('Post: ' + str(p)))
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


def scrape_reddit():    
    reddit = login()
    return (get_reviews(reddit))

def scrape_reddit_post(post_id):
    reddit = login()
    return (get_reviews_from_post(reddit, post_id))

def check_to_scrape_post():
    if (catalog.timer.check_update_db()):
        catalog.timer.next_check = catalog.timer.update_timer()
        reddit = login()
        get_reviews(reddit)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepReviews.settings')
    django.setup()
    try:
        from catalog.models import Post, Review
        if (sys.argv[1] == None):
            reddit_posts = scrape_reddit()

        elif (sys.argv[1] != None):
            reddit_posts = scrape_reddit_post(sys.argv[1])

    except django.core.exceptions.AppRegistryNotReady:
        print('Cannot Load Models because the models are not ready')