import os
import time

import numpy as np
import mujoco
import mujoco.viewer

# Path to the SO-101 model (expanduser turns ~ into your home folder)
MODEL_PATH = os.path.expanduser(
    r"~\Documents\GitHub\SO-ARM100\Simulation\SO101\scene.xml"
)

model = mujoco.MjModel.from_xml_path(MODEL_PATH)  # the arm's description
data = mujoco.MjData(model)                       # its current state

# NEW: list every body (rigid part) of the arm, so we can find the gripper's name
for i in range(model.nbody):
    print(i, model.body(i).name)

GRIPPER = "gripper"   # NEW: change this if the list shows a different name

step = 0  # NEW: counts loop ticks

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        data.ctrl[0] = 0.5 * np.sin(data.time)

        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)

        # NEW: every 250 ticks (about half a second), print the gripper's position
        if step % 250 == 0:
            x, y, z = data.body(GRIPPER).xpos
            print(f"t={data.time:4.1f}s   x={x:+.3f}  y={y:+.3f}  z={z:+.3f}  (metres)")
        step += 1