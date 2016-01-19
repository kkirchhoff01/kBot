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
        if info.type == 'text/html':
            soup = BeautifulSoup(results)
            url_title = "[URL] %s" % soup.title.string
            return url_title.encode('utf-8')
        else:
<<<<<<< HEAD
            content_size = float(info.getheaders('Content-Length')[0])
            if content_size < 1000.0:
                return "[%s] %.2f B" % (info.type, content_size)
            elif content_size > 1000.0 and content_size < 1000000:
                return "[%s] %.2f KB" % (info.type, content_size/1000.0)
            elif content_size > 1000000.0 and content_size < 1000000000.0:
                return "[%s] %.2f MB" % (info.type, content_size/1000000.0)
            elif content_size > 1000000000.0:
                return "[%s] %.2f GB" % (info.type, content_size/1000000000.0)
=======
            info_type = info.type.split('/')
            content_size = float(info.getheaders('Content-Length')[0])
            if content_size < 1000.0:
                return '[' + info_type[0] + '][' + info_type[1] + '] ' + str(content_size) + ' B'
            elif content_size > 1000.0 and content_size < 1000000.0:
                return '[' + info_type[0] + '][' + info_type[1] + '] ' + str(content_size/1000.0) + ' Kb'
            elif content_size > 1000000.0 and content_size < 1000000000.0:
                return '[' + info_type[0] + '][' + info_type[1] + '] ' + str(content_size/1000000.0) + ' Mb'
            elif content_size > 1000000000.0:
                return '[' + info_type[0] + '][' + info_type[1] + '] ' + str(content_size/1000000000.0) + ' Gb'
>>>>>>> 6f3d788700426ac406f094b6b41e1584099cb136
    except IOError, exc:
        print exc
        return False
    except Exception, exc:
        print exc
        return False
