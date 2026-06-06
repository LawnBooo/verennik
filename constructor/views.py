from django.shortcuts import render

def constructor_view(request):
    return render(request, 'constructor/constructor.html')