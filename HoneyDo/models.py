from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User


class List(models.Model):
    title = models.CharField(max_length=200, help_text='Enter a list title')
    description = models.CharField(max_length=200, help_text='Enter a list description')
    notes = models.TextField()
    list_image = models.ImageField(upload_to='images/', null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('list_detail', args=[str(self.id)])


class Task(models.Model):
    title = models.CharField(max_length=200, help_text='Enter a name for this task')
    description = models.CharField(max_length=500, help_text='Enter a description for this task')
    completion_status = models.BooleanField(default=False)
    due_date = models.DateTimeField()
    notes = models.TextField()
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    list = models.ForeignKey('List', on_delete=models.RESTRICT, null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=20)
    users = models.ManyToManyField(User)
    lists = models.ManyToManyField('List')

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique=True)
    first_name = models.TextField(max_length=500, null=True, blank=True)
    last_name = models.TextField(max_length=500, null=True, blank=True)
    email = models.TextField(max_length=500, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to="images/profile",
                              default="images/profile/default.png", null=True)
    private = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)
