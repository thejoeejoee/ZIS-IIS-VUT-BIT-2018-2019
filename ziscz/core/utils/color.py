# coding=utf-8
from __future__ import unicode_literals


def scale(color, scale):
    """
    Scales a hex string by ``scalefactor``. Returns scaled hex string.

    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.

    >>> scale("#DF3C3C", .5)
    #6F1E1E
    >>> scale("#52D24F", 1.6)
    #83FF7E
    >>> scale("#4F75D2", 1)
    #4F75D2

    https://thadeusb.com/weblog/2010/10/10/python_scale_hex_color/
    """

    def limit(val, minimum=0, maximum=255):
        if val < minimum:
            return minimum
        if val > maximum:
            return maximum
        return val

    color = color.strip('#')

    if scale < 0 or len(color) != 6:
        return color

    r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)

    r = limit(r * scale)
    g = limit(g * scale)
    b = limit(b * scale)

    return "#%02x%02x%02x" % tuple(map(int, (r, g, b)))
