"""Validate that publish-via-browseros.py generates syntactically valid code."""
import ast
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(__file__).resolve().parent / "_gen_check.txt"

for only in (1, 11):
    r = subprocess.run(
        [sys.executable, str(HERE / "publish-via-browseros.py"),
         "--only", str(only), "--dry-run"],
        capture_output=True, text=True, timeout=90,
    )
    src = r.stdout
    lines = src.splitlines()
    start = 0
    for idx, l in enumerate(lines):
        if l.startswith("# ===") and idx > 2:
            start = idx + 1
            break
    code = "\n".join(lines[start:])
    try:
        ast.parse(code)
        print(f"product {only}: generated code syntax OK ({len(code)} chars)")
    except SyntaxError as e:
        print(f"product {only}: SYNTAX ERROR line {e.lineno}: {e.msg}")
        cl = code.splitlines()
        if e.lineno and e.lineno - 1 < len(cl):
            print("  >> " + cl[e.lineno - 1][:130])
        sys.exit(1)

    # Also: every STEP marker should be present in the generated code
    steps = [f"STEP {n}" for n in range(0, 12)]
    missing = [s for s in steps if s not in code]
    if missing:
        print(f"product {only}: MISSING STEP MARKERS: {missing}")
        sys.exit(1)
    # braces balanced in embedded JS (rough check: no format leftovers)
    leftovers = [l for l in code.splitlines() if "{js_str(" in l or "json.dumps(SLUG" in l]
    if leftovers:
        print(f"product {only}: UNEXPANDED TEMPLATE in output: {leftovers[:2]}")
        sys.exit(1)

print("ALL GENERATED CODE VALID")
