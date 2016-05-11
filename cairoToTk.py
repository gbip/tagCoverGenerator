'''

(c) Paul Florence 2016

This file is part of Mp3CoverGenerator.
Mp3CoverGenerator is free software: you can redistribute it and / or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

Mp3CoverGenerator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Foobar. If not, see < http://
    www.gnu.org / licenses / >.2
'''

import tkinter

#All the code below belong to Martin P. Hellwig

def _alpha_blending(rgba, back):
    "Return a rgb tuple composed from a rgba and back(ground) tuple/list."
    paired = zip(rgba[:-1], back)
    alpha = rgba[-1]
    tmp = list()
    for upper, lower in paired:
        blend = (((255 - alpha) * lower) + (alpha * upper)) / 255
        tmp.append(blend)

    return (tuple(tmp))


def convert(bgra_buffer, width, height):
    "Convert bgra buffer to photoimage put"
    idx = 0
    end = len(bgra_buffer)
    arguments = list()
    while idx < end:
        rgba = (ord(bgra_buffer[idx + 2]),
        ord(bgra_buffer[idx + 1]),
        ord(bgra_buffer[idx + 0]),
        ord(bgra_buffer[idx + 3]))
        back = (255, 255, 255)
        rgb = _alpha_blending(rgba, back)
        arguments += rgb
        idx += 4
    print("blah")
    template = ' '.join(height * ['{%s}' % (''.join(width*["#%02x%02x%02x"]))])
    return (template % tuple(arguments))


def photoimage_from_context(surface, width, height):
    "Return a Tkinter.PhotoImage with the content set to the rendered"
    image = tkinter.PhotoImage(width=width, height=height)
    data = convert(surface.get_data(), width, height)
    image.put(data)
    return (image)