import sys
import random
from bisect import bisect
import cStringIO
import urllib
from PIL import Image

#####################################################################
#                                                                   #
# This code is an altered version of Jalal Sela's ascii draw from:  #
# https://jalalsela.wordpress.com/2015/03/19/modigliani-an-irc-bot/ #
#                                                                   #
#####################################################################

def draw_ascii(im_link):
    url = []
    url.append(im_link)
    scale = " $@B%&WM#ZQL*oahkbdpqwmCUYXzcvunxrft/\|()1{}[]?-_+~<>!lI;:,\"^`'. "
    scale= scale[::-1]
    zonebounds=range(4,256,4)
    url_string = ''

    try:
        imgfile = cStringIO.StringIO(urllib.urlopen(str(url[0])).read())
        im = Image.open(imgfile)
        height = (im.size[1] * 20) / (im.size[0])
        im = im.resize((50, height), Image.ANTIALIAS)
        im = im.convert('L')
        imgBuf=""
        for y in range(0,im.size[1]):
            imgBuf = ""
            for x in range(0,im.size[0]):
                lum = 255-im.getpixel((x,y))
                row = bisect(zonebounds,lum)
                possibles = scale[row]
                imgBuf  = imgBuf+possibles[random.randint(0,len(possibles)-1)]
            url_string = url_string + str(imgBuf) + '\n'
        return url_string
    except:
        e = sys.exc_info()
        return "Image failed to draw"
