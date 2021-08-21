from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
# Create your views here.
def index(request):
    return render(request, 'index.html')

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect(reverse('index'))


def browse(request):
    
    return render(request, 'browse.html')