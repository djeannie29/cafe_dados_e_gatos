# Lesson 05 — Hermes Agent: Backup, Update, and Restore on WSL2

How to back up Hermes Agent, update it from the terminal, and restore its data in the same Ubuntu/WSL2 installation.

**Prerequisite:** Hermes Agent must already be installed and configured. All commands below should be run in the **Ubuntu/WSL2 terminal**, except where Windows PowerShell is explicitly specified.

## Check the installation

```bash
hermes --version
hermes doctor
```

- `hermes --version`: displays the installed version.
- `hermes doctor`: checks the installation's health and identifies potential problems.

## Create a backup

```bash
BACKUP_FILE="$HOME/hermes-aula05-$(date +%Y%m%d-%H%M%S).zip"
hermes backup --output "$BACKUP_FILE"
```

- `BACKUP_FILE=...`: sets the backup file name and path, including the date and time to avoid overwriting an existing file.
- `hermes backup --output`: exports Hermes data to the specified ZIP file.

**Keep this terminal open until the restore is complete:** the `BACKUP_FILE` variable is available only in the current shell session.

## Verify the backup

### If the `unzip` command is not installed

If you see `unzip: command not found`, install the utility in Ubuntu/WSL2:

```bash
sudo apt update
sudo apt install -y unzip
```

- `apt update`: refreshes the list of available packages.
- `apt install -y unzip`: installs the tool used to test and extract ZIP files.

If `unzip` already works, skip this installation.

```bash
ls -lh "$BACKUP_FILE"
unzip -t "$BACKUP_FILE"
sha256sum "$BACKUP_FILE"
```

- `ls -lh`: confirms that the file exists and displays its size.
- `unzip -t`: checks that the ZIP file can be read without errors.
- `sha256sum`: calculates a file fingerprint (hash) so it can be compared with another copy.

**Keep a protected copy outside WSL2 before updating.** Compare the copy's hash with the original. The ZIP may contain tokens, configuration settings, and personal information; do not publish it on GitHub. Files and databases belonging to external tools such as Obsidian, OpenViking, and Hindsight may require separate backups.

## Check for available updates

```bash
hermes update --check
hermes update --plan
```

- `--check`: checks whether an update is available.
- `--plan`: shows the planned update actions without running them.

These options must be supported by your installed version. If they are not recognized, check `hermes update --help` before proceeding.

## Update Hermes from the terminal

```bash
hermes update --backup
```

Updates Hermes and requests an additional backup before updating, in versions that support this option. Use it only after verifying your earlier backup. If `--backup` is not available, consult `hermes update --help` to confirm how to use `hermes update` in your version.

## Check the installation after updating

```bash
hermes --version
hermes doctor
```

Displays the current version and checks whether the installation is still working.

## Restore the backup

You can import a backup even when the update has not caused any data loss, to demonstrate the complete process. **Importing a backup may overwrite current settings and data.** Keep the original backup, make sure there is no important new data, and stop any activity that writes to Hermes before proceeding.

```bash
hermes gateway list
hermes gateway stop
```

- `gateway list`: lists existing gateways.
- `gateway stop`: stops the gateway for the current profile. If other profiles have active gateways, stop them as well before restoring.

Confirm that the selected ZIP file exists and is intact:

```bash
test -n "$BACKUP_FILE" && test -f "$BACKUP_FILE" && unzip -t "$BACKUP_FILE"
```

This check succeeds only if the variable contains a valid path, the file exists, and the ZIP is intact. If you closed the terminal, set `BACKUP_FILE` to the correct file path again before proceeding.

```bash
hermes import "$BACKUP_FILE"
```

Imports the selected backup. Read the overwrite confirmation carefully before continuing. **Importing data does not roll back the program version.**

### If you closed the terminal and lost the variable

You can restore a backup by specifying its file name directly. For example:

```bash
hermes import hermes-aula05-20261114-163601.zip
```

**Replace `hermes-aula05-20261114-163601.zip` with the name of your own backup file.** This example works if you are in the directory where the ZIP was saved (in this case, the home directory). If you are in a different directory, provide the full file path. Before importing, confirm that the ZIP is intact and all affected gateways are stopped.

## Verify the restoration

```bash
hermes doctor
hermes
```

- `hermes doctor`: checks the installation after importing.
- `hermes`: starts the agent so you can test it.

Make sure the expected settings, profiles, skills, and memories are accessible. Check external integrations separately. If a gateway was running beforehand, restart it using your installation's usual procedure.

## If Hermes Desktop fails after restoration

If Hermes Desktop opens a blank window or shows a startup error, close the application and restart WSL2.

**In Windows PowerShell:**

```powershell
wsl --shutdown
```

- `wsl --shutdown`: stops WSL2 distributions and processes so they can restart cleanly. It does not delete files, but it interrupts running services.

**Then reopen Ubuntu and run:**

```bash
hermes desktop
```

- `hermes desktop`: launches the Hermes graphical interface again.

If the error persists, check the logs before reinstalling Hermes or importing another backup. Restarting WSL2 does not guarantee that every Desktop graphics issue will be fixed.

## If the provider or model needs to be configured again

If your previous provider or model is unavailable after restoring, launch the setup wizard from the **Ubuntu terminal**:

```bash
hermes setup model
```

- `hermes setup model`: lets you select the provider, model, and required authentication again.

For installations with separate profiles, run the setup wizard for the appropriate profile. **Example using the `aluno` profile:**

```bash
hermes -p aluno setup
```

Select the provider and model you previously used (for example, **MiniMax** and **MiniMax-M3**) and enter your API key only if the wizard requests it. Never expose API keys or tokens in screenshots.

When setup is complete, open a new conversation and test it with a simple message. If an older conversation shows `Resume failed — not_found`, Hermes could not resume that session; this does not necessarily mean the model itself has failed.

## Official references

- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/)
- [Official Hermes Agent repository](https://github.com/NousResearch/hermes-agent)
