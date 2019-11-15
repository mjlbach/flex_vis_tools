# -*- coding: utf-8
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
from vispy.visuals import transforms

import pickle

import matplotlib.cm as cm
#
# Make a canvas and add simple view
#


class Plot:
    def __init__(self):
        pass

    def update(self, event):
        if not self.reverse:
            self.idx += 1
        else:
            self.idx -= 1
        if self.idx == 59:
            self.reverse = True
        elif self.idx == 0:
            self.reverse = False
        self.scatter.set_data(pos=self.data["flex_states"][0, self.idx, :, :3], face_color=self.color_id)

    def plot(self):
        with open("./episode_1.pkl", "rb") as f:
            self.data = pickle.load(f)
        canvas = vispy.scene.SceneCanvas(keys="interactive", show=True, bgcolor="white")
        view = canvas.central_widget.add_view()

        self.idx = 0
        colors = cm.get_cmap("tab10")(np.linspace(0.0, 1.0, 10))
        self.color_id = colors[self.data["particle_ids"][0, self.idx, :, 1]]
        self.data["flex_states"][:, :, :, [0, 1, 2]] = self.data["flex_states"][:, :, :, [0, 2, 1]]
        pos = self.data["flex_states"][0, self.idx, :, :3]
        self.scatter = visuals.Markers()
        self.scatter.set_data(pos, edge_color=None, face_color=self.color_id, size=5)
        floor = visuals.Plane(width=5, height=5)
        wall = visuals.Plane(
            width=5, height=1, direction="+x", width_segments=4, height_segments=10
        )
        wall._mesh.color = "green"

        view.add(wall)
        wall.transform = transforms.STTransform(translate=(-2.5, 0.0, 0.5))
        view.add(self.scatter)
        view.add(floor)

        view.camera = "turntable"  # or try 'arcball'

        # add a colored 3D axis for orientation
        axis = visuals.XYZAxis(parent=view.scene)

        self.reverse = False

        timer = app.Timer(interval="1.1")
        timer.connect(self.update)
        timer.start(0.04)
        vispy.app.run()


if __name__ == "__main__":
    plot = Plot()
    plot.plot()
