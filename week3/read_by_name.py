"""Read joints, bodies and sites by name. Pose: 30 and 60 degrees.

Run it from the week3 folder:  python read_by_name.py
"""
import numpy as np
import mujoco

model = mujoco.MjModel.from_xml_path("../two_link_arm.xml")
data = mujoco.MjData(model)
data.qpos[:] = np.radians([30, 60])   # radians!
mujoco.mj_forward(model, data)        # compute positions and axes

np.set_printoptions(precision=3, suppress=True)
print("shoulder angle:", data.joint("shoulder").qpos)
print("elbow position:", data.body("link2").xpos)
print("link 2 axes (xmat):")
print(data.body("link2").xmat.reshape(3, 3) + 0.0)
print("hand position: ", data.site("hand").xpos)
