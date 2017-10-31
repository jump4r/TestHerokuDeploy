from django.db import models

# Create your models here.
class Post(models.Model):
    user = models.CharField(max_length=32)
    date = models.CharField(max_length=50)
    link = models.CharField(max_length=150)
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title + ', ' + self.user

class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.CharField(max_length=32)
    date = models.IntegerField()
    itemName = models.CharField(max_length=200)
    itemLink = models.CharField(max_length=150)
    itemReview = models.CharField(max_length=1500)
    itemSize = models.CharField(max_length=32)
    itemPic = models.CharField(max_length=150)

    def __str__(self):
        return self.itemName + ', by ' + self.user