from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'pages/about.html')

def contacts(request):
    return render(request, 'pages/contacts.html')
