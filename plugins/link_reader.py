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
    response = urllib.urlopen(url)
    results = response.read()
    soup = BeautifulSoup(results)
    return soup.title.string
