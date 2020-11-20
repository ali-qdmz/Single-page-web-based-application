from django.db import models
from django.contrib.auth.models import User

class Custom_Auth(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    email_confirmed = models.BooleanField(default=False)
    signup_date = models.CharField(max_length=200)
    last_login = models.CharField(max_length=200)
    has_paid = models.BooleanField(default=False)
    token = models.CharField(max_length=600)
    temp_token = models.CharField(max_length=600)
    favorite_filters = models.TextField(default='[]')
    favorite_stocks = models.TextField(default='[]')
    temporary_code = models.TextField(default='[]')



