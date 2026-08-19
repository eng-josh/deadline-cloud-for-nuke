# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

"""Scene script for the write_node_frame_limit case — executed INSIDE GUI
Nuke by the suite's opener hook (test/nuke_submitter_ui/_opener/menu.py).

Contract: build the scene, then save it to the path named by the
NUKE_SUBMITTER_UI_SCENE_FILE environment variable. Keep everything
deterministic — the exported bundle is compared against committed goldens.

Two write nodes carry their own frame-range limits, 5-10 and 40-60, inside a
much wider scene range (1-100). The submitter prefers a selected write node's
own limit over the scene range when the override is off, so the golden's
Frames parameter can only be 5-10 if the limit came from the node that was
selected. With one limited node the case could not tell that apart from "some
node's limit was used".
"""

import os

import nuke

scene_file = os.environ["NUKE_SUBMITTER_UI_SCENE_FILE"]
scene_dir = os.path.dirname(scene_file)
renders_dir = os.path.join(scene_dir, "renders")

nuke.root()["first_frame"].setValue(1)
nuke.root()["last_frame"].setValue(100)

color_wheel = nuke.nodes.ColorWheel()
for node_name, first, last in (("Write1", 5, 10), ("Write2", 40, 60)):
    write_node = nuke.nodes.Write(name=node_name)
    write_node.setInput(0, color_wheel)
    write_node["file"].setValue(
        os.path.join(renders_dir, node_name.lower(), f"{node_name.lower()}.####.exr")
    )
    write_node["use_limit"].setValue(True)
    write_node["first"].setValue(first)
    write_node["last"].setValue(last)

nuke.scriptSaveAs(scene_file, overwrite=1)
