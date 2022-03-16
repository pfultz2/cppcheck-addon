#!/bin/bash
set -e
rm -f build/*
cppcheck -j $(nproc) --error-exitcode=1 --addon=addon.py --inline-suppr --cppcheck-build-dir=build/ test/*.cpp
echo "Success"
