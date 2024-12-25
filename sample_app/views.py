from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import NonoData
import json
from janome.tokenizer import Tokenizer


def index(request):
    # POSTリクエスト時の処理
    if request.method == 'POST':
        print('POSTリクエスト')
        data = json.loads(request.body)
        speech_text = data.get('speech_text', '')  # 'speech_text'を取得
        print('speech_text:', speech_text)

        # speech_textに対する処理
        word_list = morphological_analysis(speech_text)
        print(word_list)
        response_text = nono_data_get(word_list)
        print(response_text)

        return JsonResponse({'response_text': response_text})  # JSONレスポンスを返す

    # GETリクエスト時の処理
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def morphological_analysis(text):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text)
    list_output = [token.base_form for token in tokens]
    return list_output


def nono_data_get(word_list):
    nono_data = NonoData.objects.values()

    response_text = ''

    for nono_data_dict in nono_data:
        nono_data_key = nono_data_dict['data_key']
        nono_data_value = nono_data_dict['data_value']
        if nono_data_key in word_list:
            response_text += f'{nono_data_key}は{nono_data_value}です<br>'

    return response_text
