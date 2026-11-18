"""Example 4: the same check on the 6-joint teaching arm.

Run it from the week3 folder:  python check_arm6.py
"""
import mujoco

model = mujoco.MjModel.from_xml_path("../teaching_arm_6dof.xml")
data = mujoco.MjData(model)
data.qpos[:] = [0.60, 0.55, -1.00, 0, 0, 0]  # j1..j6 (rad)
mujoco.mj_forward(model, data)
x, y, z = data.site("hand").xpos
print(f"hand = ({x:.3f}, {y:.3f}, {z:.3f}) m")
