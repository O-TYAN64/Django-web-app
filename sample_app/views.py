from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import NonoData
import json
import sys
import os
import MeCab

def index(request):
    # POSTリクエスト時の処理
    if request.method == 'POST':
        print('POSTリクエスト')
        data = json.loads(request.body)
        speech_text = data.get('speech_text', '')  # 'speech_text'を取得
        print('speech_text:', speech_text)

        # speech_textに対する処理
        # response_text = '返答(オウム返し)：' + speech_text
        word_list = morphological_analysis(speech_text)
        print(word_list)
        response_text = nono_data_get(word_list)
        print(response_text)

        return JsonResponse({'response_text': response_text})  # JSONレスポンスを返す

    # GETリクエスト時の処理
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def morphological_analysis(speech_text):
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
    os.environ['LC_ALL'] = 'C.UTF-8'

    tagger = MeCab.Tagger("-Owakati")

    str_output = tagger.parse(speech_text)

    #listに変換する
    list_output = str_output.split(' ')
    
    return list_output


def nono_data_get(word_list):
    nono_data = NonoData.objects.values()

    print(nono_data)

    response_text = ''

    for nono_data_dict in nono_data:
        nono_data_key = nono_data_dict['data_key']
        nono_data_value = nono_data_dict['data_value']
        if nono_data_key in word_list:
            response_text += f'{nono_data_key}は{nono_data_value}です<br>'

    return response_text