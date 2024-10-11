from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django.shortcuts import render
import subprocess

def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))
    
def my_python_view(request):
    # ここでPythonの処理を実行
    result = subprocess.run(['python3', '/app/getdata.py'], capture_output=True, text=True)
    data = {'message': 'Python処理が完了しました'}
    return JsonResponse(data)
