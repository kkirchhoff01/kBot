import urllib
import urllib2
import json
import re
from bs4 import BeautifulSoup


def check_link(msg):
    links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)
    if len(links) > 0:
        return links[0]
    else:
        return False


def read_link(url):
    try:
        response = urllib.urlopen(url)
        results = response.read()
        info = response.info()
        info_type = info.type.split('/')
        if info_type[1] == 'html':
            results = response.read()
            soup = BeautifulSoup(results)
            url_title = soup.title.string
            return url_title.encode('utf-8')
        else:
            return '[' + info_type[0] + '][' + info_type[1] + '] ' + info.getheaders('Content-Length')[0] + ' bytes'
    except IOError:
        print exc
        return False
    except Exception, exc:
        print exc
        return False
