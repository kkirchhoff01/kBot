import urllib
import urllib2
import json
import re
from bs4 import BeautifulSoup


def check_link(msg):
    links = re.findall('(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)
    if len(links) > 0:
        return links[0]
    else:
        return False


def read_link(url):
    try:
        if re.match('http[s]?://', url) == None:
            url = 'http://' + url
        response = urllib.urlopen(url)
        results = response.read()
        response.close()
        info = response.info()
        info_type = info.type.split('/')
        if info_type[1] == 'html':
            soup = BeautifulSoup(results)
            url_title = soup.title.string
            return url_title.encode('utf-8')
        else:
            return '[' + info_type[0] + '][' + info_type[1] + '] ' + info.getheaders('Content-Length')[0] + ' bytes'
    except IOError, exc:
        print exc
        return False
    except Exception, exc:
        print exc
        return False
