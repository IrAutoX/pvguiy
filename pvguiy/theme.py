"""PVGUIY Theme System - Define and manage visual themes."""

from typing import Dict, Any, Optional
from pvguiy.exceptions import ThemeError


class Theme:
    """Represents a complete visual theme with all color definitions."""
    
    def __init__(
        self,
        name: str,
        background: str = "#4B5A45",
        background_dark: str = "#30392D",
        background_light: str = "#68785F",
        panel: str = "#596952",
        panel_dark: str = "#3B4637",
        panel_light: str = "#6B7A62",
        text: str = "#E2E5D8",
        text_dark: str = "#11150F",
        text_disabled: str = "#777777",
        border_light: str = "#8A9980",
        border_dark: str = "#252B22",
        border_pressed: str = "#1a1f18",
        border_focus: str = "#9BAD78",
        button: str = "#596952",
        button_hover: str = "#6B7A62",
        button_pressed: str = "#3B4637",
        button_disabled: str = "#444444",
        input: str = "#20261E",
        input_focus: str = "#2a3128",
        highlight: str = "#82966F",
        selection: str = "#4a5a45",
        accent: str = "#9BAD78",
        success: str = "#75995B",
        warning: str = "#B29A56",
        error: str = "#B94A48",
        console: str = "#10140F",
        titlebar: str = "#30392D",
        titlebar_text: str = "#E7E9DD",
        scrollbar: str = "#3B4637",
        tooltip: str = "#1a1f18",
        notification: str = "#596952",
        white: str = "#E7E9DD",
        black: str = "#11140F"
    ):
        self.name = name
        self.background = background
        self.background_dark = background_dark
        self.background_light = background_light
        self.panel = panel
        self.panel_dark = panel_dark
        self.panel_light = panel_light
        self.text = text
        self.text_dark = text_dark
        self.text_disabled = text_disabled
        self.border_light = border_light
        self.border_dark = border_dark
        self.border_pressed = border_pressed
        self.border_focus = border_focus
        self.button = button
        self.button_hover = button_hover
        self.button_pressed = button_pressed
        self.button_disabled = button_disabled
        self.input = input
        self.input_focus = input_focus
        self.highlight = highlight
        self.selection = selection
        self.accent = accent
        self.success = success
        self.warning = warning
        self.error = error
        self.console = console
        self.titlebar = titlebar
        self.titlebar_text = titlebar_text
        self.scrollbar = scrollbar
        self.tooltip = tooltip
        self.notification = notification
        self.white = white
        self.black = black
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert theme to dictionary."""
        return {
            "name": self.name,
            "background": self.background,
            "background_dark": self.background_dark,
            "background_light": self.background_light,
            "panel": self.panel,
            "panel_dark": self.panel_dark,
            "panel_light": self.panel_light,
            "text": self.text,
            "text_dark": self.text_dark,
            "text_disabled": self.text_disabled,
            "border_light": self.border_light,
            "border_dark": self.border_dark,
            "border_pressed": self.border_pressed,
            "border_focus": self.border_focus,
            "button": self.button,
            "button_hover": self.button_hover,
            "button_pressed": self.button_pressed,
            "button_disabled": self.button_disabled,
            "input": self.input,
            "input_focus": self.input_focus,
            "highlight": self.highlight,
            "selection": self.selection,
            "accent": self.accent,
            "success": self.success,
            "warning": self.warning,
            "error": self.error,
            "console": self.console,
            "titlebar": self.titlebar,
            "titlebar_text": self.titlebar_text,
            "scrollbar": self.scrollbar,
            "tooltip": self.tooltip,
            "notification": self.notification,
            "white": self.white,
            "black": self.black
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Theme':
        """Create theme from dictionary."""
        return cls(**data)


# Built-in GREEN theme (classic Half-Life style)
GREEN = Theme(
    name="green",
    background="#4B5A45",
    background_dark="#30392D",
    background_light="#68785F",
    panel="#596952",
    panel_dark="#3B4637",
    panel_light="#6B7A62",
    text="#E2E5D8",
    text_dark="#11150F",
    text_disabled="#777777",
    border_light="#8A9980",
    border_dark="#252B22",
    border_pressed="#1a1f18",
    border_focus="#9BAD78",
    button="#596952",
    button_hover="#6B7A62",
    button_pressed="#3B4637",
    button_disabled="#444444",
    input="#20261E",
    input_focus="#2a3128",
    highlight="#82966F",
    selection="#4a5a45",
    accent="#9BAD78",
    success="#75995B",
    warning="#B29A56",
    error="#B94A48",
    console="#10140F",
    titlebar="#30392D",
    titlebar_text="#E7E9DD",
    scrollbar="#3B4637",
    tooltip="#1a1f18",
    notification="#596952",
    white="#E7E9DD",
    black="#11140F"
)

# ORANGE theme (warm brown/orange tones)
ORANGE = Theme(
    name="orange",
    background="#5A4936",
    background_dark="#382C21",
    background_light="#786047",
    panel="#66523E",
    panel_dark="#443526",
    panel_light="#7A624A",
    text="#EEE2D2",
    text_dark="#17110C",
    text_disabled="#777777",
    border_light="#9A816A",
    border_dark="#30251C",
    border_pressed="#241b15",
    border_focus="#B8956B",
    button="#66523E",
    button_hover="#7A624A",
    button_pressed="#443526",
    button_disabled="#444444",
    input="#241B14",
    input_focus="#2e221a",
    highlight="#A8784D",
    selection="#5a4535",
    accent="#D38B45",
    success="#789B5E",
    warning="#B79855",
    error="#BE554C",
    console="#120E0A",
    titlebar="#382C21",
    titlebar_text="#F1E6D8",
    scrollbar="#443526",
    tooltip="#1e1610",
    notification="#66523E",
    white="#F1E6D8",
    black="#15100C"
)

# BLACK theme (dark gray/black tones)
BLACK = Theme(
    name="black",
    background="#303030",
    background_dark="#191919",
    background_light="#444444",
    panel="#383838",
    panel_dark="#242424",
    panel_light="#4a4a4a",
    text="#E5E5E5",
    text_dark="#090909",
    text_disabled="#777777",
    border_light="#707070",
    border_dark="#121212",
    border_pressed="#0a0a0a",
    border_focus="#909090",
    button="#383838",
    button_hover="#4a4a4a",
    button_pressed="#242424",
    button_disabled="#444444",
    input="#171717",
    input_focus="#1f1f1f",
    highlight="#555555",
    selection="#3a3a3a",
    accent="#9A9A9A",
    success="#72975D",
    warning="#A68D51",
    error="#B84C4C",
    console="#080808",
    titlebar="#191919",
    titlebar_text="#F2F2F2",
    scrollbar="#242424",
    tooltip="#121212",
    notification="#383838",
    white="#F2F2F2",
    black="#050505"
)

THEMES: Dict[str, Theme] = {
    "green": GREEN,
    "orange": ORANGE,
    "black": BLACK
}


def get_theme(name: str) -> Theme:
    """Get a theme by name (case-insensitive)."""
    name = name.lower()
    if name not in THEMES:
        raise ThemeError(f"Unknown theme: {name}. Available: {list(THEMES.keys())}")
    return THEMES[name]


def register_theme(name: str, theme: Theme) -> None:
    """Register a custom theme."""
    THEMES[name.lower()] = theme


def list_themes() -> list:
    """List all available theme names."""
    return list(THEMES.keys())


class ThemeManager:
    """Manages themes for the application."""
    
    def __init__(self, default_theme: str = "green"):
        self._themes: Dict[str, Theme] = dict(THEMES)
        self._current_theme: Theme = self._themes.get(default_theme.lower(), GREEN)
        self._listeners: list = []
    
    @property
    def current_theme(self) -> Theme:
        """Get the current theme."""
        return self._current_theme
    
    def set_theme(self, name: str) -> None:
        """Set the current theme by name."""
        theme = get_theme(name)
        self._current_theme = theme
        self._notify_listeners()
    
    def register_theme(self, name: str, theme: Theme) -> None:
        """Register a custom theme."""
        self._themes[name.lower()] = theme
    
    def add_listener(self, callback) -> None:
        """Add a theme change listener."""
        self._listeners.append(callback)
    
    def remove_listener(self, callback) -> None:
        """Remove a theme change listener."""
        if callback in self._listeners:
            self._listeners.remove(callback)
    
    def _notify_listeners(self) -> None:
        """Notify all listeners of theme change."""
        for callback in self._listeners:
            try:
                callback(self._current_theme)
            except Exception:
                pass
    
    def get_theme(self, name: str) -> Theme:
        """Get a theme by name."""
        return get_theme(name)
    
    def list_themes(self) -> list:
        """List available themes."""
        return list(self._themes.keys())
