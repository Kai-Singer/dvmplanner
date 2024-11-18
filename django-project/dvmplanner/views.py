from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage

def dashboard(request):
  return render(request, 'dvmplanner/dashboard.html')