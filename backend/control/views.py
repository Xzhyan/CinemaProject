from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from .forms import AddFilmCardForm

def control_panel(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'control_panel.html')
    return render(request, 'base.html')

def users(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'users.html')
    return render(request, 'base.html')


def films(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        form = AddFilmCardForm()

        context = {
            'form': form,
        }

        return render(request, 'films.html', context)
    return render(request, 'base.html')

def categories(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'categories.html')
    return render(request, 'base.html')
