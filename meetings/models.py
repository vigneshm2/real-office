from __future__ import unicode_literals
import json

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin
from rooms.models import Room


class Meeting(models.Model):
    name = models.CharField(max_length=1000)
    info = models.TextField(blank=True, default='')
    creatingStaff = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    creatingProfessor = models.CharField(max_length=200, blank=True)
    # store comma sep list of participants, TODO add helper functions
    participants = models.TextField(default='[]', blank=False, null=False)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    venue = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s on %s at %s' % (self.name, self.start, self.venue)

    def storeParticipants(self, text):
        pass
    
    def getParticipantsAsText(self):
        pass
