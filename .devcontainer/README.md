# Dev Container Configuration

This directory contains the development container configuration for the EIA Daily Dashboard project.

## What's Included

- **Python 3.12** environment
- **Virtual environment** automatically created in `.venv`
- **All dependencies** from `requirements.txt` pre-installed
- **VS Code extensions**:
  - Python
  - Pylance
  - Jupyter
  - Code Spell Checker
- **Port forwarding** for Streamlit (8501)
- **Automatic .env setup** from `.env.example`

## How It Works

When you open this repository in VS Code with the Dev Containers extension:

1. Docker builds a container based on the official Python 3.12 image
2. The `post-create.sh` script runs automatically to:
   - Create a virtual environment in `.venv`
   - Install all Python dependencies
   - Copy `.env.example` to `.env` (if it doesn't exist)
3. VS Code connects to the container and configures Python settings
4. Port 8501 is forwarded for the Streamlit dashboard

## Files

- `devcontainer.json` - Main configuration file for the dev container
- `post-create.sh` - Script that runs after container creation to set up the environment

## Usage

Simply open the repository in VS Code and click "Reopen in Container" when prompted. Everything else is automatic!
