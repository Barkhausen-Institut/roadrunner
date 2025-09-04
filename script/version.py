#!/bin/env python3
import argparse
from pathlib import Path
import re
import subprocess
import sys

#load version
VERSION_FILE = Path(__file__).parent / "../roadrunner/version"
VERSION_GITREX = r'v(\d+)\.(\d+)\.(\d+)(-[\w-]+)?'

parser = argparse.ArgumentParser()
parser.add_argument('command', choices=['bump', 'tag', 'read'])
parser.add_argument('--minor', action='store_true')
parser.add_argument('--major', action='store_true')
parser.add_argument('--force', action='store_true')
args = parser.parse_args()

major, minor, patch = None, None, None

#read version from file
lines = []
insertAt = None
with(open(VERSION_FILE, 'r')) as fh:
    raw = fh.read()
try:
    major, minor, patch = (int(x) for x in raw.strip().split('.'))
except:
    raise Exception(f"could not read version from:{raw} - please fix roadrunner/version")
print(f"current version:{major} {minor} {patch}")
#read version from git
raw = subprocess.check_output(["git", "describe", "--tags"])
out = raw.decode(sys.stdout.encoding).strip()
m = re.match(VERSION_GITREX, out)
if m is None:
    print(f"could not read git version from:{out}")
    gitMajor, gitMinor, gitPatch = None, None, None
else:
    gitMajor = int(m.group(1))
    gitMinor = int(m.group(2))
    gitPatch = int(m.group(3))
    print(f"git version:{gitMajor} {gitMinor} {gitPatch}")

if args.command == 'bump':
    if args.major:
        print("increasing major")
        major += 1
        minor = 0
        patch = 0
    elif args.minor:
        print("increasing minor")
        minor += 1
        patch = 0
    else:
        print("increasing patch")
        patch += 1
    print(f"new version:{major} {minor} {patch}")
    with open(VERSION_FILE, 'w') as fh:
        print(f"{major}.{minor}.{patch}", file=fh)
elif args.command == 'tag':
    print("check repository")
    result = subprocess.run(["git", "diff", "--exit-code", VERSION_FILE])
    if result.returncode != 0:
        if args.force:
            print("version file is not clean - but --force is set")
        else:
            print("version file is not clean - use --force to override")
            exit(1)
    tagname = f"v{major}.{minor}.{patch}"
    print(f"creating tag:{tagname}")
    subprocess.run([
        "git", "tag", "-a", tagname, "-m", f"version {tagname}"
    ])
elif args.command == 'read':
    if gitMajor is None:
        print("no git version available - cannot compare")
        exit(1)
    if gitMajor != major or gitMinor != minor or gitPatch != patch:
        print("NOT SYNCED ")
    else:
        print("SYNCED  ")

else:
    print("unknown command")