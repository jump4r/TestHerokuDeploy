from django.shortcuts import render

# Create your views here.
from .models import Post, Review

def index(request):
    num_reviews = Review.objects.all().count()

    return render(request, 'index.html', context={'num_reviews': num_reviews})