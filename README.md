# Automated SSH Manager
An advanced Python-based tool for managing SSH connections, executing commands, and generating reports. This project supports both Command-Line Interface (CLI) and Graphical User Interface (GUI) modes for maximum flexibility.

## Features
- Connect to remote servers via SSH using Fabric or Paramiko.
- Execute commands and display real-time output.
- Generate detailed PDF reports of command outputs.
- GUI for ease of use and CLI for automation and scripting.

## Requirements
- Python 3.8 or higher
- Libraries listed in `requirements.txt`

## Usage
- CLI TOOL: python main.py execute --host <ip>> --username <username> --password <password> --command "<command>"
    eg: python main.py execute --host 172.18.124.20 --username gr4y --password gray69 --command "ls"

- GUI TOOL: python gui.py

