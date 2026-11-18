"""The simulation loop, live in the viewer: the same motor move as Example 3.

Run it from the week3 folder:
  Windows (WSL 2), Linux:  python watch_it.py
  macOS:                   mjpython watch_it.py
Close the viewer window to stop. (On Linux/WSL, Ctrl+C skips the clean close at the end.)
"""
import time

import numpy as np
import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("../two_link_arm.xml")
data = mujoco.MjData(model)
data.ctrl[:] = np.radians([30, 60])

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        start = time.time()
        mujoco.mj_step(model, data)    # physics
        viewer.sync()                  # show it
        wait = model.opt.timestep - (time.time() - start)
        time.sleep(max(wait, 0))       # real time

# Linux/WSL only: let the viewer close cleanly before Python exits.
# (Same fix as demo.py; without it the window can crash or hang on close.)
import atexit, platform, threading
if platform.system() != "Darwin":
    for thread in threading.enumerate():
        if thread is not threading.main_thread():
            thread.join(timeout=5)
    import glfw
    atexit.unregister(glfw.terminate)
