"""Example 1: check the Week 2 worked example in MuJoCo.

Run it from the week3 folder:
  python check_fk.py                      the 2-link arm, angles 30 and 60 degrees
  python check_fk.py my_arm.xml           your edited copy of the model
  python check_fk.py my_arm.xml 90 -90    other angles, in degrees
"""
import sys

import numpy as np
import mujoco

path = sys.argv[1] if len(sys.argv) > 1 else "../two_link_arm.xml"
angles = [float(a) for a in sys.argv[2:]] or [30, 60]  # degrees

model = mujoco.MjModel.from_xml_path(path)
data = mujoco.MjData(model)
data.qpos[:] = np.radians(angles)  # radians!
# Challenge c: a slide joint moves in meters, not degrees. Use that number as it is.
for j in range(model.njnt):
    if model.jnt_type[j] == mujoco.mjtJoint.mjJNT_SLIDE:
        data.qpos[j] = angles[j]
mujoco.mj_forward(model, data)        # compute positions


def fk_2link(t1, t2, L1=0.40, L2=0.30):  # Week 2
    x = L1*np.cos(t1) + L2*np.cos(t1 + t2)
    y = L1*np.sin(t1) + L2*np.sin(t1 + t2)
    return x, y


x, y = fk_2link(*np.radians(angles))
hand = data.site("hand").xpos
print(f"by hand: ({x:.3f}, {y:.3f})")
print(f"MuJoCo:  ({hand[0]:.3f}, {hand[1]:.3f}, {hand[2]:.3f})")
