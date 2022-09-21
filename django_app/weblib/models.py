from ast import keyword
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_owner')
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=1000)
    content = models.TextField(max_length=1000)
    keyword = models.TextField(max_length=100)
    folder_id = models.IntegerField(default=-1)
    pub_date = models.DateTimeField(auto_now_add=True)
    good_count = models.IntegerField(default=0)
    public = models.BooleanField()

    def __str__(self):
        return '<Article:id='+str(self.id)+', '+\
            self.title + '(' + str(self.owner) + ')>'

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
        related_name='comment_owner')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'comment for "' + str(self.article) + '" (by ' + \
            str(self.owner) + ')'

class Folder(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
        related_name='folder_owner')
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return '<' + self.title + '(' + str(self.owner) + ')>'

class Good(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
        related_name='good_owner')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.article) + '" (by ' + \
            str(self.owner) + ')'

class Tag(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
        related_name='tag_owner')
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return '<' + self.title + '(' + str(self.owner) + ')>'

class TagArrow(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
        related_name='tagArrow_owner')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    def __str__(self):
        return '<' + self.tag.title + ' -> ' + self.article.title + '(' + str(self.owner) + ')>'
