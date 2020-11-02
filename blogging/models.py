from django.db import models

from django.contrib.auth.models import User

#For adding the RSS Feed
from django.contrib.syndication.views import Feed
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=128)# name of category
    description = models.CharField(max_length=128)#description
    posts = models.ManyToManyField(Post, blank=True, related_name='categories' )# posts


    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


#Creating the RSS Feed

class RecentPosts(Feed):
    title = "Latest Blog Entries"
    link = "/latest/"
    description = "Updates to the blog"

    def items(self):
        return Post.objects.order_by('published_date')

    def item_title(self, item):
        return item.title

    def item_author(self, item):
        return item.author

    def item_date(self, item):
        return item.created_date

    def item_link(self,item):
        return reverse('blog_detail', args=[item.pk])
