# -*- coding: utf-8 -*-
# vispy: gallery 10
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

""" Demonstrates use of visual.Markers to create a point cloud with a
standard turntable camera to fly around with and a centered 3D Axis.
"""

import numpy as np
import vispy.scene
from vispy.scene import visuals
import vispy.app as app

import pickle 

#
# Make a canvas and add simple view
#
with open("./episode_1.pkl", "rb") as f:
    data = pickle.load(f)
canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()


idx = 0
pos = data["flex_states"][0, idx, :, :3]
scatter = visuals.Markers()
scatter.set_data(pos, edge_color=None, face_color=(1, 1, 1, .5), size=5)

view.add(scatter)

view.camera = 'turntable'  # or try 'arcball'

# add a colored 3D axis for orientation
axis = visuals.XYZAxis(parent=view.scene)

reverse = False 
def update(event):
    global pos,idx, reverse
    if not reverse:
        idx += 1
    else:
        idx -= 1
    if idx == 59:
        reverse=True
    elif idx == 0:
        reverse = False
    scatter.set_data(pos=data["flex_states"][0, idx, :, :3])


timer = app.Timer(interval="1.1")
timer.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1:
        vispy.app.run()
