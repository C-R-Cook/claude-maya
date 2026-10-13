# Claude in Maya (no MCP)

Let Claude Code see and work in your Maya scene. No plugins, no MCP server, nothing to install in Maya. One line opens a port in Maya, and a small script lets Claude talk to it.

Companion repo for the video **Claude Code in Maya for VFX Artists**: <video link>

## What's in here

| File | What it does |
| --- | --- |
| `install_shelf_button.py` | Adds a "Claude port" button to your shelf, icon included. Run it once. |
| `maya_send.py` | The messenger. Claude runs it to send Python to Maya and read the reply. |
| `CLAUDE.md` | Tells Claude how to talk to Maya. Claude reads it automatically when a session starts in this folder. |
| `CLAUDE_top-level.md` | Only for starting Claude in a folder above this one. See "Using it from a parent folder". Ignore or delete it otherwise. |
| `icons/` | The shelf icons, blue for open and grey for closed (32 px and 64 px), if you'd rather set the button up yourself. |

## Setup

**1. Add the shelf button in Maya**

In the Script Editor, go to File > Load Script, pick `install_shelf_button.py`, and press Execute All. A button with the arrows icon appears on the shelf tab you're looking at.

Click it once and the port opens: the icon turns blue and "Claude port open" appears in the viewport. Click it again and the port closes: the icon goes grey.

If you quit Maya with the port open, the icon may still show blue next time you launch, even though the port is closed. One click puts it back in sync. Closing the port before you quit avoids it.

Prefer to set it up by hand? Copy both PNGs from `icons/` into your Maya icons folder (`Documents\maya\<version>\prefs\icons`, for example `Documents\maya\2027\prefs\icons`), then make a shelf button with `claude_port_off.png` as its icon, the label `Claude port`, and the toggle code from inside `install_shelf_button.py` as its Python command.

**2. Put the files in a folder**

Make a working folder, for example `D:\Work\claude-maya`, and put everything from this repo in it (green Code button > Download ZIP, then unzip).

Or let Claude do it: start a Code session in an empty folder and say:

> Download everything from https://github.com/C-R-Cook/claude-maya into this folder.

**3. Start Claude Code in that folder**

In the Claude desktop app, start a new Code session and choose your folder. **Make sure it runs locally on your machine.** A cloud session can't reach `localhost`.

Then ask:

> What do I have selected in Maya?

The first time, Claude asks permission to run `python maya_send.py`. Allow it.

You don't need to explain anything: Claude reads `CLAUDE.md` in the folder at the start of every session, so it already knows how to talk to Maya.

## How it works

Maya's commandPort only returns the value of a single expression, and it doesn't keep variables between calls. `maya_send.py` wraps your code so you can send normal multi-line Python:

- The value of the last line comes back as the reply.
- Variables persist between calls (they live in Maya's `__main__`).
- Errors come back as a full traceback, and the script exits with code 1.

```
python maya_send.py -f script.py
python maya_send.py "__import__('maya.cmds').cmds.ls(selection=True, long=True)"
```

Claude writes multi-line code to a temporary file and sends it with `-f`, so every command stays on one line. A command with line breaks in it doesn't match the permission rule, and you'd get asked every time. `CLAUDE.md` tells Claude to do this, so you don't have to.

## Using it from a parent folder

If you start Claude in a folder above this one (say, the folder that holds all your Maya projects, with this repo cloned inside it as `claude-maya`), it needs two small changes. Claude only reads the `CLAUDE.md` in the folder you start in, and the commands need the subfolder in their path.

**1. Copy `CLAUDE_top-level.md` up to the parent folder and rename it `CLAUDE.md`.** Copy it, don't move it, so the repo stays intact for `git pull`. Already have a `CLAUDE.md` up there? Paste its contents onto the end of yours instead.

It pulls in this repo's instructions (the `@claude-maya/CLAUDE.md` line) and tells Claude to use the `claude-maya/` path. Inside the repo it does nothing: Claude only reads files named exactly `CLAUDE.md`.

**2. Allow the new command.** In a session in the parent folder, ask Claude:

> Add a permission rule so `python claude-maya/maya_send.py` runs with any arguments without asking.

Keep the files inside `claude-maya` rather than moving them up a level, so `git pull` still updates them.

## Safety

- The port listens on `localhost` only. Don't open it to your network.
- Ask Claude to wrap scene changes in one undo chunk, so one Ctrl+Z reverts them.
- Close the port when you're done: click the shelf button again.
- Claude Code runs in the cloud, so scene information like node names and weights leaves your machine. Check your studio's policy before using it on show assets.

## Requirements

- Maya 2022 or newer (Python 3). Older versions won't work.
- The shelf button installs into whichever Maya version you run it in. Using more than one version? Run the installer once in each.
- Claude Code running locally on the same machine as Maya.

Tested with Maya 2027 on Windows.
