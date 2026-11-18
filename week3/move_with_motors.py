"""Example 3: give the motors targets and let physics move the arm.

Run it from the week3 folder:  python move_with_motors.py
"""
import numpy as np
import mujoco

model = mujoco.MjModel.from_xml_path("../two_link_arm.xml")
data = mujoco.MjData(model)

data.ctrl[:] = np.radians([30, 60])   # motor targets
for step in range(1, 1001):           # 1000 x 0.002 s = 2 s
    mujoco.mj_step(model, data)       # physics
    if step % 125 == 0:               # every 0.25 s
        t1, t2 = np.degrees(data.qpos)
        x, y, _ = data.site("hand").xpos
        print(f"{data.time:4.2f} s  {t1:4.1f} {t2:4.1f} deg"
              f"  hand ({x:.3f}, {y:.3f})")
