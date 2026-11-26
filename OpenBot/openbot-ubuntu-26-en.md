# OpenBot on Ubuntu 26.04 (AMD64 / x86_64)

[Português](./openbot-ubuntu-26.md) · [Español](./openbot-ubuntu-26-es.md) · [English](./openbot-ubuntu-26-en.md)

**Official website:** https://openbot.run/

## Prepare Ubuntu

Open Terminal and refresh the package list:

```bash
sudo apt update
```

This command does not install or upgrade any applications.

## Download OpenBot from the official website

- Open https://openbot.run/ in Firefox.
- Click **Download for Linux**.
- Check that the Linux build is for **x86_64 / AMD64** and comes as an **AppImage**.
- Save the file in **Downloads**.

The website can detect Linux, but that does not mean all dependencies are installed.

## Launch the app

### Without the terminal: Gear Lever (tested in the video)

On Ubuntu 26.04, the OpenBot AppImage was launched with [Gear Lever](https://flathub.org/en/apps/it.mijorus.gearlever), a graphical app that opens AppImages and adds them to the app menu.

- In **Bazaar**, search for **Gear Lever** and install it.
- Open Gear Lever and drag the OpenBot AppImage from **Downloads** into the Gear Lever window.
- Click **Move to the app menu** to add OpenBot to the app menu. Then click **Launch** to open it. If you just want to try it without adding it to the menu, click **Launch** directly.

### Alternative: launch it directly from the file manager

- Open the **Files** app.
- If needed, create an **Applications** folder in your home directory.
- Move the AppImage from **Downloads** to **Applications**.
- Under **Properties → Permissions**, enable file execution if that option is available.

If the option isn't available, run:

```bash
chmod +x "$HOME"/Applications/OpenBot-*-x86_64.AppImage
```

Double-click the AppImage to try opening it. **Don't install dependencies in advance; first see whether the app opens.**

## Only if the app won't open

**FUSE / fusermount3 error:** check whether the command is available:

```bash
command -v fusermount3
```

If no path is printed, install the dependency and try again:

```bash
sudo apt install fuse3
```

**Sandbox or user namespace error:** on Ubuntu 26.04, OpenBot may need an AppArmor profile, as described in the official documentation. If you see this error, run:

```bash
curl -fL -o /tmp/openbot.apparmor https://raw.githubusercontent.com/nightly-labs/openbot/main/build/linux/openbot.apparmor
```

Review the downloaded file:

```bash
cat /tmp/openbot.apparmor
```

Install the official profile and reload AppArmor:

```bash
sudo install -m 0644 /tmp/openbot.apparmor /etc/apparmor.d/openbot
sudo systemctl reload apparmor
```

If `curl` is not installed, install it before downloading the profile (`sudo apt install curl`). Do not work around the issue with `--no-sandbox`.

Keep the AppImage in `~/Applications` so its location matches the path in the profile.
