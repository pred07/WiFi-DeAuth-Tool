import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ssh_utils.cli import cli

if __name__ == "__main__":
    cli()
