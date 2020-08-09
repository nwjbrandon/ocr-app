#!/usr/bin/env bash
cd src
zip -r main.zip * -x __pycache__/* __pycache__/
cd ..