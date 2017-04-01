from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import ModelForm
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

from .models import Meeting
from tasks.models import Task
from rooms.models import Room


def index(request):
    startdate = timezone.now()
    enddate = startdate + datetime.timedelta(days=5)

    m = Meeting.objects.filter(start__range=[startdate, enddate])

    t = Task.objects.filter(meeting__in=m, complete='False')

    return render(request, 'index.html', {'user': request.user, 'meeting': m, 'task': t})


class MeetingForm(ModelForm):

    class Meta:
        model = Meeting
        exclude = ['creatingStaff']


def about(request):
    return render(request, 'about.html')

def success(request):
    return render(request, 'meeting_success.html')

def create(request):
    if request.method == 'POST':
        # print(request.POST)
        form = request.POST
        u = User.objects.get(id=2)
        m = Meeting()
        m.name = form['Name']
        m.info = form['Info']
        m.creatingProfessor = form['CreatingProfessor']
        m.creatingStaff = u  # default vignesh for now
        m.participants = form['Participants']
        m.start = form['Start']
        m.end = form['End']
        ven = Room.objects.get(id=form['Venue'])
        m.venue = ven
        m.save()

        if(len(form['tasks'])>0):
            taskComma = form['tasks']
            taskList = taskComma.split(",")

            for task in taskList:
                t = Task()
                t.meeting = m
                t.name = task
                t.save()

        return redirect('/meeting/success')

    else:
        form = MeetingForm()
        r = Room.objects.all()
        return render(request, 'create_meeting.html', {'user': request.user, 'form': form, 'room': r})

def view_list(request):
    meetings = Meeting.objects.all()
    return render(request, 'view_meeting.html', {'user': request.user, 'meeting': meetings})


def individual_meeting(request):
    if request.method == 'GET':
        meetid = request.GET['meetid']
        print meetid
        x = (Meeting.objects.get(id=(meetid)))
        return render(request, 'individual_meeting.html', {'user': request.user, 'meeting': x})
