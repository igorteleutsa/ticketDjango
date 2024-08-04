from django.db import models
from users.models import User


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='assigned_groups')

    def __str__(self):
        return self.name
