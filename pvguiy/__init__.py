from .app import VGUI
from .core import Panel, Frame, Label, Scheme
from .widgets import (
    Button,
    CheckButton,
    TextEntry,
    Console
)
from .notifications import (
    Notification,
    NotificationManager
)
from .themes import (
    Theme,
    GREEN,
    ORANGE,
    BLACK,
    THEMES,
    get_theme
)

__version__ = "1.0.0"

__all__ = [
    "VGUI",
    "Panel",
    "Frame",
    "Label",
    "Scheme",
    "Button",
    "CheckButton",
    "TextEntry",
    "Console",
    "Notification",
    "NotificationManager",
    "Theme",
    "GREEN",
    "ORANGE",
    "BLACK",
    "THEMES",
    "get_theme"
]
