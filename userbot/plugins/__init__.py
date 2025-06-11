from importlib import import_module
from pathlib import Path

COMMANDS = {}

def add_command(name, func):
    """Register a command handler provided by plugins."""
    COMMANDS[name] = func


def load_plugins(directory: Path | None = None):
    """Load all plugin modules from *directory*."""
    if directory is None:
        directory = Path(__file__).parent
    for file in directory.glob('*.py'):
        if file.name == '__init__.py':
            continue
        module = import_module(f'{__name__}.{file.stem}')
        if hasattr(module, 'register'):
            module.register(add_command)
