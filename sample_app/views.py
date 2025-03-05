from django.http import JsonResponse, HttpResponse
from django.template import loader
from .models import NonoData
import json
from janome.tokenizer import Tokenizer
from datetime import date, timedelta
from difflib import get_close_matches
from pykakasi import kakasi

# Tokenizer と Kakasi のインスタンスを共有
tokenizer = Tokenizer()
kks = kakasi()


def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        speech_text = data.get('speech_text', '')

        # 形態素解析
        word_list = morphological_analysis(speech_text)

        # データ取得
        response_text = nono_data_get(word_list)

        return JsonResponse({'response_text': response_text})

    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def morphological_analysis(text):
    """
    入力テキストを形態素解析し、基本形の単語リストを返す。
    """
    tokens = tokenizer.tokenize(text)
    return [token.base_form for token in tokens]


def convert_to_romaji(text):
    """
    日本語のテキストをローマ字に変換する。
    """
    result = kks.convert(text)
    return ''.join([converted_word['hepburn'] for converted_word in result])


def nono_data_get(word_list):
    """
    単語リストを元にデータベースを検索し、対応する情報を返す。
    """
    if ('自己' in word_list and '紹介' in word_list) or '挨拶' in word_list:
        return "こんにちは。私は、地域情報音声アシスタントアプリ、「ノノ」です。私は地域情報を提供し、みなさんの生活をサポートします。何か知りたいことはありますか？"

    today = date.today()
    date_mapping = {'今日': today, '明日': today + timedelta(days=1), '昨日': today - timedelta(days=1)}

    # データベースからユニークな data_key を取得
    data_keys = list(NonoData.objects.values_list('data_key', flat=True).distinct())

    # 日付とデータキーを抽出
    target_dates = [(word, date_mapping[word]) for word in word_list if word in date_mapping]
    target_keys = [word for word in word_list if word in data_keys]

    if not target_dates:
        target_dates = [('今日', today)]

    # ローマ字変換されたデータキーをキャッシュ
    romaji_keys = {key: convert_to_romaji(key) for key in data_keys}

    # target_keys に含まれない data_keys を取得
    unmatched_data_keys = [key for key in data_keys if key not in target_keys]

    matched_keys = []

    # 近似一致を検索（target_keys に含まれないデータキーに対して）
    for word in word_list:
        word_romaji = convert_to_romaji(word)
        matched_keys.extend(get_close_matches(word_romaji, [romaji_keys[key] for key in unmatched_data_keys], n=3, cutoff=0.7))

    if matched_keys:
        matched_original_keys = [key for key, romaji in romaji_keys.items() if romaji in matched_keys]
        response_texts = [f"もしかして「{', '.join(matched_original_keys)}」でしょうか？"]

        # 近似一致したデータキーを target_keys に追加
        target_keys.extend(matched_original_keys)

    # 完全一致検索
    response_texts = response_texts if 'response_texts' in locals() else []
    for target_day_word, target_date in target_dates:
        query = NonoData.objects.filter(date=target_date, data_key__in=target_keys)
        for data in query:
            response_texts.append(f"{target_day_word}の{data.data_key}は{data.data_value}です")

    if response_texts:
        return '<br>'.join(response_texts)

    return '申し訳ありません、質問の内容を理解できませんでした。もう一度、別の言い方でお尋ねいただけますか？'
