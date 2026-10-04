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

**Mac only:** run this once after creating `.venv`, so `mjpython` can find uv's Python library. Without it, `mjpython` stops with `Library not loaded: @executable_path/../lib/libpython3.11.dylib` ([MuJoCo issue #1923](https://github.com/google-deepmind/mujoco/issues/1923)).

```bash
ln -sf "$(python -c 'import sys; print(sys.base_prefix)')/lib/libpython3.11.dylib" .venv/lib/
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
| `No module named 'mujoco'` | `source .venv/bin/activate`, then `uv pip install -r requirements.txt`. In VS Code, select the `.venv` interpreter. |
| Mac: ``launch_passive` requires ... `mjpython` `` | Run `mjpython demo.py` in the activated environment. |
| Mac: `mjpython` says `Library not loaded: @executable_path/../lib/libpython3.11.dylib` | Run the **Mac only** `ln -sf ...` command from section 3, then `mjpython demo.py` again. |
| Linux / WSL: `Segmentation fault (core dumped)` or a hang **after** `PASS` | Run `git pull`: the current `demo.py` and `inspect_arm.py` wait for the viewer to close cleanly. The physics result above it was already valid. |
| Apple Silicon prints `x86_64` | Use a native Terminal (not Rosetta) and make a new `.venv`. |
| `ParseXML: Error opening file ... arm_demo.xml` | Keep `arm_demo.xml` beside `demo.py`. Run `git status`; `git restore arm_demo.xml` brings it back. |
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
