#!/bin/bash

# Default to current directory if no argument is provided
Path="${1:-$(pwd)}"

# Function to activate a virtual environment
activate_venv() {
    local venv_path=$1
    if [ -f "$venv_path/bin/activate" ]; then
        echo "Activating virtual environment at: $venv_path"
        source "$venv_path/bin/activate"
    else
        echo "No virtual environment found at: $venv_path"
    fi
}

# Check if the directory contains a .venv folder
venv_path="$Path/.venv"

if [ -d "$venv_path" ]; then
    activate_venv "$venv_path"
else
    # Look for requirements.txt in the current directory
    requirements_path="$Path/requirements.txt"
    if [ -f "$requirements_path" ]; then
        dir_name=$(basename "$Path")
        new_venv_path="$Path/$dir_name"

        echo "Creating new virtual environment named '$dir_name'..."

        # Create the virtual environment
        python3 -m venv "$new_venv_path"
        echo "New virtual environment created at: $new_venv_path"

        # Activate the new environment and install dependencies
        source "$new_venv_path/bin/activate"
        pip install -r "$requirements_path"

        echo "Dependencies installed successfully!"
    else
        echo "Error: No .venv or requirements.txt found in the specified directory."
    fi
fi
