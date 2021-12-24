# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 11:59:01 2021

@author: zhoup
"""


# Author: Gael Varoquaux <gael dot varoquaux at normalesup.org>
# Copyright (c) 2009, Enthought, Inc.
# License: BSD style.

import numpy as np
from mayavi import mlab
import sys

################################################################################
# Disable the rendering, to get bring up the figure quicker:
figure = mlab.gcf()
mlab.clf()
figure.scene.disable_render = True

# Creates two set of points using mlab.points3d: red point and
# white points
x1, y1, z1 = np.random.random((3, 10))
red_glyphs = mlab.points3d(x1, y1, z1, color=(1, 0, 0),
                resolution=20)

x2, y2, z2 = np.random.random((3, 10))
white_glyphs = mlab.points3d(x2, y2, z2, color=(0.9, 0.9, 0.9),
                resolution=20)


# Add an outline to show the selected point and center it on the first
# data point.
outline = mlab.outline(line_width=3)
outline.outline_mode = 'cornered'
outline.bounds = (x1[0]-0.1, x1[0]+0.1,
                  y1[0]-0.1, y1[0]+0.1,
                  z1[0]-0.1, z1[0]+0.1)

# Every object has been created, we can reenable the rendering.
figure.scene.disable_render = False
################################################################################


# Here, we grab the points describing the individual glyph, to figure
# out how many points are in an individual glyph.
g1 = red_glyphs.glyph.glyph_source.glyph_source.output.points.to_array()
g2 = white_glyphs.glyph.glyph_source.glyph_source.output.points.to_array()
print(g1,g2)

red_glyphs.actor.property.color = (1,1,0)
red_glyphs.actor.property.point_size = 50


def picker_callback(picker):
    """ Picker callback: this get called when on pick events.
    """
    if picker.actor in red_glyphs.actor.actors:
        # Find which data point corresponds to the point picked:
        # we have to account for the fact that each data point is
        # represented by a glyph with several points
        print(picker.point_id)
        point_id = int(picker.point_id/g1.shape[0])
        print(point_id)
        # If the no points have been selected, we have '-1'
        if point_id != -1:
            # Retrieve the coordinates coorresponding to that data
            # point
            x, y, z = x1[point_id], x1[point_id], x1[point_id]
            # Move the outline to the data point.
            outline.bounds = (x-0.1, x+0.1,
                              y-0.1, y+0.1,
                              z-0.1, z+0.1)
    elif picker.actor in white_glyphs.actor.actors:
        point_id = int(picker.point_id/g2.shape[0])
        # If the no points have been selected, we have '-1'
        if point_id != -1:
            # Retrieve the coordinates coorresponding to that data
            # point
            x, y, z = x2[point_id], x2[point_id], x2[point_id]
            # Move the outline to the data point.
            outline.bounds = (x-0.1, x+0.1,
                              y-0.1, y+0.1,
                              z-0.1, z+0.1)


picker = figure.on_mouse_pick(picker_callback)

# Decrease the tolerance, so that we can more easily select a precise
# point.
picker.tolerance = 0.01

mlab.title('Click on red balls')

mlab.show()