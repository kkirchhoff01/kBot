import urllib
import urllib2
import json
import re
from bs4 import BeautifulSoup


# Check for URL in IRC message
def check_link(msg):
    # Regex for URL
    links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|' +
                       '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)

    # If URL was found len(lings) > 0
    if len(links) > 0:
        return links[0]  # Return first URL (don't want multiple searches)
    else:
        return False  # No URL found


# Function to fetch link info
def read_link(url):
    try:
        # Open link and get response
        response = urllib.urlopen(url)
        results = response.read()
        response.close()

        info = response.info()

        # URL is text/html web page
        if info.type == 'text/html':
            # Use BeautifulSoup to get info
            soup = BeautifulSoup(results)
            title_string = re.sub('[\r|\n]', ' ', soup.title.string)

            # Handle page summary longer than 200 characters
            if len(title_string) > 200:
                title_string = title_string[:200] + "..."

            # Return page info
            url_title = "[URL] {0}".format(title_string)
            return url_title.encode('utf-8')

        # URL is not HTML (download or image)
        else:
            # Get size of content
            content_size = float(info.getheaders('Content-Length')[0])

            # Format byte size to KB/MB/etc.
            if content_size < 1000.0:
                return "[%s] %.2f B" % (info.type, content_size)
            elif content_size > 1000.0 and content_size < 1000000:
                return "[%s] %.2f KB" % (info.type, content_size/1000.0)
            elif content_size > 1000000.0 and content_size < 1000000000.0:
                return "[%s] %.2f MB" % (info.type, content_size/1000000.0)
            elif content_size > 1000000000.0:
                return "[%s] %.2f GB" % (info.type, content_size/1000000000.0)

    except IOError, exc:  # Bad link
        return "[URL] Site not found"

    except AttributeError:  # No title information
        return "[URL] (No title)"

    except Exception, exc:  # Other exception; print error; return False
        print exc
        return False
