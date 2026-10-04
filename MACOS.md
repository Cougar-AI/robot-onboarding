# Mac: prepare Terminal and Git, then clone

MuJoCo 3.10.0 supports macOS 11 and later. For current VS Code, use a supported macOS version. Older Mac? Ask a lead.

## 1. Open Terminal and note your chip

1. Open **Applications > Utilities > Terminal**.
2. Open **Apple menu > About This Mac**. An M1/M2/M3/M4 chip is **Apple Silicon**; otherwise it is an **Intel** Mac.
3. On Apple Silicon, use a native Terminal session (not "Open using Rosetta").

## 2. Make sure Git is installed

```bash
git --version
```

If macOS offers to install the **Command Line Tools**, accept and wait for the install to finish. Then run `git --version` again.

## 3. Clone the project into your home folder

```bash
cd ~
git clone https://github.com/Cougar-AI/robot-onboarding.git
cd robot-onboarding
```

## 4. Open it in VS Code

Install VS Code (<https://code.visualstudio.com/Download>): open the `.dmg` and drag **Visual Studio Code.app** to **Applications**. Then use **File > Open Folder** and choose `robot-onboarding` in your home folder.

Optional shortcut: in VS Code press **Cmd+Shift+P**, run **Shell Command: Install 'code' command in PATH**, restart Terminal, then `code .` opens the current folder.

On macOS, run the MuJoCo viewer with `mjpython` (for example `mjpython demo.py`). After you create `.venv` (README section 3), run the **Mac only** `ln -sf ...` command there once; without it `mjpython` cannot find uv's Python library.

**Next:** [README.md, section 2](README.md#2-open-the-folder-in-vs-code) onward.
