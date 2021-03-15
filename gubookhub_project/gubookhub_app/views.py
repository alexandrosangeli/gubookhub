from django.shortcuts import render

# Create your views here.

def index(request):
    context_dict = {}

    context_dict['boldmessage'] = 'Find resources that are right for you!'

    return render(request, 'gubookhub/index.html', context=context_dict)

def about(request):
    context_dict = {}

    context_dict['aboutmessage'] = 'This is a student made resource hub for the University of Glasgow students. It features a collection of useful textbooks and resources submitted by fellow students across various schools from various years.'

    return render(request, 'gubookhub/about.html', context = context_dict)
