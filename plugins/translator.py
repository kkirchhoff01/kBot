# -*- coding: iso-8859-15 -*-
import urllib
import json

api_key = ""
with open('key.txt', 'r') as fh:
    api_key = fh.read().strip('\n')

url = language_detection = "https://translate.yandex.net/api/v1.5/tr.json/"


def translate(text):
    language_detection = url + "detect?key={0}&text={1}".format(api_key, text)
    response = urllib.urlopen(language_detection)
    detection_results = response.read()
    detection_json = json.loads(detection_results)
    response.close()

    if int(detection_json['code']) != 200:
        return "Failed to detect language"

    lang = detection_json['lang'] + "-en"
    translator = url + "translate?key={0}&text={1}&lang={2}".format(
            api_key, text, lang)
    response = urllib.urlopen(translator)
    results = response.read()
    translation = json.loads(results)
    response.close()

    if int(translation['code']) != 200:
        return "Failed to translate"

    return "({0}) {1}".format(lang, translation['text'][0])
