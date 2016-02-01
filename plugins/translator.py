# -*- coding: iso-8859-15 -*-
import urllib
import json

api_key = ("trnsl.1.1.20160201T180329Z.e923c0b1bd751207." +
           "e44a510e32cecc9383da7f944b729372974bdccb")
url = language_detection = "https://translate.yandex.net/api/v1.5/tr.json/"


def translate(text):
    language_detection = url + "detect?key={}&text={}".format(api_key, text)
    response = urllib.urlopen(language_detection)
    detection_results = response.read()
    detection_json = json.loads(detection_results)
    response.close()

    if int(detection_json['code']) != 200:
        return "Failed to detect language"

    lang = detection_json['lang'] + "-en"
    translator = url + "translate?key={}&text={}&lang={}".format(
            api_key, text, lang)
    response = urllib.urlopen(translator)
    results = response.read()
    translation = json.loads(results)
    response.close()

    if int(translation['code']) != 200:
        return "Failed to translate"

    return "({}) {}".format(lang, translation['text'][0])
