from uuid import uuid4
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, null=False)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    display_name = models.CharField(max_length=64, null=False, blank=False)
    creation_time = models.DateTimeField(auto_now_add=True)

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, null=False)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    description = models.CharField(max_length=128, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name="users")
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    # project =one to one
class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    description = models.CharField(max_length=128, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


    

    