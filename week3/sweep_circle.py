"""Example 2: turn the shoulder from 0 to 180 degrees, elbow straight.

Run it from the week3 folder:  python sweep_circle.py
"""
import numpy as np
import mujoco

model = mujoco.MjModel.from_xml_path("../two_link_arm.xml")
data = mujoco.MjData(model)

for deg in range(0, 181, 30):
    data.qpos[:] = np.radians([deg, 0])   # elbow straight
    mujoco.mj_kinematics(model, data)     # positions only
    x, y, _ = data.site("hand").xpos
    r = np.hypot(x, y)
    print(f"{deg:3d} deg  hand ({x:6.3f}, {y:6.3f})  r = {r:.3f}")
