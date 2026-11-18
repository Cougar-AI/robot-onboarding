# Robot Arm Software / Simulation Onboarding

**CougarAI × Robotics@UH · Robot Arm Project · First simulation milestone: October 13, 2026**

In this onboarding you will:

1. **Clone** this repository with Git.
2. Open it in **VS Code**, with the Explorer and the integrated terminal.
3. Run a six-joint MuJoCo home-to-goal exercise.
4. Get updates with **`git pull`**.

You do not need prior Linux experience.

| Your computer | Prepare it first | Terminal for every command below |
|---|---|---|
| Windows | [WINDOWS_WSL2.md](WINDOWS_WSL2.md): WSL 2 + Ubuntu 24.04 | **Ubuntu** (inside WSL), not PowerShell |
| Mac | [MACOS.md](MACOS.md): Terminal + Git | **Terminal** |
| Linux desktop | [LINUX.md](LINUX.md): Ubuntu packages + Git | **Terminal** |

We use **Python 3.11 + MuJoCo 3.10.0**. This version has native packages for Intel Macs, Apple Silicon Macs and Linux. `uv` installs Python and keeps this project's packages in its own environment. [MuJoCo 3.10.0 files](https://pypi.org/project/mujoco/3.10.0/), [uv](https://docs.astral.sh/uv/)

Type commands one line at a time and press Enter after each line. A leading `$` in other guides is the prompt; do not type it. A password prompt shows no characters while you type; that is normal.

## 1. Clone the project

Run these in the terminal from the table above (Windows: the **Ubuntu** terminal).

```bash
cd ~
git clone https://github.com/Cougar-AI/robot-onboarding.git
cd robot-onboarding
ls
```

`git clone` makes the folder `~/robot-onboarding` with every file and its version history. `ls` must list `demo.py`, `arm_demo.xml`, `requirements.txt` and `RobotArm_Model`.

Clone once. If Git says `destination path 'robot-onboarding' already exists`, you already have it: run `cd ~/robot-onboarding` and `git pull` instead.

## 2. Open the folder in VS Code

Install VS Code from <https://code.visualstudio.com/Download>. In VS Code, open **Extensions** and install **Python** by Microsoft. On Windows, also install **WSL** by Microsoft.

From the project folder in your terminal:

```bash
code .
```

The period means "this folder".

- **Windows:** `code .` from Ubuntu opens VS Code connected to WSL. The lower-left corner must say **WSL: Ubuntu**.
- **Mac:** if `code` is not found, use **File > Open Folder** and choose `robot-onboarding`. Optional: install the `code` command with **Cmd+Shift+P**, then **Shell Command: Install 'code' command in PATH**.

Check the **Explorer** pane: it lists `demo.py`, `arm_demo.xml` and `RobotArm_Model`. Then open **Terminal > New Terminal**. This integrated terminal starts in the project folder. Run all remaining commands there.

```bash
pwd
git status
```

`pwd` ends in `/robot-onboarding`. `git status` says `On branch main` and `nothing to commit, working tree clean`.

## 3. Install uv, Python and MuJoCo

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close the terminal (trash-can icon) and open **Terminal > New Terminal** again, so the new `uv` command is found. Then:

```bash
uv --version
uv python install 3.11
uv venv --python 3.11 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Mac only:** run this once after creating `.venv`, with `.venv` activated, so `mjpython` can find uv's Python library. It works from any folder in the project. Without it, `mjpython` stops with `Library not loaded: @executable_path/../lib/libpython3.11.dylib` ([MuJoCo issue #1923](https://github.com/google-deepmind/mujoco/issues/1923)).

```bash
ln -sf "$(python -c 'import sys; print(sys.base_prefix)')/lib/libpython3.11.dylib" "$VIRTUAL_ENV/lib/"
```

Run it again if you ever delete and re-create `.venv`.

If `uv` is still missing, run the shell setup command that the installer printed, or `source "$HOME/.local/bin/env"`. [Official uv installation](https://docs.astral.sh/uv/getting-started/installation/)

**VS Code:** press **Ctrl+Shift+P** (Mac: **Cmd+Shift+P**), run **Python: Select Interpreter**, and choose this project's `.venv`. Its path ends in `.venv/bin/python`.

## 4. Check the environment

```bash
python -c "import sys; print(sys.executable)"
python -c "import platform; print(platform.machine())"
python -c "import mujoco; print(mujoco.__version__)"
```

| Check | Expected |
|---|---|
| Python path | ends in `.venv/bin/python` |
| Mac architecture | `arm64` on Apple Silicon, `x86_64` on Intel |
| MuJoCo version | `3.10.0` |

Every time you open a new terminal for this project:

```bash
cd ~/robot-onboarding
source .venv/bin/activate
```

## 5. Run the exercise

First test the physics without a window:

```bash
python demo.py --headless
```

The output ends with `PASS: home-to-goal physics test completed.` and reports 6 joint positions, 6 actuators and a max joint error below 0.05 rad.

Then watch the arm move:

```bash
# Windows WSL / Linux desktop
python demo.py
```

```bash
# macOS
mjpython demo.py
```

The arm moves for 4 simulated seconds and holds the goal until 8 seconds. Leave the window open. On macOS, `mjpython` comes with MuJoCo and is required for its passive viewer. [Viewer documentation](https://mujoco.readthedocs.io/en/stable/python.html#passive-viewer)

The six targets are joint angles in radians, ordered `j1` to `j6`:

```python
home = [0, 0, 0, 0, 0, 0]
goal = [0.6, -0.7, 1.0, 0.4, -0.5, 0.4]
```

`data.ctrl` holds the position-actuator targets. `mujoco.mj_step` calculates the next state. `viewer.sync` displays it. The test checks that the largest final joint error is below **0.05 rad**.

**This is a teaching arm.** It checks your software setup and a basic control loop:

- Its geometry and inertias are simplified.
- Gravity is zero.
- Arm collisions are off.

It is not the physical Robot Arm Project model.

## 6. Get updates with `git pull`

The leads add files and fixes to this repository. Get them from the integrated terminal:

```bash
cd ~/robot-onboarding
git pull
```

`Already up to date.` means you have the newest version. Otherwise Git lists the files that changed.

Experiment in a copy, so `git pull` never collides with your edits:

```bash
cp demo.py my_demo.py
```

If `git pull` says your local changes would be overwritten:

1. Run `git status` to see the changed file.
2. Save your version as a copy.
3. Run `git restore <file>`, then `git pull` again.

## 7. Open the project's robot model

`RobotArm_Model/Arm.urdf` and its seven meshes are a checked copy of the selected project model ([source](https://github.com/Cougar-AI/robotarm-cai-ruh/tree/main/software/robotviewer/models/RobotArm)). Keep `Arm.urdf` and `meshes/` together.

```bash
python inspect_arm.py --model RobotArm_Model/Arm.urdf --check
```

Expected: `MuJoCo 3.10.0: nq=6, nv=6, nu=0`, six named joints, and `Import check passed.`

Open a static view:

```bash
# Windows WSL / Linux desktop
python inspect_arm.py --model RobotArm_Model/Arm.urdf
```

```bash
# macOS
mjpython inspect_arm.py --model RobotArm_Model/Arm.urdf
```

The viewer holds the file's zero reference pose. Close the window when you finish.

**Before the October 13 milestone, agree with Jonathan on the real joint mapping, limits, home/goal poses and actuators.** The model has six continuous hinge joints, no actuators and no finite angle limits. A pose preview with `qpos` + `mj_forward` is kinematic; it does not test motor control.

## 8. Troubleshooting

| Message or symptom | First step |
|---|---|
| `git: command not found` | Windows/Linux (Ubuntu): `sudo apt install -y git`. Mac: run `git --version` and accept the Command Line Tools install. |
| `destination path 'robot-onboarding' already exists` | You cloned before. `cd ~/robot-onboarding`, then `git pull`. |
| Windows: `PS C:\...>` prompt, or VS Code shows no **WSL: Ubuntu** label | You are in PowerShell / Windows. Open **Ubuntu**, then `cd ~/robot-onboarding` and `code .`. Clone inside Ubuntu, not in PowerShell. |
| `code: command not found` (Mac) | Use **File > Open Folder**, or install the `code` command (section 2). |
| `uv: command not found` | Open a new terminal, or run the PATH command the installer printed. |
| `command not found: python` (Mac) or `Command 'python' not found` (Ubuntu/WSL) | The environment is not active. Run `source ~/robot-onboarding/.venv/bin/activate` (it works from any folder). Do not install `python-is-python3` or switch to `python3`. |
| `No module named 'mujoco'` (or `'numpy'`) | Run `source ~/robot-onboarding/.venv/bin/activate`, then `uv pip install -r ~/robot-onboarding/requirements.txt` (both work from any folder). Then run the same command again. In VS Code, select the `.venv` interpreter. |
| Mac: `` `launch_passive` requires ... `mjpython` `` | Run the same script with `mjpython` instead of `python` in the activated environment, for example `mjpython demo.py` or `mjpython watch_it.py`. |
| Mac: `mjpython` says `Library not loaded: @executable_path/../lib/libpython3.11.dylib` | Run the **Mac only** `ln -sf ...` command from section 3, then the same `mjpython` command again. |
| Linux / WSL: `Segmentation fault (core dumped)` or a hang **after** `PASS` | Run `git pull`: the current `demo.py` and `inspect_arm.py` wait for the viewer to close cleanly. The physics result above it was already valid. |
| Apple Silicon prints `x86_64` | Use a native Terminal (not Rosetta) and make a new `.venv`. |
| `ParseXML: Error opening file ... arm_demo.xml` | Keep `arm_demo.xml` beside `demo.py`. Run `git status`; `git restore arm_demo.xml` brings it back. |
| `ParseXML: Error opening file '../two_link_arm.xml'` (or `'../teaching_arm_6dof.xml'`) | You are not in `week3`. Run `cd ~/robot-onboarding/week3`, then start the script by its name only, without `week3/` (for example `python check_fk.py`). Type Week 3 commands in the terminal: VS Code's **Run** button starts in the repo root. |
| `python: can't open file '.../check_fk.py'` (or another Week 3 script) | You are not in `week3`. Run `cd ~/robot-onboarding/week3`, then the same command again. |
| WSL window does not open | PowerShell: `wsl -l -v` must show VERSION 2. Save work, then `wsl --update` and `wsl --shutdown`, and reopen Ubuntu. |
| Linux / WSL display or OpenGL error | `echo "$DISPLAY"` and `glxinfo -B`. `llvmpipe` means software rendering: update the graphics driver. |

Do not add guessed `DISPLAY`, `GALLIUM_DRIVER` or `LD_PRELOAD` values to your shell profile. [WSLg display troubleshooting](https://github.com/microsoft/wslg/wiki/Diagnosing-%22cannot-open-display%22-type-issues-with-WSLg)

## 9. What to share by October 13, 2026

- Your OS, CPU architecture, Python version and MuJoCo version.
- A screenshot of the working viewer and the test output.
- Your home and goal joint vectors in radians, with the joint order.
- A clip or screenshots of the team's chosen robot moving home → goal.
- Your script, model path/revision, run commands and any blocker.

The teaching demo is the setup check. The milestone is the team's robot moving between agreed poses. Contact **Jonathan Gaucin, Software / Simulation**.

## Week 2: check forward kinematics in MuJoCo

The "Frames, joints and forward kinematics" lesson uses two models. Get them with `git pull`:

| File | What it is |
|---|---|
| `two_link_arm.xml` | The flat 2-link arm: L1 = 0.40 m (blue), L2 = 0.30 m (orange). Both joints turn about z. |
| `teaching_arm_6dof.xml` | The red 6-joint teaching arm: shoulder at H = 0.20 m, L1 = 0.40 m, elbow to hand 0.30 m with the wrist straight. |
| `fk_check.py` | Sets the joint angles, runs `mj_forward` and prints where the hand is. |

In the activated environment:

```bash
python fk_check.py two_link 30 60
python fk_check.py teaching_arm 0.60 0.55 -1.00 0 0 0
```

Expected: `hand = (0.346, 0.500) m` and `hand = (0.504, 0.345, 0.279) m`, the same as the worked examples on the slides. `two_link` takes 2 angles in degrees. `teaching_arm` takes 6 angles in radians, ordered `j1` to `j6`. Use your own exercise angles to check your hand calculations.

These are teaching arms, not the project arm. The project arm is `RobotArm_Model/Arm.urdf` (section 7).

## Week 3: MuJoCo basics (model, loop, move, read)

The Week 3 scripts are in `week3/`. Get them with `git pull`, then run every command from that folder, typed in the terminal. The scripts load the models one folder up (`../two_link_arm.xml`). VS Code's **Run** button starts in the repo root instead, and the scripts then stop with `ParseXML: Error opening file`.

```bash
cd ~/robot-onboarding
git pull
cd week3
source ../.venv/bin/activate
```

`two_link_arm.xml` changed for Week 3: its joints are now named `shoulder` and `elbow` (the Week 2 slides call them j1 and j2), and each joint has a position motor (`shoulder_motor`, `elbow_motor`). `fk_check.py` and the Week 2 answers do not change.

| Script | What it does | Expected output (MuJoCo 3.10.0) |
|---|---|---|
| `check_fk.py` | Sets 30° and 60°, runs `mj_forward`, and prints the hand twice: from the Week 2 formula (`by hand:`) and from MuJoCo (`MuJoCo:`) | `MuJoCo:  (0.346, 0.500, 0.050)` |
| `read_by_name.py` | Reads a joint angle, a body position, a body's axes (`xmat`) and a site by name | `hand position:  [0.346 0.5   0.05 ]` |
| `sweep_circle.py` | Turns the shoulder 0° to 180° with the elbow straight | `r = 0.700` on every line |
| `move_with_motors.py` | Sets motor targets in `data.ctrl` and runs `mj_step` for 2 s | `2.00 s  30.0 60.0 deg  hand (0.346, 0.500)` |
| `check_arm6.py` | The same check on the 6-joint teaching arm | `hand = (0.504, 0.345, 0.279) m` |
| `watch_it.py` | The simulation loop, live in the viewer | the arm moves to 30°, 60° |

Open a model in MuJoCo's viewer (plain `python` works on every system):

```bash
python -m mujoco.viewer --mjcf=../two_link_arm.xml
```

`watch_it.py` uses `launch_passive`. On macOS run it with `mjpython watch_it.py` (do the **Mac only** step in section 3 first); on Windows (WSL) and Linux use `python watch_it.py`. It runs until you close the viewer window. Close the window to stop it: on Linux/WSL, Ctrl+C skips the clean close and can end with `Segmentation fault (core dumped)`, which is harmless.

`check_fk.py` also takes a model file, then two angles in degrees, for the edit-predict-check challenges: copy the model (`cp ../two_link_arm.xml my_arm.xml`), edit the copy, then run `python check_fk.py my_arm.xml 30 60`. It is not Week 2's `fk_check.py`: its first argument is a file, not an arm name like `two_link`.

If you edit `../two_link_arm.xml` itself (the motor TRY IT in class), undo it afterwards with `git restore ../two_link_arm.xml`, so `git pull` keeps working.

Check your Week 2 project-arm sketch: from `week3`, run `python -m mujoco.viewer --mjcf=../RobotArm_Model/Arm.urdf`. The arm has no motors, so it falls while the simulation runs. Press **Space** to pause and **Backspace** to reset it to the zero pose (straight up). Then open the **Joint** panel and drag one slider at a time. `Base_Joint_Joint1` is j1, `Joint_1_Joint2` is j2, and so on to `Joint_5_Revolute-10` (j6).

## Legacy: you downloaded a ZIP instead of cloning

GitHub's **Code > Download ZIP** gives `robot-onboarding-main.zip`. That copy has **no Git history**, so `git pull` does not work in it. Clone instead (section 1) when you can.

If you must use the ZIP:

1. Extract it.
2. Make `~/robot-onboarding` (`mkdir -p ~/robot-onboarding`).
3. Copy the extracted files into it, keeping `RobotArm_Model/meshes` intact.
   - **Windows:** in Ubuntu, run `cd ~/robot-onboarding && explorer.exe .` and paste the files into the window that opens.
4. Continue at section 2.

## Notes for leads

- MuJoCo is pinned to 3.10.0 because its release files include Intel Mac packages as well as Apple Silicon. Revisit the pin together before upgrading. [3.10.0 files](https://pypi.org/project/mujoco/3.10.0/)
- Verified on Apple Silicon macOS with Python 3.11.13 and MuJoCo 3.10.0, from a fresh `git clone` of this repository: headless exercise PASS, model import check passed.
- The viewer was also checked on Oct 4, 2026: 20 runs each of `demo.py` and `inspect_arm.py` on Ubuntu 24.04 (Linux container, X virtual display), and `mjpython` on Apple Silicon macOS, all exiting cleanly. Before the shutdown fix, 8 of 20 `demo.py` runs and 10 of 20 `inspect_arm.py` runs crashed, hung or aborted *after* the work was done.
- Real Windows/WSL machines, Linux desktops, Intel Macs and live viewer interaction were not tested here. Those steps follow the official Microsoft, uv and MuJoCo documentation.
