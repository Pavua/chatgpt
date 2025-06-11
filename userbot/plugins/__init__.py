from importlib import import_module, reload
from pathlib import Path
import sys

COMMANDS: dict[str, callable] = {}
_LOADED: dict[str, object] = {}


def add_command(name: str, func) -> None:
    """Register a command handler provided by plugins."""
    COMMANDS[name] = func


def load_plugins(directory: Path | None = None) -> None:
    """Load or reload all plugin modules from *directory*."""
    global _LOADED
    COMMANDS.clear()
    if directory is None:
        directory = Path(__file__).parent
    for file in directory.glob("*.py"):
        if file.name == "__init__.py":
            continue
        module_name = f"{__name__}.{file.stem}"
        if module_name in _LOADED:
            module = reload(sys.modules[module_name])
        else:
            module = import_module(module_name)
        _LOADED[module_name] = module
        if hasattr(module, "register"):
            module.register(add_command)


def plugin_names() -> list[str]:
    """Return a list of currently loaded plugin command names."""
    return sorted(COMMANDS)
