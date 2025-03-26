#!/bin/bash

# a test bash script to see the basic functionality with cron

#obtaining PATH variable to the parent folder
SCRIPT=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")
PROJECT_PATH="$(dirname "$SCRIPT_PATH")"
#echo "$SCRIPT_PATH"
#echo "$PROJECT_PATH"

# executing test python script
# this script goes to the project directory, activates venv, and runs the .py script
cd "$PROJECT_PATH" || { echo "Directory not found"; exit 1; }
. "$PROJECT_PATH"/venv/bin/activate
python3.11 -m src.testing.test_script


