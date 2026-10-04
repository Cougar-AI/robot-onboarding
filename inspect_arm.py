"""Open the project URDF at its zero reference pose without running dynamics.

Windows WSL / Linux: python inspect_arm.py --model path/to/Arm.urdf
macOS:               mjpython inspect_arm.py --model path/to/Arm.urdf
Import check only:    python inspect_arm.py --model path/to/Arm.urdf --check

The URDF's continuous joints have no actuators or finite limits. This is a
static model inspection, not a simulation of motors or a hardware controller.
"""
import argparse
from pathlib import Path
import time

import mujoco
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    model = mujoco.MjModel.from_xml_path(str(args.model.resolve()))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    print(f"MuJoCo {mujoco.__version__}: nq={model.nq}, nv={model.nv}, nu={model.nu}")
    assert np.isfinite(data.xpos).all(), "Model transforms contain non-finite values"
    for joint_id in range(model.njnt):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, joint_id)
        print(f"  qpos[{model.jnt_qposadr[joint_id]}]: {name}")
    print("Import check passed. Reference pose is qpos=0; this is not a calibrated home pose.")
    if args.check:
        return
    from mujoco import viewer as viewer_module
    with viewer_module.launch_passive(model, data) as viewer:
        with viewer.lock():
            viewer.cam.lookat[:] = [-0.035, 0, 0.415]
            viewer.cam.distance = 1.52
            viewer.cam.azimuth = 130
            viewer.cam.elevation = -15
        while viewer.is_running():
            # Leave dynamics stopped so the unactuated arm stays visible.
            viewer.sync()
            time.sleep(1 / 60)


if __name__ == "__main__":
    main()
