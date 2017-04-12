import json

from django.shortcuts import render
from db.models import webshell
from django.http import HttpResponse

# Create your views here.
def delete(request):
    id = request.GET.get('id')
    shell = webshell.objects.get(id=id)
    shell.delete()
    shell = webshell.objects.all()
    WEBHSELL = []
    for s in shell:
        t = {}
        t['id'] = s.id
        t['remarks'] = s.remarks
        t['links'] = s.links
        t['type'] = s.type
        t['time'] = str(s.time)
        # print(time.strftime('%Y-%m-%d',t['time']))
        WEBHSELL.append(t)
    return HttpResponse(json.dumps({'webshell': WEBHSELL}))