"""PVGUIY Scheme System - Visual configuration layer for colors, fonts, and borders."""

from typing import Dict, Any, Optional, Tuple
from pvguiy.theme import Theme


class Scheme:
    """
    Scheme class that acts as a centralized visual configuration layer.
    Provides access to colors, fonts, and borders for widgets.
    """
    
    def __init__(self, theme: Theme):
        self._theme = theme
        self._colors: Dict[str, str] = {}
        self._fonts: Dict[str, Tuple[str, int, str]] = {}
        self._borders: Dict[str, Dict[str, Any]] = {}
        self._setup_defaults()
    
    def _setup_defaults(self) -> None:
        """Set up default colors, fonts, and borders from theme."""
        # Colors from theme
        self._colors = {
            "Background": self._theme.background,
            "BackgroundDark": self._theme.background_dark,
            "BackgroundLight": self._theme.background_light,
            "PanelBg": self._theme.panel,
            "PanelBgDark": self._theme.panel_dark,
            "PanelBgLight": self._theme.panel_light,
            "Text": self._theme.text,
            "TextDark": self._theme.text_dark,
            "TextDisabled": self._theme.text_disabled,
            "BorderLight": self._theme.border_light,
            "BorderDark": self._theme.border_dark,
            "BorderPressed": self._theme.border_pressed,
            "BorderFocus": self._theme.border_focus,
            "Button": self._theme.button,
            "ButtonHover": self._theme.button_hover,
            "ButtonPressed": self._theme.button_pressed,
            "ButtonDisabled": self._theme.button_disabled,
            "Input": self._theme.input,
            "InputFocus": self._theme.input_focus,
            "Highlight": self._theme.highlight,
            "Selection": self._theme.selection,
            "Accent": self._theme.accent,
            "Success": self._theme.success,
            "Warning": self._theme.warning,
            "Error": self._theme.error,
            "Console": self._theme.console,
            "TitleBar": self._theme.titlebar,
            "TitleBarText": self._theme.titlebar_text,
            "ScrollBar": self._theme.scrollbar,
            "ToolTip": self._theme.tooltip,
            "Notification": self._theme.notification,
            "White": self._theme.white,
            "Black": self._theme.black
        }
        
        # Default fonts (system-dependent)
        import platform
        system = platform.system()
        if system == "Windows":
            default_font = ("MS Sans Serif", 8, "")
            bold_font = ("MS Sans Serif", 8, "bold")
            small_font = ("MS Sans Serif", 7, "")
            mono_font = ("Courier New", 8, "")
        elif system == "Darwin":
            default_font = ("Lucida Grande", 11, "")
            bold_font = ("Lucida Grande", 11, "bold")
            small_font = ("Lucida Grande", 10, "")
            mono_font = ("Monaco", 10, "")
        else:  # Linux
            default_font = ("Sans", 9, "")
            bold_font = ("Sans", 9, "bold")
            small_font = ("Sans", 8, "")
            mono_font = ("Monospace", 9, "")
        
        self._fonts = {
            "Default": default_font,
            "Bold": bold_font,
            "Small": small_font,
            "Mono": mono_font,
            "TitleBar": bold_font,
            "Button": default_font,
            "Input": default_font,
            "Console": mono_font,
            "Menu": default_font,
            "Tooltip": small_font
        }
        
        # Default borders
        self._borders = {
            "Raised": {
                "light": self._theme.border_light,
                "dark": self._theme.border_dark
            },
            "Sunken": {
                "light": self._theme.border_light,
                "dark": self._theme.black
            },
            "Flat": {
                "light": self._theme.border_dark,
                "dark": self._theme.border_dark
            },
            "Focus": {
                "light": self._theme.border_focus,
                "dark": self._theme.border_focus
            },
            "Disabled": {
                "light": self._theme.border_dark,
                "dark": self._theme.border_dark
            }
        }
    
    @property
    def theme(self) -> Theme:
        """Get the current theme."""
        return self._theme
    
    def get_color(self, name: str) -> str:
        """Get a color by name."""
        return self._colors.get(name, self._theme.panel)
    
    def set_color(self, name: str, value: str) -> None:
        """Set a color by name."""
        self._colors[name] = value
    
    def get_font(self, name: str) -> Tuple[str, int, str]:
        """Get a font by name. Returns (family, size, weight)."""
        return self._fonts.get(name, self._fonts["Default"])
    
    def set_font(self, name: str, family: str, size: int, weight: str = "") -> None:
        """Set a font by name."""
        self._fonts[name] = (family, size, weight)
    
    def get_border(self, name: str) -> Dict[str, str]:
        """Get border colors by name."""
        return self._borders.get(name, self._borders["Raised"])
    
    def set_border(self, name: str, light: str, dark: str) -> None:
        """Set border colors by name."""
        self._borders[name] = {"light": light, "dark": dark}
    
    # Convenience properties for backward compatibility
    @property
    def background(self) -> str:
        return self._theme.background
    
    @property
    def background_dark(self) -> str:
        return self._theme.background_dark
    
    @property
    def background_light(self) -> str:
        return self._theme.background_light
    
    @property
    def panel(self) -> str:
        return self._theme.panel
    
    @property
    def panel_dark(self) -> str:
        return self._theme.panel_dark
    
    @property
    def panel_light(self) -> str:
        return self._theme.panel_light
    
    @property
    def text(self) -> str:
        return self._theme.text
    
    @property
    def text_dark(self) -> str:
        return self._theme.text_dark
    
    @property
    def text_disabled(self) -> str:
        return self._theme.text_disabled
    
    @property
    def border_light(self) -> str:
        return self._theme.border_light
    
    @property
    def border_dark(self) -> str:
        return self._theme.border_dark
    
    @property
    def button(self) -> str:
        return self._theme.button
    
    @property
    def button_hover(self) -> str:
        return self._theme.button_hover
    
    @property
    def button_pressed(self) -> str:
        return self._theme.button_pressed
    
    @property
    def input(self) -> str:
        return self._theme.input
    
    @property
    def highlight(self) -> str:
        return self._theme.highlight
    
    @property
    def accent(self) -> str:
        return self._theme.accent
    
    @property
    def success(self) -> str:
        return self._theme.success
    
    @property
    def warning(self) -> str:
        return self._theme.warning
    
    @property
    def error(self) -> str:
        return self._theme.error
    
    @property
    def console(self) -> str:
        return self._theme.console
    
    @property
    def white(self) -> str:
        return self._theme.white
    
    @property
    def black(self) -> str:
        return self._theme.black
    
    def update_theme(self, theme: Theme) -> None:
        """Update the scheme with a new theme."""
        self._theme = theme
        self._setup_defaults()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scheme to dictionary."""
        return {
            "theme": self._theme.name,
            "colors": dict(self._colors),
            "fonts": {k: list(v) for k, v in self._fonts.items()},
            "borders": dict(self._borders)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], theme_manager=None) -> 'Scheme':
        """Create scheme from dictionary."""
        from pvguiy.theme import get_theme
        theme_name = data.get("theme", "green")
        theme = get_theme(theme_name)
        scheme = cls(theme)
        
        if "colors" in data:
            scheme._colors.update(data["colors"])
        if "fonts" in data:
            for k, v in data["fonts"].items():
                scheme._fonts[k] = tuple(v)
        if "borders" in data:
            scheme._borders.update(data["borders"])
        
        return scheme
