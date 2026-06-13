"""Allow running orchestrator as: python -m orchestrator"""

import sys

from orchestrator.cli import main

if __name__ == "__main__":
    sys.exit(main())
