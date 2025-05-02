#!/bin/bash

# bash script which runs the AR(p) model forecasting
# is run by a * * * * * (=every minute) cron job

#obtaining PATH variable to the parent folder
SCRIPT=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")
PROJECT_PATH="$(dirname "$SCRIPT_PATH")"
#echo "$SCRIPT_PATH"
#echo "$PROJECT_PATH"

# executing test python script
# this script goes to the project directory, activates venv, and runs the .py script
cd "$PROJECT_PATH" || { echo "Directory not found"; exit 1; }
. "$PROJECT_PATH"/venv/bin/activate # works with ".", does not work with "source"
python3.11 -m apps.statistics.automatic_ar_model_forecasting