from __future__ import unicode_literals
from django.db import models
from ..courses.models import Course
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
  def validate_and_create_user(self, form_data):
    email = form_data['email']
    password = form_data['password']

    errors = []

    if not EMAIL_REGEX.match(email):
      errors.append('Email must be valid.')
    if len(password) < 8:
      errors.append('Password must be at least 8 characters long.')

    if len(errors) > 0:
      return (False, errors)
    
    try:
      self.get(email=email)
      errors.append('Email already in use.')
      return (False, errors)
    except:
      pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
      user = self.create(email=email, password_hash=pw_hash)
      return (True, user)

  def validate_login(self, form_data):
    email = form_data['email']
    password = form_data['password']

    errors = []

    user = self.filter(email=email)
    if len(user) > 0:
      is_matching = bcrypt.checkpw(password.encode(), user[0].password_hash.encode())
      print is_matching, "<------- is_matching"

      if is_matching:
        return (True, user[0])

      errors.append('Username and password combo not valid.')
      return (False, errors)

    errors.append('Username and password combo not valid.')
    return (False, errors)


class User(models.Model):
  email = models.CharField(max_length = 255)
  password_hash = models.CharField(max_length = 500)
  permission_level = models.CharField(max_length = 255)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  courses = models.ManyToManyField(Course, related_name = 'users')
  objects = UserManager()