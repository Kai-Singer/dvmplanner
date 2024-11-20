from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage

def home(request):
  return redirect(dashboard)

def dashboard(request):
  return render(request, 'dvmplanner/dashboard.html')

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