from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Models and Managers.

class UserManager(models.Manager):
    def register_validator(self,postData):
        errors = {}
        first_name = postData['first_name']
        if (len(first_name)<2) or not re.match(r"^[A-Za-z]*$",first_name):
            errors['first_name']="Not a valid first name"
        last_name = postData['last_name']
        if (len(last_name)<2) or not (re.match(r"^[A-Za-z]*$",first_name)):
            errors['last_name']="Not a valid last name"
        email=postData['email']
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            errors['email']="Not a valid email"
            if User.objects.filter(email=email).exists():
                errors['email']="A user with this email already exists"
        if len(postData['password'])<8:
            errors['password']="Password is too short"
        if postData['password']!=postData['pw_confirm']:
            errors['pw_confirm']="Confirmation password  doesn't match"
        return errors
    
    def login_validator(self,postData):
        errors = {}
        email=postData['email']
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            errors['login_email']="Not a valid email"
        elif len(postData['password'])<8:
            errors['login_password']="Password is too short"
        elif User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
                errors['login_password']="WRONG PASSWORD"
        else:
            errors['login_email']="This email doesn't match any users"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    access_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    author = models.ForeignKey(User, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, related_name='comments')
    message = models.ForeignKey(Message, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)