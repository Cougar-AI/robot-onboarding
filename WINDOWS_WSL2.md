# Windows: prepare WSL 2 + Ubuntu, then clone

The robotics tools use a Linux terminal. WSL 2 runs Ubuntu inside Windows. After this page, **every command runs in the Ubuntu terminal**, not in PowerShell.

Windows 11 is preferred. WSLg, which shows Linux windows on Windows, also supports Windows 10 build 19044 or later. Install current Windows updates and your Intel, AMD or NVIDIA graphics driver. [Microsoft WSLg requirements](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps)

## 1. Install WSL 2 and Ubuntu

1. Open Start, search **PowerShell**, choose **Run as administrator**.
2. Run:

   ```powershell
   wsl --install -d Ubuntu-24.04
   ```

3. Restart Windows if asked. Open **Ubuntu 24.04** from Start.
4. Create a Linux username (simple, lowercase) and password. This account belongs to Ubuntu. The password prompt shows nothing while you type.
5. Back in PowerShell:

   ```powershell
   wsl --update
   wsl -l -v
   ```

The Ubuntu row must show **VERSION 2**. If it shows 1, run the command below. Use the exact name that `wsl -l -v` prints.

```powershell
wsl --set-version Ubuntu-24.04 2
```

[Microsoft install guide](https://learn.microsoft.com/en-us/windows/wsl/install)

If virtualization is unavailable, ask a lead for help enabling hardware virtualization in firmware. On a managed laptop without administrator access, use a lab computer or ask IT. Do not reset an existing WSL distribution.

## 2. Prepare Ubuntu (in the Ubuntu terminal)

```bash
sudo apt update
sudo apt install -y curl ca-certificates git
sudo apt install -y libgl1 libglfw3 mesa-utils
```

`sudo` asks for your Ubuntu password. `git` gets the project; the graphics libraries show the MuJoCo window.

## 3. Clone the project into your Linux home folder

```bash
cd ~
git clone https://github.com/Cougar-AI/robot-onboarding.git
cd robot-onboarding
```

Keep the project in the Linux home folder (`~`), not on the Windows `C:` drive. It is faster and the paths stay simple.

## 4. Open it in VS Code

Install VS Code on Windows (<https://code.visualstudio.com/Download>) and its **WSL** extension. Then, in Ubuntu:

```bash
code .
```

The lower-left corner of VS Code must say **WSL: Ubuntu**. Open **Terminal > New Terminal**; it runs in Ubuntu.

**Next:** [README.md, section 2](README.md#2-open-the-folder-in-vs-code) onward.
