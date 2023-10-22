from django.db import models
from django.urls import reverse
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a list category.')

    def __str__(self):
        return self.name


class List(models.Model):
    title = models.CharField(max_length=200, help_text='Enter a list title')
    description = models.CharField(max_length=200, help_text='Enter a list description')
    notes = models.TextField()
    category = models.ManyToManyField(Category, help_text='Select a category for this list')
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
    difficulty = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ], help_text="Enter a difficulty level for the task. The higher the number, the more difficult it should be.", null=True)

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


class Reminder(models.Model):
    description = models.CharField(max_length=100)
    task = models.OneToOneField('Task', on_delete=models.RESTRICT, null=False)
    user = models.OneToOneField(User, on_delete=models.RESTRICT, null=False)
    notification_date = models.DateTimeField()

    def __str__(self):
        return self.description
