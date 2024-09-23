from django.shortcuts import render



def Main_Page(request):
    return render(request, "main.html")


