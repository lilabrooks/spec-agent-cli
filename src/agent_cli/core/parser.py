import argparse
import sys
from typing import NoReturn


class FriendlyArgumentParser(argparse.ArgumentParser):
    """Argument parser with concise, actionable error output."""

    def error(self, message: str) -> NoReturn:
        self.print_usage(sys.stderr)
        self.exit(2, f"Error: {message}\nTry '{self.prog} --help' for available options.\n")
