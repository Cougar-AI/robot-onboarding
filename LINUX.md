# Linux desktop: prepare packages and Git, then clone

These commands target **Ubuntu 22.04 / 24.04**. On another distribution, use its package manager and the equivalent graphics libraries. Open Terminal in your local desktop session (an SSH-only session may have no display).

## 1. Install Git and the graphics libraries

```bash
sudo apt update
sudo apt install -y curl ca-certificates git
sudo apt install -y libgl1 libglfw3 mesa-utils
```

## 2. Clone the project into your home folder

```bash
cd ~
git clone https://github.com/Cougar-AI/robot-onboarding.git
cd robot-onboarding
```

## 3. Open it in VS Code

Install VS Code (<https://code.visualstudio.com/Download>): download the `.deb` package and open it with your software installer. Then:

```bash
code .
```

**Next:** [README.md, section 2](README.md#2-open-the-folder-in-vs-code) onward.
