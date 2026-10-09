"""Add a "Claude port" toggle button to your current Maya shelf.

Run once: open this file in the Script Editor (File > Load Script),
then press Execute All. Click the button to open the port (blue icon),
click again to close it (grey icon). Only localhost can connect.
"""
import base64
import os
import maya.cmds as cmds
import maya.mel as mel

ICONS = {
    "claude_port_on.png": "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",
    "claude_port_off.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAFBElEQVR4nMVXTWhcVRT+zn3vvvdmYhJtyW+bmUx+RLBaNbYKglAt1doiKnTTjbsuYqGVdl+6VyGkLYILV7qJCMUu7E9qU0tA2kaqKZR0kpIRoWmckEwyeX/3x8XkTf5mJtM24gcXHve+d+537jnnu+8AK3Do0CED/zHW7kErFwYGBuSRI0fiTs1znxDhHdJoVdCktab1pjYGEWmANEhPQeOa8BcGzp07txDtVSRw6tQpdvr0adV77MTblml9UxOveV4phTAMn8bZIjjnYIxhcTE/EXh+79mzX12MSFD0cPz4ybeYaV0xTdN5MDEuMplJuK77RJ6vhobjxHQikUSqo9NUSkkvcA+c7SuQIEDTiRMn40HIRmPxePvI7ZtibOyeyRgD0SbsD0BrDaUkOjq6xeu73jD9wJ9i2n+hr69vjgGk/ZA+rquvb38wkRZjY/dM27bBOYdpmpsyOOew7RjGx++b4+kxUV9X3yS1eRiAZgDACPuUUjqTmQRjrMj6SUep7wEN0zSRyUxSGIaamPEeADAA0ETNYRiS67r0dMdOiJI3cmRlGIgInuciCHxioMYigbLmiKoejBkQIsSrr/WgvT2FfH5hHYlSMCstBkFQPNKNYBgMi/k8ap+pxZ49e3HhwnmM/vkHHMcBEZW1U5KA1hqMMSQSSTCDAVVwIEYIPB+xeBxKSezffxANDQ34degaQATOeXUEIraccxw4+CFisRiUUhszWIJSCr7vAwB2734TDQ2NuDp4GfPz8yXLumIIDMOAYRhV6wERQQixVPcKQghs27YdtbV1mJ2dhWGsv2pKEiAiSClx9+4oLMuCjk6AUDYcRAQhBVpaWrFly1bEYjFMTU3hwk/nMTOTheM4EEJsTCAqFyEErg5eQpQ7lRIJQEHr83nse38/UqlOjIzcwpXLFxEEPhzHKRvGiiGwbadYZkKIpXJj0BpYG5WIoG3bGB6+gcuXfgbnHJxbFXOoIoHIY89z0dzSitraOkyMp8E5X3caWmtYloWR27eQy+XgODaI2IZlXJZA5FEQBEgkU+jp2YXx9P1ihq83rAEQZrJZMMNY8rowZ5rl/Sy7IqWA1sCLO15CZ2c3lFJwHAfb2xIFg+U8I1q1prTCTDZbfQ4QFWo5Hq/Bjh070djUhCAIAACNTc1obmkt6816W4QgCHB96CqklNURAApHH4vFsWXr1uKHy7rPUJU0rvimEkqWIecc09OPcH3oF/T07EJdfT2klJibnUU2+0/V8gwiSCkevwoiEvn8AoaHb+Dlna8glerAg4k07tz5HZZlV31JAYV/wnI6UjYJtS78QCglcfvmbwiCACa3YFl2QR0fg0CldzfUAcYYiHPcHf0DsVgcZrHENgdsaaNHnHPtOI4uJTBAQWo9d3G9BFaJZaV0YFm2llpNLxMQepAxRolEEkotZ/1aA6zEbVbt5pGctyWSmnNOWmNwiYAm12U/5HJzf6c6Os2Ojm7heR6ECKGUKg4pJaSUq+aqHUIIuK6LZLJddnV1G7nc3Ezoye8AULExOXr05F7LsS4yxlg6fT/8KzPJPM99Io/XwrYdtCWSuqur2yQi+K73UX//F+eXGpPlvrC39/MP7LjzdTxe0yZCgSDwN4WAZVng3EI+n38Y+v5nZ858+WOxNYteiiY+PXbs2XpmHWZg7wJo0RpP1R4RQWuih1rpoXm5+P23/f3TK5vTVfg/2vN/AUqY15JlImjYAAAAAElFTkSuQmCC",
}

# What the button runs on each click.
TOGGLE = '''import os
import maya.cmds as cmds
PORT = "localhost:7001"
icons = cmds.internalVar(userBitmapsDir=True)
if cmds.commandPort(PORT, q=True):
    cmds.commandPort(name=PORT, close=True)
    icon = os.path.join(icons, "claude_port_off.png")
    cmds.inViewMessage(amg="Claude port <hl>closed</hl>", pos="topCenter", fade=True)
else:
    cmds.commandPort(name=PORT, sourceType="python")
    icon = os.path.join(icons, "claude_port_on.png")
    cmds.inViewMessage(amg="Claude port <hl>open</hl> on 7001", pos="topCenter", fade=True)
for b in cmds.lsUI(type="shelfButton") or []:
    if cmds.shelfButton(b, q=True, label=True) == "Claude port":
        cmds.shelfButton(b, e=True, image=icon)
'''

# Save both icons into Maya's user icons folder.
icon_dir = cmds.internalVar(userBitmapsDir=True)
if not os.path.isdir(icon_dir):
    os.makedirs(icon_dir)
for name, data in ICONS.items():
    with open(os.path.join(icon_dir, name), "wb") as fh:
        fh.write(base64.b64decode(data))

# Start in the state the port is actually in.
is_open = cmds.commandPort("localhost:7001", q=True)
start_icon = os.path.join(icon_dir, "claude_port_on.png" if is_open else "claude_port_off.png")

# Add the button to whichever shelf tab is showing.
shelf_top = mel.eval("$tmp = $gShelfTopLevel")
shelf = cmds.tabLayout(shelf_top, q=True, selectTab=True)
cmds.shelfButton(
    parent=shelf,
    label="Claude port",
    annotation="Open / close the Claude port (localhost:7001)",
    image=start_icon,
    command=TOGGLE,
    sourceType="python",
)
cmds.inViewMessage(amg="Claude port button added to the <hl>%s</hl> shelf" % shelf, pos="topCenter", fade=True)
