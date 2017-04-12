from django.shortcuts import render
from db.models import webshell
# Create your views here.
def index(request):
    php = webshell.objects.filter(type='PHP')
    jsp = webshell.objects.filter(type='JSP')
    asp = webshell.objects.filter(type='ASP')
    aspx = webshell.objects.filter(type='ASPX')
    all = webshell.objects.all()
    return render(
        request,
        'index.html',
        {
            'php': len(php),
            'jsp': len(jsp),
            'asp': len(asp),
            'aspx': len(aspx),
            'webshell': all
        }
    )