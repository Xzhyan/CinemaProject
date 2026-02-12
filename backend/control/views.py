from django.shortcuts import render


def control(request):
    return render(request, 'control.html')