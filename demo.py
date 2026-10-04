"""MuJoCo onboarding: a six-joint teaching arm moves from home to goal.

Linux / WSL: python demo.py
macOS:       mjpython demo.py
Any OS:      python demo.py --headless

Keep arm_demo.xml beside this file. This model is only a setup exercise.
It is not the team's hardware model or a controller for physical motors.
"""

import argparse
from pathlib import Path
import platform
import time

import mujoco
import numpy as np

HOME_POSE = np.zeros(6)
GOAL = np.array([0.6, -0.7, 1.0, 0.4, -0.5, 0.4])  # radians: j1...j6
MOVE_SECONDS = 4.0
TOTAL_SECONDS = 8.0


def target_at(t):
    # Smooth start and stop over 4 simulation seconds, then hold the goal.
    progress = np.clip(t / MOVE_SECONDS, 0.0, 1.0)
    blend = progress * progress * (3.0 - 2.0 * progress)
    return HOME_POSE + blend * (GOAL - HOME_POSE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--headless", action="store_true", help="test physics without a window")
    args = parser.parse_args()
    model_path = Path(__file__).with_name("arm_demo.xml")
    model = mujoco.MjModel.from_xml_path(str(model_path))
    data = mujoco.MjData(model)
    data.qpos[:] = HOME_POSE
    data.ctrl[:] = HOME_POSE
    mujoco.mj_forward(model, data)
    print(f"Python {platform.python_version()} | {platform.system()} {platform.machine()}")
    print(f"MuJoCo {mujoco.__version__} | {model.nq} joint positions | {model.nu} actuators")
    print("Home [rad]:", HOME_POSE)
    print("Goal [rad]:", GOAL)

    def step():
        data.ctrl[:] = target_at(data.time)
        mujoco.mj_step(model, data)

    if args.headless:
        while data.time < TOTAL_SECONDS:
            step()
    else:
        from mujoco import viewer as viewer_module

        with viewer_module.launch_passive(model, data) as viewer:
            with viewer.lock():
                viewer.cam.lookat[:] = [0.35, 0.1, 0.3]
                viewer.cam.distance = 1.65
                viewer.cam.azimuth = 130
                viewer.cam.elevation = -25
            while viewer.is_running() and data.time < TOTAL_SECONDS:
                start = time.perf_counter()
                step()
                viewer.sync()
                time.sleep(max(0, model.opt.timestep - (time.perf_counter() - start)))

    error = float(np.max(np.abs(data.qpos - GOAL)))
    print("Final [rad]:", np.round(data.qpos, 4))
    print(f"Max joint error: {error:.6f} rad")
    if data.time + model.opt.timestep < TOTAL_SECONDS:
        print("Stopped early: rerun and leave the window open for the full motion.")
        raise SystemExit(1)
    if not np.isfinite(data.qpos).all() or error >= 0.05:
        print("CHECK: expected finite joint values and max error below 0.05 rad.")
        raise SystemExit(1)
    print("PASS: home-to-goal physics test completed.")


if __name__ == "__main__":
    main()
