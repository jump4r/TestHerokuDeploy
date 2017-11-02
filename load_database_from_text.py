from pprint import pprint
import django
import sys, os, time
import re
sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), '..\\..']))
sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), '..']))

def run():
    load_posts()
    load_reviews()

def load_posts():
    text_file = open('load_posts.txt', 'r')
    lines = text_file.readlines()
    for line in lines:
        sub = re.sub(' +', ' ', line)
        s = sub.split('\t')
        user = s[0][1:len(s[0])-1]
        link = s[1][1:len(s[1])-1]
        _id = s[2][1:len(s[2])-1]
        title = s[3][1:len(s[3])-1]
        date = s[4][1:len(s[4])-1]
        
        try:
            p_exists = Post.objects.get(id=_id)
            print('Object already in database')
            return
        except:
            pass

        p = Post(user=user, date=date, link=link, id=_id, title=title)
        p.save()
        
def load_reviews():
    text_file = open('load_reviews.txt', 'r')
    lines = text_file.readlines()
    for line in lines:
        sub = re.sub(' +', ' ', line)
        s = sub.split('\t')
        print('Length of Split Review: ' + str(len(s)))
        _id = s[0][1:len(s[0])-1]
        user = s[2][1:len(s[2])-1]
        date = s[3][1:len(s[3])-1]
        item = s[4][1:len(s[4])-1]
        link = s[5][1:len(s[5])-1]
        review = s[6][1:len(s[6])-1]
        size = s[7][1:len(s[7])-1]
        post_id = s[8][1:len(s[8])-1]
        pic = s[9][1:len(s[9])-1]
        print(post_id + ' ' + _id + ' ' + user +  ' ' + date + ' ' + item)

        try:
            p = Post.objects.get(id=post_id)
        except:
            print('Post does not exist')
            return

        p.review_set.create(user=user, date=int(date), itemName=item, itemLink=link, itemReview=review, itemSize=size, itemPic=pic)

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepReviews.settings')
    django.setup()

    try:
        from catalog.models import Post, Review
        run()
        
    except django.core.exceptions.AppRegistryNotReady:
        print('Cannot Load Models because the models are not ready')