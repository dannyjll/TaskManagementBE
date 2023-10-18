from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a category name')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Comment(models.Model):
    list = models.ForeignKey('List', on_delete=models.RESTRICT, null=True)
    siteUser = models.ForeignKey('SiteUser', on_delete=models.RESTRICT, null=True)
    comments = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.comments


class List(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a List Title')
    private = models.BooleanField()
    favorite = models.BooleanField()
    notes = models.TextField()
    list_Type = models.ForeignKey('list', on_delete=models.RESTRICT, null=True)
    siteUser = models.ForeignKey('SiteUser', on_delete=models.RESTRICT, null=True)
    parent = models.ForeignKey('List', on_delete=models.RESTRICT, null=True, blank=True)
    list_image = models.ImageField(upload_to='images/', null=True, blank=True)
    categories = models.ManyToManyField('Category', related_name='lists', blank=True)
    comments = models.ManyToManyField('List', related_name='list_comments', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list_detail', args=[str(self.id)])


class MembershipTable(models.Model):
    siteUser = models.ForeignKey('SiteUser', on_delete=models.RESTRICT, null=True)
    group = models.ForeignKey('Group', on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.siteUser


class Group(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Task(models.Model):
    uniqueId = models.CharField(max_length=100, help_text='Enter a unique name for this item')
    name = models.CharField(max_length=200, help_text='Enter a name for this item')
    quantity = models.IntegerField()
    value = models.DecimalField(decimal_places=2, max_digits=100)
    notes = models.TextField()
    collectedDate = models.DateField()
    list = models.ForeignKey('List', on_delete=models.RESTRICT, null=True)

    #    categories = models.ManyToManyField('Category', related_name='items', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list_detail', args=[str(self.list.id)])


class SiteUser(AbstractUser):
    private = models.BooleanField(default=True)
    first_name = models.CharField(max_length=150)
    description = models.TextField(null=True)
    user_image = models.ImageField(upload_to='images/', null=True, blank=True)
    favorite_lists = models.ManyToManyField(List, related_name='favored_by', blank=True)

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])
