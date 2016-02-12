import json
import random
import re
import urllib
import urlparse
import mechanize
from plugins.image_ascii import draw_ascii


def get_command(cmd, msg):
    if cmd == 'help':
        return("For a list of commands use .commands. To use kBot try:" +
               " .<command> <input>")
    elif cmd == 'commands':
        return 'Commands: ' + ', '.join(get_command_list())
    elif cmd == 'g':
        return google(msg)
    elif cmd == 'w':
        return wikipedia(msg)
    elif cmd == 'def':
        return dictionary_search(msg)
    elif cmd == 'about':
        return "This bot was written in Python by Kevin Kirchhoff"
    elif cmd == 'convert':
        return convert_units(msg)
    elif cmd == 'eval':
        return evaluate(msg)
    elif cmd == 'quote':
        return quote(msg)
    elif cmd == 'decide':
        return decide(msg)
    elif cmd == 'draw':
        return draw_ascii(msg)
    elif cmd == 'translate':
        return translate(msg)
    else:
        return False


def get_command_list():
    return ['help', 'commands', 'g', 'w', 'about',  'convert',
            'eval', 'def', 'quote', 'decide', 'draw', 'translate']


def google(search_input):
    if search_input is None:
        return 'Use .help for help.'
    query = urllib.urlencode({'q': search_input})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query
    response = urllib.urlopen(url)
    search_results = response.read()
    input_results = json.loads(search_results)
    results = input_results['responseData']['results']
    result = re.sub('<.*?>', '', u' '.join((results[0]['title'], ': ',
                    results[0]['url'],
                    results[0]['content'])).encode('utf-8').strip())
    return result


# Use wikipedia python library? Or do it the right way?
def wikipedia(search_input):
    if search_input is None:
        return 'Use .help for help.'
    return 'Wiki search is still in progress!'


# Keep dict file or use website
# Possibly find words most closely spelled to request
def dictionary_search(search_input):
    if(re.match(r"^[a-zA-Z]+$", search_input) is None):
        return 'Invalid input.'

    else:
        url = 'http://dictionary.reference.com/browse/' + search_input
        response = urllib.urlopen(url)
        search_results = response.read()
        content = re.findall(r'<div class="def-content">(.*?)</div>',
                             search_results, re.DOTALL)
        if len(content) != 0:
            return_content = re.sub('<.*?>', '', content[0])
            return return_content.strip('\n')
        else:
            return 'Definition not found'


# Get code from submit site using form info
def evaluate(msg):
    eval_input = None
    language = None

    if ' ' in msg:
        language = msg[0:msg.index(' ')]
        eval_input = msg.split(language)[1]
    else:
        language = msg

    if eval_input is None and language.lower() != 'list':
        return 'Use .help for help.'

    value = ""
    if language.lower() == 'c':
        value = "c/gcc-4.4.3"
    elif language == 'C++' or language == 'c++' or language == 'cpp':
        value = "c++/c++11-gcc-4.9.1"
    elif language.lower() == 'javascript':
        value = "javascript/node-0.10.29"
    elif language.lower() == 'lua':
        value = "lua/lua-5.1.5"
    elif language.lower() == 'php':
        value = "php/php-5.5.14"
    elif language.lower() == 'perl':
        value = "perl/perl-5.20.0"
    elif language.lower() == 'python' or language.lower() == 'python2':
        value = "python/cpython-2.7.8"
    elif language.lower() == 'python3':
        value = "python/cpython-3.4.1"
    elif language.lower() == 'ruby':
        value = "ruby/mri-1.0"
    elif language.lower() == 'list':
        return ('Language Options: C, C++, Javascript, lua,' +
                ' PHP, Perl, Python, Python3, Ruby.')
    else:
        return "Language not found."

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open('https://eval.in')
    br.select_form(nr=0)
    br["code"] = eval_input.strip(' ')
    br.form["lang"] = [value, ]
    res = br.submit()
    content = res.read()
    content = content.split('Output')[2].split('Fork')[0]
    br.close()
    content = re.findall(r'<p.*?>(.*?)</p.*?>', content, re.DOTALL)

    if 'OK' in content[len(content) - 1]:
        return content[0].strip('\n')
    else:
        return content[len(content)-1].strip('\n')


def convert_units(msg):
    form = re.match(r"^(?P<unit_value>[1-9][0-9]+)\s(?P<unit_from>[a-zA-Z]+)" +
                    r"(\s|\s(to)\s)(?P<unit_to>[a-zA-Z]+)$", msg)
    value = None
    unit_input = None
    unit_output = None
    if form is not None:
        unit_dict = form.groupdict()
        try:
            value = unit_dict['unit_value']
            unit_input = unit_dict['unit_from']
            unit_output = unit_dict['unit_to']
        except:
            return("Usage: .convert <value> <units to convert from>" +
                   " <units to convert to>")
    else:
        return("Usage: .convert <value> <units to convert from>" +
               " <units to convert to>")
    if value is None:
        return "Use .help for help"
    return "Unit converter is still in progress!"


def quote(user):
    if user is None:
        return "Use .help for help"
    quotes = []
    with open('/home/kkirchhoff/Programming/Python/IRC-Bot/IRC.log',
              'r') as log:
        lines = log.readlines()
        for line in lines:
            line = line.split(' ')
            if(len(line) > 1 and user == line[1].strip(':') and
                    line[2].split('.')[0] != ''):
                quotes.append(' '.join(line[2:]))
    if len(quotes) > 0:
        return("<{0}> {1}".format(user,
                                  quotes[random.randint(0,
                                         len(quotes)-1)].strip('\n')))
    else:
        return 'No quotes found'


def decide(options):
    make_decision = options.split('or')
    if len(make_decision) != 2:
        return "Use: .decide <option 1> or <option 2>"
    decision_number = int(round(random.random()))

    return "Do %s" % make_decision[decision_number].strip(' ')


def translate(text):
    api_key = ""
    with open('key.txt', 'r') as fh:
        api_key = fh.read().strip('\n')

    url = "https://translate.yandex.net/api/v1.5/tr.json/"

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
