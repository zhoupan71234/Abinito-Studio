# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 15:12:46 2021

@author: Administrator
"""

# import modules
from mayavi import mlab
import numpy as np
import pandas as pd
import networkx as nx

# set number of nodes
number = 6

# create random node positions
np.random.seed(5)
pos = 100*np.random.rand(6, 3)
print(pos)
pos = pd.DataFrame(pos, columns=['x', 'y', 'z'])

# create chain graph links
links = [(x, y) for x, y in zip(range(0, number-1), range(1, number))]

# create graph (not strictly needed, link list above would be enough)
graph = nx.Graph()
graph.add_edges_from(links)

# setup mayavi figure
figure = mlab.gcf()
mlab.clf()

# add nodes as individual glyphs
# store glyphs in dictionary to allow interactive adjustments of visibility
color = (0.5, 0.0, 0.5)
nodes = dict()
texts = dict()
for ni, n in enumerate(graph.nodes()):
    xyz = pos.loc[n]
    n = mlab.points3d(xyz['x'], xyz['y'], xyz['z'], scale_factor=5, color=color)
    label = 'node %s' % ni
    t = mlab.text3d(xyz['x'], xyz['y'], xyz['z']+5, label, scale=(5, 5, 5))
    # each glyph consists of many points
    # arr = n.glyph.glyph_source.glyph_source.output.points.to_array()
    nodes[ni] = n
    texts[ni] = t

# add edges as individual tubes
edges = dict()
for ei, e in enumerate(graph.edges()):
    xyz = pos.loc[np.array(e)]
    edges[ei] = mlab.plot3d(xyz['x'], xyz['y'], xyz['z'], tube_radius=1, color=color)


# define picker callback for figure interaction
def picker_callback(picker):
    # get coordinates of mouse click position
    cen = picker.pick_position
    print(cen)
    # compute Euclidean distance btween mouse position and all nodes
    dist = np.linalg.norm(pos-cen, axis=1)
    # get closest node
    ni = np.argmin(dist)
    # hide/show node and text
    n = nodes[ni]
    n.actor.property.color = (1,0,0)
#    n.visible = not n.visible
#    t = texts[ni]
#    t.visible = not t.visible
#    # hide/show edges
#    # must be adjusted if double-clicking should hide/show both nodes and edges in a reasonable way
#    for ei, edge in enumerate(graph.edges()):
#        if ni in edge:
#            e = edges[ei]
#            e.visible = not e.visible


# add picker callback
picker = figure.on_mouse_pick(picker_callback)
picker.tolerance = 0.01

# show interactive window
# mlab.show()

# collect visibility/deletion status of nodes, e.g.
# [(0, True), (1, False), (2, True), (3, True), (4, True), (5, True)]
[(key, node.visible) for key, node in nodes.items()]