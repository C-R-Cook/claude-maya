# Claude in Maya (no MCP)

Let Claude Code see and work in your Maya scene. No plugins, no MCP server, nothing to install in Maya. One line opens a port in Maya, and a small script lets Claude talk to it.

Companion repo for the video **Claude Code in Maya for VFX Artists**: <video link>

## What's in here

|File|What it does|
|-|-|
|`install\_shelf\_button.py`|Adds a "Claude port" button to your shelf, icon included. Run it once.|
|`maya\_send.py`|The messenger. Claude runs it to send Python to Maya and read the reply.|
|`CLAUDE.md.example`|Tells Claude how to talk to Maya. Optional: Claude can write its own.|
|`icons/`|The shelf icons, blue for open and grey for closed (32 px and 64 px), if you'd rather set the button up yourself.|
|`userSetup\_snippet.py`|Advanced: opens the port automatically when Maya starts.|

## Setup

**1. Add the shelf button in Maya**

In the Script Editor, go to File > Load Script, pick `install\_shelf\_button.py`, and press Execute All. A button with the arrows icon appears on the shelf tab you're looking at.

Click it once and the port opens: the icon turns blue and "Claude port open" appears in the viewport. Click it again and the port closes: the icon goes grey.

If you quit Maya with the port open, the icon may still show blue next time you launch, even though the port is closed. One click puts it back in sync. Closing the port before you quit avoids it.

Prefer to set it up by hand? Copy both PNGs from `icons/` into your Maya icons folder (`Documents\\maya\\2027\\prefs\\icons`), then make a shelf button with `claude\_port\_off.png` as its icon, the label `Claude port`, and the toggle code from inside `install\_shelf\_button.py` as its Python command.

**2. Put the files in a folder**

Make a working folder, for example `D:\\Work\\claude-maya`, and put `maya\_send.py` in it.

Or let Claude do it: start a Code session in an empty folder and say:

> Set up the Maya bridge from > https://github.com/C-R-Cook/claude-maya in this folder.

**3. Start Claude Code in that folder**

In the Claude desktop app, start a new Code session and choose your folder. **Make sure it runs locally on your machine.** A cloud session can't reach `localhost`.

Then ask:

> What do I have selected in Maya?

The first time, Claude asks permission to run `python maya\_send.py`. Allow it.

**4. (Optional) Let Claude remember the setup**

> Write a CLAUDE.md in this folder so next time you know how to talk to Maya.

Or rename `CLAUDE.md.example` to `CLAUDE.md`.

## How it works

Maya's commandPort only returns the value of a single expression, and it doesn't keep variables between calls. `maya\_send.py` wraps your code so you can send normal multi-line Python:

* The value of the last line comes back as the reply.
* Variables persist between calls (they live in Maya's `\_\_main\_\_`).
* Errors come back as a full traceback, and the script exits with code 1.

```
python maya\_send.py "import maya.cmds as cmds
sel = cmds.ls(selection=True, long=True)
sel"

python maya\_send.py -f script.py
```

## Advanced: open the port automatically

If you want the port open every time Maya starts, add `userSetup\_snippet.py` to the end of your `userSetup.py`:

* Windows: `Documents\\maya\\scripts\\userSetup.py` (create it if it doesn't exist)

If it doesn't open on startup, other tools may be in the way. Plugins such as MASH and Quixel ship their own `userSetup.py`, and if one of them errors at startup, yours can get skipped. Check the top of the Script Editor history after a fresh launch, or just use the shelf button.

## Safety

* The port listens on `localhost` only. Don't open it to your network.
* Ask Claude to wrap scene changes in one undo chunk, so one Ctrl+Z reverts them.
* Close the port when you're done: click the shelf button again.
* Claude Code runs in the cloud, so scene information like node names and weights leaves your machine. Check your studio's policy before using it on show assets.

Tested with Maya 2027 on Windows.

