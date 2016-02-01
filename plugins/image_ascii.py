import numpy as np
import cStringIO
import urllib
from PIL import Image

#####################################################################
#                                                                   #
# This code was inspired by Jalal Sela's ascii draw found at:       #
# https://jalalsela.wordpress.com/2015/03/19/modigliani-an-irc-bot/ #
#                                                                   #
#####################################################################

colors = { 0 : (255, 255, 255),
           1 : (0, 0, 0),
           2 : (0, 0, 127),
           3 : (0, 147, 0),
           4 : (255, 0, 0),
           5 : (127, 0, 0),
           6 : (156, 0, 156),
           7 : (252, 127, 0),
           8 : (255, 255, 0),
           9 : (0, 252, 0),
           10 : (0, 147, 147),
           11 : (0, 255, 255),
           12 : (0, 0, 252),
           13 : (255, 0, 255),
           14 : (127, 127, 127),
           15 : (210, 210, 210)
        }

def draw_ascii(im_link):
    zonebounds = range(4,256,4)
    url_string = ''

    try:
        imgfile = cStringIO.StringIO(urllib.urlopen(im_link).read())
        im = Image.open(imgfile)
        height = (im.size[1] * 20) / (im.size[0])
        im = im.resize((50, height), Image.ANTIALIAS)
        im_col = im.convert('RGB')
        imgBuf = ""
        for y in range(0,im.size[1]):
            imgBuf = ""
            for x in range(0,im.size[0]):
                light = get_color(im_col.getpixel((x,y)))
                imgBuf  = imgBuf + ("\x03" + str(light) + "," +
                                    str(light)  + "x\x03")
            url_string = url_string + str(imgBuf) + '\n'
        return url_string
    except:
        return "Image failed to draw"


def get_color(pixel_color):
    color_diff = [colors[0][i] - pixel_color[i] for i in xrange(3)]
    smallest_diff = np.linalg.norm(color_diff)
    closest_color = 0
    for c in colors.keys():
        color_diff = [colors[c][i] - pixel_color[i] for i in xrange(3)]
        diff = np.linalg.norm(color_diff)
        if diff < smallest_diff:
            closest_color = c
            smallest_diff = diff
    return closest_color