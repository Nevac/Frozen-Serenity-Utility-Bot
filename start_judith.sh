#!/bin/bash

# Check if already running
dupe_script=$(ps -ef | grep -e "app.py" -e "start_judith.sh" | grep -v grep | wc -l)
if [ "${dupe_script}" -gt 3 ]; then
  echo -e "Judith already running"
  exit 0
fi

function install_venv() {
  [ $# -lt 1 ] && {
    echo "install_venv(): Not enough arguments supplied"
    return
  }
  dest=$1
  # Deactivate current venv
  deactivate 2>/dev/null
  # Create venv if not exist
  [[ -d "${dest}/venv" ]] && {
    # Source venv
    source "${dest}/venv/bin/activate"
    echo "Sourced venv ${dest}/venv"
  } || {
    echo "Installing venv ${dest}/venv"
    # Update dependencies
    pip install --upgrade pip
    python3 -m pip install --user virtualenv
    echo "Downloaded dependencies"
    # Install venv
    python3 -m venv "${dest}/venv"
    echo "Installed venv"
    # Install requirements
    source "${dest}/venv/bin/activate"
    echo "Sourced venv"
    pip install -r "${dest}/requirements.txt"
    echo "Finished install venv"
    pip freeze
  }
  echo ""
}

echo "Start Judith..."
echo ""

start_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# Install and source venv
install_venv "${start_dir}"
# Start bot
python3 app.py

echo ""
echo "Stopped Judith"
