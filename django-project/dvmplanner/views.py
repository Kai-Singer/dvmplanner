from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from dvmplanner.scripts.users import User

def home(request):
  return redirect(dashboard)

def dashboard(request):
  usernames = []
  users = User.getUsers()
  for user in users:
    usernames.append(user.getUsername())
    data = {
      'usernames': usernames
    }
  return render(request, 'dvmplanner/dashboard.html', data)

def reports(request):
  return render(request, 'dvmplanner/reports.html')

def review(request):
  return render(request, 'dvmplanner/review.html')

def admin(request):
  return render(request, 'dvmplanner/admin.html')

def profile(request):
  return render(request, 'dvmplanner/profile.html')

def addreport(request):
  return render(request, 'dvmplanner/addreport.html')