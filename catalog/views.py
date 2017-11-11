from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sys, os
import catalog.scraper, catalog.timer
from pprint import pprint
from .models import Post, Review

class Filter:
    def __init__(self):
        self.reviews = self.sort(Review.objects.all())

    def process(self, args):
        for a in args:
            
            if (args[a] == None or args[a] == ''):
                print('Empty argument for ' + a + ', continuing')
                continue

            self.reviews = self.filter(a, args[a])

    def filter(self, attr, key):
        filtered_reviews = []

        for review in self.reviews:
            if key.lower() in getattr(review, attr).lower():
                print(key + ' found in ' + getattr(review, attr))
                filtered_reviews.append(review)

        return self.sort(filtered_reviews)

    def filter_by_id(self, id_string, reviews):
        ids = id_string.split(',')

        filtered_reviews = []

        for review in reviews:
            if (str(review.id) in ids):
                # print('Found Review ' + str(review.id) + ' in ' + str(ids))
                filtered_reviews.append(review)

        self.reviews = self.sort(filtered_reviews)

    # Sorts by most recent
    def sort(self, reviews):
        return sorted(reviews, key=lambda Review: Review.date, reverse=True)

class Query:
    def __init__(self, user='', item=''):
        self.args = { 'user': user, 'itemName': item }

class AppView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        
        catalog.scraper.check_to_scrape_post()

        args = { }

        args['user'] = request.GET.get('user') if (request.GET.get('user') != None) else ''   
        args['itemName'] = request.GET.get('item') if (request.GET.get('item') != None) else ''
        ids = request.GET.get('ids') if (request.GET.get('ids') != None) else ''

        is_filtered = self.any_full_filter(args['user'], args['itemName'], ids)
        bookmarks_only = True if (ids != '') else False

        query_string = '?'  
        if (is_filtered):
            query_string += ('user=' + args['user'] + '&') if (args['user'] != '') else ''
            query_string += ('item=' + args['itemName'] + '&') if (args['itemName'] != '') else ''
        
        if (bookmarks_only):
            query_string += 'ids=' + ids + '&'

        f = Filter()
        f.process(args)

        if bookmarks_only:
            f.filter_by_id(request.GET.get('ids'), f.reviews)

        paginator = Paginator(f.reviews, 10)
        page = request.GET.get('page')

        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            reviews = paginator.page(1)
        except EmptyPage:
            reviews = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {"request": request.GET, "reviews": reviews, "is_filtered": is_filtered, "query": query_string, "bookmarks_only": bookmarks_only, 'num_reviews': len(Review.objects.all()) })

    def any_full_filter(self, user, item, ids):
        return True if (user or item or ids) else False