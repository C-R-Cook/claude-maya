# Add this to your userSetup.py so Maya opens the Claude port on startup.
#
# Windows:  Documents\maya\scripts\userSetup.py            (all Maya versions)
#      or   Documents\maya\<version>\scripts\userSetup.py  (one version only)
# Create the file if it doesn't exist.

import maya.cmds as cmds
import maya.utils


def _open_claude_port():
    port = "localhost:7001"  # localhost only: never open this to your network
    if not cmds.commandPort(port, q=True):
        cmds.commandPort(name=port, sourceType="python")


# Wait until Maya has finished starting up before opening the port.
maya.utils.executeDeferred(_open_claude_port)
