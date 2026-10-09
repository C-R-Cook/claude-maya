# Talking to Maya

Maya has a commandPort open on `localhost:7001` in Python mode. Use `maya_send.py` in this folder; always start the command with `python maya_send.py` (one approval pattern).

```bash
python maya_send.py "import maya.cmds as cmds
sel = cmds.ls(selection=True, long=True)
sel"
python maya_send.py -f script.py
```

Options: `--host`, `--port` (default 7001), `--timeout` (default 10s).

## How it behaves

- Normal multi-line Python works. The reply is the value of the **last line** if it is an expression, otherwise `None`.
- `print()` output goes to Maya's Script Editor, not the reply. Return a value as the last line instead.
- Code runs in Maya's `__main__` namespace, so variables persist between calls (`x = 3` in one call, `x` in the next).
- Errors come back as the full traceback (file name `<maya_send>`), and the script exits 1. A connection failure also exits non-zero.
- A literal `\n` in a one-line argument is treated as a newline.

## Why the wrapper exists (don't send raw code to the port)

The raw commandPort returns only the value of a single expression, evaluates it outside `__main__`, and multi-statement code returns `None`. `maya_send.py` wraps your code into one expression that execs it in `__main__` and returns the last value or traceback. Don't change Maya's side; everything lives in the script.

## Conventions

- Prefer `cmds.ls(selection=True, long=True)` (long names) to avoid ambiguity between same-named objects.
- Wrap every scene change in one undo chunk (`cmds.undoInfo(openChunk=True)` / `closeChunk=True`), so one Ctrl+Z reverts it.
- Ask before saving files or editing nodes inside a reference.
