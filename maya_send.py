"""Send multi-line Python to a Maya commandPort and print the last line's value.

Usage:
    python maya_send.py "import maya.cmds as cmds\nsel = cmds.ls(sl=True)\nsel"
    python maya_send.py -f script.py

Code runs in Maya's __main__ namespace, so variables persist between calls.
"""
import argparse
import ast
import socket
import sys


# Runs inside Maya. Executes all but the last statement, evals the last if it
# is an expression, and returns the value or the full traceback as text.
_RUNNER = """
import ast, linecache, sys, traceback
linecache.cache['<maya_send>'] = (len(code), None, code.splitlines(True), '<maya_send>')
try:
    tree = ast.parse(code, '<maya_send>')
    last = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last = ast.Expression(tree.body.pop().value)
    exec(compile(tree, '<maya_send>', 'exec'), ns)
    r = eval(compile(last, '<maya_send>', 'eval'), ns) if last else None
except BaseException:
    t, v, tb = sys.exc_info()
    if isinstance(v, SyntaxError):
        r = ''.join(traceback.format_exception_only(t, v)).rstrip()
    else:
        r = ''.join(traceback.format_exception(t, v, tb.tb_next)).rstrip()  # hide runner frame
"""


def wrap(code):
    """Turn multi-line Python into the single expression the commandPort needs.

    The commandPort only returns the value of one expression, and evaluates it
    outside __main__. The code runs in __main__'s namespace so variables persist.
    The reply is the last line's value (None if it is a statement), or the full
    traceback if the code raised.
    """
    if "\n" not in code:
        code = code.replace("\\n", "\n")  # allow literal \n in one-line args
    return (
        "(lambda g: (exec(%r, g), g['r'])[1])"
        "({'code': %r, 'ns': __import__('__main__').__dict__})"
    ) % (_RUNNER, code)


def send(code, host="localhost", port=7001, timeout=10.0):
    """Send code to Maya's commandPort and return the reply string."""
    with socket.create_connection((host, port), timeout=timeout) as s:
        s.sendall(wrap(code).encode("utf-8") + b"\n")
        chunks = []
        try:
            while True:
                data = s.recv(4096)
                if not data:
                    break
                chunks.append(data)
                # Maya terminates each reply with a NUL byte.
                if data.endswith(b"\x00"):
                    break
        except socket.timeout:
            pass
    return b"".join(chunks).rstrip(b"\x00").decode("utf-8", errors="replace").rstrip()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("code", nargs="?", help="Python code to run")
    p.add_argument("-f", "--file", help="Read code from file")
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=7001)
    p.add_argument("--timeout", type=float, default=10.0)
    args = p.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            code = fh.read()
    elif args.code is not None:
        code = args.code
    else:
        p.error("provide code or -f FILE")

    try:
        reply = send(code, args.host, args.port, args.timeout)
        print(reply)
        # Runner output for exceptions: a traceback, or a bare SyntaxError report.
        if reply.startswith("Traceback (most recent call last):") or reply.startswith('  File "<maya_send>"'):
            sys.exit(1)
    except OSError as e:
        sys.exit("Could not reach Maya on %s:%d: %s" % (args.host, args.port, e))


if __name__ == "__main__":
    main()
