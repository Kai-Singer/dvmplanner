from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles import finders
from dvmplanner.scripts.users import User
import os

uid = 'u0000'
if not finders.find(f'profiles/{uid}.png'):
  uid = '_default'
data = {
  'uid': uid,
  'username': 'testuser',
  'first_name': 'Max',
  'last_name': 'Mustermann'
}

def home(request):
  return redirect(dashboard)

def dashboard(request):
  # usernames = []
  # users = User.getUsers()
  # for user in users:
  #   usernames.append(user.getUsername())
  # data = {
  #   'usernames': usernames
  # }
  return render(request, 'dvmplanner/dashboard.html', data)

def reports(request):
  return render(request, 'dvmplanner/reports.html', data)

def review(request):
  return render(request, 'dvmplanner/review.html', data)

def admin(request):
  return render(request, 'dvmplanner/admin.html', data)

def profile(request):
  return render(request, 'dvmplanner/profile.html', data)

def addreport(request):
  return render(request, 'dvmplanner/addreport.html', data)