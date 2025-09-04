import sys

if len(sys.argv) > 1:
    object = sys.argv[1]
else:
    object = "Welt"

with open("message", "w") as fh:
    print(f"Hallo {object}!", file=fh)