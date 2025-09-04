#!/usr/bin/env bash

SRCDIR=$(dirname "$0")
DSTDIR=$HOME/.config/roadrunner


mkdir -p $HOME/.config/roadrunner
cp $SRCDIR/config.ini $DSTDIR
cp $SRCDIR/flake.nix $DSTDIR
