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
        response.close()
        info = response.info()
        if info.type == 'text/html':
            soup = BeautifulSoup(results)
            title_string = re.sub('[\r|\n]', ' ', soup.title.string)
            if len(title_string) > 200:
                title_string = title_string[:200] + "..."
            url_title = "[URL] {}".format(title_string)
            return url_title.encode('utf-8')
        else:
            content_size = float(info.getheaders('Content-Length')[0])
            if content_size < 1000.0:
                return "[%s] %.2f B" % (info.type, content_size)
            elif content_size > 1000.0 and content_size < 1000000:
                return "[%s] %.2f KB" % (info.type, content_size/1000.0)
            elif content_size > 1000000.0 and content_size < 1000000000.0:
                return "[%s] %.2f MB" % (info.type, content_size/1000000.0)
            elif content_size > 1000000000.0:
                return "[%s] %.2f GB" % (info.type, content_size/1000000000.0)
    except IOError, exc:
        return "[URL] Site not found"
    except AttributeError:
        return "[URL] (No title)"
    except Exception, exc:
        print exc
        return False
