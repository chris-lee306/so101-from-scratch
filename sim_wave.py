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

# Print each motor's number and name, so we know what ctrl[0], ctrl[1]... mean
for i in range(model.nu):
    print(i, model.actuator(i).name)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        # Swing motor 0 (the base) back and forth, like a wave
        data.ctrl[1] = 1 * np.sin(data.time)

        mujoco.mj_step(model, data)    # advance the physics one small step
        viewer.sync()                  # update the picture
        time.sleep(model.opt.timestep) # run at roughly real-time speed