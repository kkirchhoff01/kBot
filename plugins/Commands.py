import json
import random
import re
import urllib
import urlparse
import mechanize
from image_ascii import draw_ascii


# Match proper command
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


# Return command list
def get_command_list():
    return ['help', 'commands', 'g', 'w', 'about',  'convert',
            'eval', 'def', 'quote', 'decide', 'draw', 'translate']


# Google Search
def google(search_input):
    if search_input is None:
        return 'Use .help for help.'

    query = urllib.urlencode({'q': search_input})  # Encode url
    # Use google api to search
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query

    # Fetch results
    response = urllib.urlopen(url)
    search_results = response.read()

    # Get json results
    input_results = json.loads(search_results)
    results = input_results['responseData']['results']

    # Remove unwanted HTML tags and join results
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
    # Make sure input is valid (single word)
    if(re.match(r"^[a-zA-Z]+$", search_input) is None):
        return 'Invalid input.'

    else:
        # Simple search using URL
        url = 'http://dictionary.reference.com/browse/' + search_input
        response = urllib.urlopen(url)
        search_results = response.read()

        # Find definition in response
        content = re.findall(r'<div class="def-content">(.*?)</div>',
                             search_results, re.DOTALL)

        # Make sure definition was found
        if len(content) != 0:
            # Remove HTML tags and return definition
            return_content = re.sub('<.*?>', '', content[0])
            return return_content.strip('\n')
        else:
            return 'Definition not found'


# Get code from submit site using form info
def evaluate(msg):
    eval_input = None
    language = None

    # Check for proper input or list request
    if ' ' in msg:
        # Get language and code to evaluate
        language = msg[0:msg.index(' ')]
        eval_input = msg.split(language)[1]
    else:
        # List request found; return languages
        language = msg

    if eval_input is None and language.lower() != 'list':
        return 'Use .help for help.'

    # Find language
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
    elif language.lower() == 'list':  # Return list of languages
        return ('Language Options: C, C++, Javascript, lua,' +
                ' PHP, Perl, Python, Python3, Ruby.')
    else:
        return "Language not found."  # Return if no language found

    # Use eval.in to evaluate language
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open('https://eval.in')

    br.select_form(nr=0)  # Form select

    # Form input
    br["code"] = eval_input.strip(' ')
    br.form["lang"] = [value, ]

    # Get Results
    res = br.submit()
    content = res.read()
    # Parse output
    content = content.split('Output')[2].split('Fork')[0]
    br.close()
    # Get result
    content = re.findall(r'<p.*?>(.*?)</p.*?>', content, re.DOTALL)

    # If code ran properly return output
    if 'OK' in content[len(content)-1]:
        # Check for output
        if len(content[0]) > 0:
            return content[0].strip('\n')
        else:
            return "OK (no output)"

    # Code did not run properly
    else:
        return content[len(content)-1].strip('\n')


# Convert units still in progress
def convert_units(msg):
    # Match convert
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


# Quote
def quote(user):
    if user is None:
        return "Use .help for help"

    quotes = []
    # Open log
    with open('/home/kkirchhoff/Programming/Python/IRC-Bot/IRC.log',
              'r') as log:
        # Read log into memory
        lines = log.readlines()
        for line in lines:
            line = line.split(' ')
            # Parse line in log
            if(len(line) > 1 and user == line[1].strip(':') and
                    line[2].split('.')[0] != ''):
                # Get quotes
                quotes.append(' '.join(line[2:]))
    if len(quotes) > 0:
        # Return random quote
        return("<{0}> {1}".format(user,
                                  quotes[random.randint(0,
                                         len(quotes)-1)].strip('\n')))
    else:
        return 'No quotes found'


# Choose between two options
def decide(options):
    # Split on 'or'
    make_decision = options.split('or')

    if len(make_decision) != 2:
        return "Use: .decide <option 1> or <option 2>"

    # Random choice
    decision_number = int(round(random.random()))
    # Return decision
    return "Do %s" % make_decision[decision_number].strip(' ')


# Translate foreign language to English
def translate(text):
    api_key = ""

    # API key for yandex required in fil key.txt
    with open('key.txt', 'r') as fh:
        api_key = fh.read().strip('\n')

    # Use yandex to translate
    url = "https://translate.yandex.net/api/v1.5/tr.json/"

    # Detect language
    language_detection = url + "detect?key={0}&text={1}".format(api_key, text)
    response = urllib.urlopen(language_detection)
    detection_results = response.read()
    detection_json = json.loads(detection_results)
    response.close()

    # yandex couldn't detect language
    if int(detection_json['code']) != 200:
        return "Failed to detect language"

    # Format to convert to English
    lang = detection_json['lang'] + "-en"
    translator = url + "translate?key={0}&text={1}&lang={2}".format(
            api_key, text, lang)

    # Get translation
    response = urllib.urlopen(translator)
    results = response.read()
    translation = json.loads(results)
    response.close()

    # yandex failed to translate
    if int(translation['code']) != 200:
        return "Failed to translate"

    # Return translation
    return "({0}) {1}".format(lang, translation['text'][0])
