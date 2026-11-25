# How to Turn a TV Box into an AI Gateway — Part 2

**Café com Dados & Gatos | New API and Telegram automations**

In this lab, the BTV BX will run New API as a gateway for artificial intelligence models and a Python bot for queries, summaries and monitoring through Telegram.

## Black screen and XRDP disconnection when XFCE is open over HDMI

**Observed symptom:** when signing into the BTV BX through Windows Remote Desktop using Xorg and the `teste` account, the password was accepted, a black screen appeared and the remote session ended almost immediately. SSH access continued working.

**Messages recorded in the logs:**

```text
Session started successfully for user teste on display 10
Window manager ... exited quickly (2 secs)
(xfwm4): Gtk-WARNING: cannot open display: :10.0
```

The `/home/teste/.xsession` configuration contained `startxfce4`, as expected. Next, the diagnostic commands showed:

```bash
loginctl list-sessions
ps -u teste -o pid,cmd | grep -E 'xfce4-session|xfwm4|Xorg'
```

The `teste` account already had a local `seat0` graphical session over HDMI, including `xfce4-session` and `xfwm4 --display :0.0`. **Cause identified on this device:** the XFCE session automatically opened over HDMI using the same `teste` account interfered with the creation of the XRDP session. Stopping the local session allowed remote login. The message `X server already running` alone does not indicate a failure.

**Successful test:** keep the SSH terminal open as `root`, **temporarily** stop the local login manager and, **before restarting it**, open Windows Remote Desktop.

```bash
systemctl stop display-manager
```

**Observed result:** with the local manager stopped, XRDP allowed login from Windows. This procedure stops the HDMI graphical interface but does not shut down Linux, SSH or the AI services. **Do not run `systemctl start display-manager` before testing XRDP**, because that reopens the local session.

**Restore HDMI after the temporary test:** log out of the remote graphical session and run the following in the same SSH session:

```bash
systemctl start display-manager
```

### Access only from Windows, without opening XFCE over HDMI

With 2 GB of RAM, it is preferable not to maintain two graphical sessions simultaneously. The BTV can operate without a monitor, using **SSH** (terminal), **XRDP** (graphical desktop) or an **SSH tunnel** (web dashboards/APIs). An SSH tunnel does not display a desktop.

Temporarily stopping the display manager resolved the disconnection in the test. To prevent the HDMI session from automatically returning after reboot, disable **LightDM** startup without removing XFCE or XRDP. Confirm the result after rebooting the BTV.

**Before making changes:** keep an SSH session open in PowerShell, confirm SSH works and XRDP is configured to start at boot. On the BTV, in the `root` shell:

```bash
systemctl is-enabled ssh
systemctl is-enabled xrdp
systemctl is-active xrdp
systemctl status lightdm --no-pager
```

If SSH is not enabled, fix that **before** disabling local graphical login. Do not disable SSH or XRDP. Do not expose port 3389 directly to the internet.

**Once remote access is confirmed**, disable only the local LightDM, immediately and for subsequent boots:

```bash
systemctl disable --now lightdm
```

This **does not uninstall** XFCE, LightDM or XRDP; it only stops the local login manager and disables its automatic activation. HDMI may have no graphical interface: this is expected. XRDP starts its own Xorg/XFCE session upon remote login. Source: [official systemctl manual](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) and [XRDP project](https://github.com/neutrinolabs/xrdp).

**Verification after the change:**

```bash
systemctl is-enabled lightdm
systemctl is-active lightdm
systemctl is-active xrdp
```

Expected result: `lightdm` disabled and inactive; `xrdp` active. Then log in from Windows using `mstsc`, user `teste`, Xorg session. **Reboot the BTV only after confirming remote access** and repeat the test after boot to verify that the behavior persists.

**To restore HDMI with automatic graphical login**, via SSH as `root`:

```bash
systemctl enable --now lightdm
```

**How to save RAM:** when finished using XRDP, choose **Log Out / End Session** from the XFCE menu instead of simply closing the Remote Desktop application window. Disconnecting alone may leave the session and its processes loaded for reconnection. When only a terminal or web dashboard is needed, prefer SSH/an SSH tunnel without starting XFCE.

**Important:** without HDMI, keep a record of the BTV IP and keep SSH accessible over the network. Operation after reboot still needs to be confirmed on this unit.

## API Gateway with a visual dashboard

### Download the binary

Visit https://github.com/QuantumNous/new-api/releases and download the Linux ARM64 binary for the BTV BX (version v1.0.0-rc.51 or later compatible with `HOST`).

Create the installation directory:

```bash
mkdir -p "$HOME/new-api"
```

Save the executable in `~/new-api` under the name `new-api`.

### Start New API

```bash
cd "$HOME/new-api"
chmod +x new-api
HOST=127.0.0.1 PORT=3000 ./new-api
```

Keep the terminal open.

### Access the visual dashboard

In the browser on the BTV itself:

```text
http://127.0.0.1:3000
```

To access it from the PC, open a tunnel in PowerShell, replacing the username and IP with those of your BTV:

```powershell
ssh -N -L 3300:127.0.0.1:3000 teste@192.168.1.100
```

In the PC browser:

```text
http://127.0.0.1:3300
```

### Configure New API

- Complete the initial setup and create the administrator account.
- Register a channel with the AI provider, provider key and desired models.
- Test the channel.
- Create an API key for the bot, granting access only to the required models and setting an appropriate usage limit.

### Start New API automatically with the TV Box

After completing initial setup, stop the manually running New API process with Ctrl+C. Run the commands below in the BTV terminal as a regular user. The service will start with the TV Box without needing to log in via SSH, access XRDP or keep a terminal open. The SSH tunnel is needed only to access the dashboard from the PC.

```bash
sudo tee /etc/systemd/system/new-api.service >/dev/null <<SERVICE
[Unit]
Description=Central IA - New API
Wants=network-online.target
After=network-online.target

[Service]
User=$USER
WorkingDirectory=$HOME/new-api
Environment=HOST=127.0.0.1
Environment=PORT=3000
ExecStart=$HOME/new-api/new-api
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE
sudo systemctl daemon-reload
sudo systemctl enable --now new-api.service
```

### Manage New API

Start:

```bash
sudo systemctl start new-api.service
```

Restart:

```bash
sudo systemctl restart new-api.service
```

Stop:

```bash
sudo systemctl stop new-api.service
```

Check whether it is enabled at boot and currently running:

```bash
systemctl is-enabled new-api.service
systemctl is-active new-api.service
```

Check status and logs:

```bash
systemctl status new-api.service --no-pager
sudo journalctl -u new-api.service -n 50 --no-pager
```

## Install Python 3

In the BTV terminal:

```bash
sudo apt update
sudo apt install -y python3 ca-certificates
python3 --version
mkdir -p "$HOME/central-ia"
```

The bot uses the Python standard library.

## Create the Telegram bot

The Telegram app can be used on a phone or computer. In the video, setup will be demonstrated on a computer for easier viewing. On the BTV BX we will run only the Python bot, which queries the New API endpoint (`http://127.0.0.1:3000/v1`) with the configured API key.

Open [@BotFather](https://t.me/BotFather), send `/newbot` and follow the instructions. Open the private conversation with the newly created bot and send `/start`.

## Configure credentials

Use the full token provided by BotFather for your own bot. Do not share the token or API key.

In the BTV terminal:

```bash
umask 077
read -r -s -p 'Token do BotFather: ' TG_TOKEN; echo
read -r -s -p 'Chave de API do New API: ' IA_KEY; echo
read -r -p 'Nome do modelo configurado no New API: ' IA_MODEL
printf 'BOT_TOKEN=%s\nIA_KEY=%s\nIA_MODEL=%s\nIA_URL=http://127.0.0.1:3000/v1\n' \
  "$TG_TOKEN" "$IA_KEY" "$IA_MODEL" > "$HOME/central-ia/telegram.env"
unset TG_TOKEN IA_KEY IA_MODEL
chmod 600 "$HOME/central-ia/telegram.env"
```

Do not publish the `telegram.env` file.

## Create the Python bot

The complete code is available in [telegram_central.py](./telegram_central.py). There is no need to copy the entire code into the terminal.

### Download the file to your computer

Open the file on GitHub, click **Download raw file** and save `telegram_central.py` in your computer's Downloads folder.

### Transfer the file to the BTV via SCP

Keep the SSH session open. Open another PowerShell window in Windows and run:

```powershell
scp "$HOME\Downloads\telegram_central.py" root@192.168.1.100:/root/central-ia/
```

Replace the IP with your TV Box address. The example uses the `root` user, as in the demonstration. If using another user, use the same account used to configure credentials and the `central-ia` directory in that account's home folder. Enter the SSH password if prompted.

### Verify the file on the BTV

Return to the BTV SSH terminal and run:

```bash
ls -l "$HOME/central-ia/telegram_central.py"
python3 -m py_compile "$HOME/central-ia/telegram_central.py"
```

If the second command shows no errors, proceed to chat authorization and bot testing.

## Authorize the chat and test

```bash
set -a
. "$HOME/central-ia/telegram.env"
set +a
python3 "$HOME/central-ia/telegram_central.py" bot
```

Send `/id` in the private conversation with the bot. Copy the returned number and stop the process with Ctrl+C.

```bash
read -r -p 'Seu chat_id: ' TG_CHAT_ID
printf 'ALLOWED_CHAT_ID=%s\n' "$TG_CHAT_ID" >> "$HOME/central-ia/telegram.env"
unset TG_CHAT_ID
set -a
. "$HOME/central-ia/telegram.env"
set +a
python3 "$HOME/central-ia/telegram_central.py" bot
```

In the conversation with your bot (not BotFather), send `/status` and `/ia Explain what an API is in one sentence`. Stop with Ctrl+C before creating the services.

## Start the bot automatically

Stop the manually running bot with Ctrl+C if it is still running. Run the block below in the BTV SSH terminal. The gateway service must be named `new-api.service`.

```bash
sudo tee /etc/systemd/system/central-telegram.service >/dev/null <<SERVICE
[Unit]
Description=Central IA - Telegram
Wants=network-online.target new-api.service
After=network-online.target new-api.service

[Service]
User=$USER
WorkingDirectory=$HOME/central-ia
EnvironmentFile=$HOME/central-ia/telegram.env
ExecStart=/usr/bin/python3 $HOME/central-ia/telegram_central.py bot
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE
sudo systemctl daemon-reload
sudo systemctl enable central-telegram.service
sudo systemctl restart central-telegram.service
systemctl is-active new-api central-telegram
```

## Schedule a news summary at 7 AM

### Check and adjust the time zone

In the BTV SSH terminal:

```bash
timedatectl
```

If the time zone is incorrect, adjust it to your city. In the video we use Campo Grande/MS:

```bash
timedatectl set-timezone America/Campo_Grande
```

If it returns `Failed to set time zone: Access denied`, check whether you are logged in as root:

```bash
id -u
```

If it returns `0`, try configuring the time zone directly:

```bash
test -f /usr/share/zoneinfo/America/Campo_Grande && \
  ln -sfn /usr/share/zoneinfo/America/Campo_Grande /etc/localtime && \
  echo "America/Campo_Grande" > /etc/timezone
date
timedatectl
```

Confirm that the time and time zone are correct before creating the schedule. For another city, replace `America/Campo_Grande` with the corresponding time zone (`timedatectl list-timezones`). If the direct change fails, do not proceed with scheduling until the time zone is corrected.

### Create the schedule

```bash
sudo tee /etc/systemd/system/central-resumo.service >/dev/null <<SERVICE
[Unit]
Description=Central IA - Resumo de manchetes
Wants=network-online.target new-api.service
After=network-online.target new-api.service

[Service]
Type=oneshot
User=$USER
EnvironmentFile=$HOME/central-ia/telegram.env
ExecStart=/usr/bin/python3 $HOME/central-ia/telegram_central.py resumo
SERVICE
sudo tee /etc/systemd/system/central-resumo.timer >/dev/null <<'TIMER'
[Unit]
Description=Central IA - Resumo diário

[Timer]
OnCalendar=*-*-* 07:00:00
Persistent=false

[Install]
WantedBy=timers.target
TIMER
sudo systemctl daemon-reload
sudo systemctl enable --now central-resumo.timer
sudo systemctl start central-resumo.service
```

## Monitor a website every 15 minutes

Enter the HTTPS URL of a website you own or have permission to monitor.

```bash
read -r -p 'URL do site: ' SITE_URL
printf 'MONITOR_URL=%s\n' "$SITE_URL" >> "$HOME/central-ia/telegram.env"
unset SITE_URL
sudo tee /etc/systemd/system/central-site.service >/dev/null <<SERVICE
[Unit]
Description=Central IA - Monitorar site
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
User=$USER
EnvironmentFile=$HOME/central-ia/telegram.env
ExecStart=/usr/bin/python3 $HOME/central-ia/telegram_central.py site
SERVICE
sudo tee /etc/systemd/system/central-site.timer >/dev/null <<'TIMER'
[Unit]
Description=Central IA - Monitorar site a cada 15 minutos

[Timer]
OnBootSec=2min
OnUnitActiveSec=15min

[Install]
WantedBy=timers.target
TIMER
sudo systemctl daemon-reload
sudo systemctl enable --now central-site.timer
sudo systemctl start central-site.service
```

The monitor checks the website every 15 minutes when the timer is active and sends notifications only when the observed state changes (including the first check). Manual notification testing worked; continuous automatic execution still needs to be validated. A single access failure does not mean the website is down for everyone.

## Test with the PC turned off

```bash
systemctl is-active new-api central-telegram
systemctl list-timers --all | grep central-
free -h
```

Turn off the PC, keep the TV Box connected to power and the internet, and test the bot from your phone.

## Official references

- [New API — Releases](https://github.com/QuantumNous/new-api/releases)
- [New API — Documentation](https://docs.newapi.ai/en/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python 3 — Debian](https://packages.debian.org/bookworm/python3)
- [systemd.timer](https://www.freedesktop.org/software/systemd/man/systemd.timer.html)

**Café com Dados & Gatos — Part 2.**