import json
import re
import urllib
import urlparse
import mechanize

command_trigger = '.'

def get_command(cmd, msg):
	if cmd == command_trigger + 'help':
		return "For a list of commands use .commands. To use kBot try: .<command> <input>"
	elif cmd == command_trigger + 'commands':
		return 'Commands: ' + str(get_command_list()).strip('[]')
	elif cmd == command_trigger + 'g':
		return google(msg)
	elif cmd == command_trigger + 'w' or cmd == command_trigger + 'wiki':
		return wikipedia(msg)
	elif cmd == command_trigger + 'def':
		return dictionary_search(msg)
	elif cmd == command_trigger + 'about':
		return "This bot was written in Python by Kevin Kirchhoff"
	elif cmd == command_trigger + 'convert':
		msg = msg.split(' ')
		if type(msg[0]) == float or type(msg[0]) == int:
			try:
				return conver_units(msg[0], msg[1], msg[2])
			except:
				return "Usage: %sconvert <value> <units to convert from> <units to convert to>" % command_trigger
		else:
			return "Usage: %sconvert <value> <units to convert from> <units to convert to>" % command_trigger
	elif cmd == command_trigger + 'eval':
		if ' ' in msg:
			lang = msg[0:msg.index(' ')]
			msg = msg.split(lang)[1]
		else:
			lang = msg
			msg = ""
		return evaluate(lang, msg)
	else:
		pass

def get_command_list():
	return [command_trigger + 'help', command_trigger + 'commands', command_trigger + 'g', command_trigger + 'w', command_trigger + 'wiki', command_trigger + 'about', command_trigger + 'convert', command_trigger + 'eval', command_trigger + 'def']

def google(search_input):
	if search_input == '':
		return command_trigger +  'Use help for help.'
	query = urllib.urlencode({'q': search_input})
	url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query
	response = urllib.urlopen(url)
	search_results = response.read()
	input_results = json.loads(search_results)
	results = input_results['responseData']['results']
	result = re.sub('<.*?>','', u' '.join((results[0]['title'], ': ', results[0]['url'], results[0]['content'])).encode('utf-8').strip())
	return result

#Use wikipedia python library? Or do it the right way?
def wikipedia(search_input):
	if search_input == '':
		return 'Use %shelp for help.' % command_trigger 
	return 'Wiki search is still in progress!'

#Keep dict file or use website
#Possibly find words most closely spelled to request
def dictionary_search(search_input):
	if search_input.isalpha() == False or len(search_input.split(' ')) > 1 or search_input == '':
		return 'Invalid input.'
	else:
		url = 'http://dictionary.reference.com/browse/' + search_input
		response = urllib.urlopen(url)
		search_results = response.read()
		try:
			result = search_results.split('def-content')[1]
			final_result = result[3:result.index('div')-3]
			#if '.' in final_result:
			#	final_result = final_result[0:final_result.index('.')]
			#elif ':' in final_resut:
			#	final_result = final_result[0:final_result.index(':')]
			#print final_result
			return final_result
		except ValueError:
			return 'Definition not found.'
		except IndexError:
			return 'Definition not found.'
		except:
			pass

#Get code from submit site using form info
def evaluate(language, eval_input):
	if search_input == '':
		return 'Use %shelp for help.' % command_trigger 
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
		value="python/cpython-2.7.8"
	elif language.lower() == 'python3':
		value="python/cpython-3.4.1"
	elif language.lower() == 'ruby':
		value="ruby/mri-1.0"
	elif language.lower() == 'list':
		c = 'Language Options: C, C++, Javascript, lua, PHP, Perl, Python, Python3, Ruby.'
		return c
	else:
		return "Language not found."
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.open('https://eval.in')
	b.select_form(nr=0)
	br["code"] = eval_input.strip(' ')
	br.form["lang"] = [value,]
	res = br.submit()
	content = res.read()
	content = content.split('Output')[2].split('Fork')[0]
	br.close()
	content = re.sub('<.*?>','', content).split('\n')
	content = [c for c in content if c != '' and c != ' ' and c != '  ']
	if 'OK' in content[len(content) -1]:
		return content[0].strip('    ')
	else:
		return content[len(content)-1].strip('    ')

def convert_units(value, unit_input, unit_output):
	if search_input == '':
		return 'Use %shelp for help.' % command_trigger
	return "Unit converter is still in progress!"
