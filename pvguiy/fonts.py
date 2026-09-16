"""PVGUIY Font System - System font management."""

import platform
from typing import Dict, Tuple, Optional


class Font:
    """Represents a font with family, size, and style attributes."""
    
    def __init__(self, family: str = "MS Sans Serif", size: int = 8, 
                 bold: bool = False, italic: bool = False, underline: bool = False):
        self.family = family
        self.size = size
        self.bold = bold
        self.italic = italic
        self.underline = underline
    
    def to_tkinter(self) -> Tuple:
        """Convert to Tkinter font tuple."""
        weight = "bold" if self.bold else ""
        slant = "italic" if self.italic else ""
        
        parts = [self.family, self.size]
        if weight or slant:
            if weight and slant:
                parts.append(f"{weight} {slant}".strip())
            elif weight:
                parts.append(weight)
            elif slant:
                parts.append(slant)
        
        return tuple(parts)
    
    def __repr__(self) -> str:
        styles = []
        if self.bold:
            styles.append("bold")
        if self.italic:
            styles.append("italic")
        if self.underline:
            styles.append("underline")
        style_str = " ".join(styles) if styles else "normal"
        return f"Font('{self.family}', {self.size}, {style_str})"


class FontManager:
    """Manages fonts for the application based on platform."""
    
    DEFAULT_FONTS: Dict[str, Dict[str, Dict[str, Tuple[str, int]]]] = {
        "Windows": {
            "default": ("MS Sans Serif", 8),
            "bold": ("MS Sans Serif", 8),
            "small": ("MS Sans Serif", 7),
            "large": ("MS Sans Serif", 10),
            "mono": ("Courier New", 8),
            "titlebar": ("MS Sans Serif", 8),
            "button": ("MS Sans Serif", 8),
            "input": ("MS Sans Serif", 8),
            "console": ("Courier New", 8),
            "menu": ("MS Sans Serif", 8),
            "tooltip": ("MS Sans Serif", 7)
        },
        "Darwin": {
            "default": ("Lucida Grande", 11),
            "bold": ("Lucida Grande", 11),
            "small": ("Lucida Grande", 10),
            "large": ("Lucida Grande", 13),
            "mono": ("Monaco", 10),
            "titlebar": ("Lucida Grande", 11),
            "button": ("Lucida Grande", 11),
            "input": ("Lucida Grande", 11),
            "console": ("Monaco", 10),
            "menu": ("Lucida Grande", 11),
            "tooltip": ("Lucida Grande", 10)
        },
        "Linux": {
            "default": ("Sans", 9),
            "bold": ("Sans", 9),
            "small": ("Sans", 8),
            "large": ("Sans", 11),
            "mono": ("Monospace", 9),
            "titlebar": ("Sans", 9),
            "button": ("Sans", 9),
            "input": ("Sans", 9),
            "console": ("Monospace", 9),
            "menu": ("Sans", 9),
            "tooltip": ("Sans", 8)
        }
    }
    
    def __init__(self):
        self._system = platform.system()
        if self._system not in self.DEFAULT_FONTS:
            self._system = "Linux"
        
        self._fonts: Dict[str, Font] = {}
        self._setup_defaults()
    
    def _setup_defaults(self) -> None:
        """Set up default fonts for the current platform."""
        defaults = self.DEFAULT_FONTS[self._system]
        
        for name, (family, size) in defaults.items():
            bold = name == "bold" or name == "titlebar"
            self._fonts[name] = Font(family=family, size=size, bold=bold)
    
    def get(self, name: str) -> Font:
        """Get a font by name."""
        return self._fonts.get(name, self._fonts["default"])
    
    def set(self, name: str, font: Font) -> None:
        """Set a custom font."""
        self._fonts[name] = font
    
    def create(self, family: str, size: int, bold: bool = False, 
               italic: bool = False, underline: bool = False) -> Font:
        """Create a new font."""
        return Font(family, size, bold, italic, underline)
    
    def get_default_font(self) -> Font:
        """Get the default font."""
        return self._fonts["default"]
    
    def get_mono_font(self) -> Font:
        """Get the monospace font."""
        return self._fonts["mono"]
    
    def get_bold_font(self) -> Font:
        """Get the bold font."""
        return self._fonts["bold"]
    
    def get_small_font(self) -> Font:
        """Get the small font."""
        return self._fonts["small"]
    
    def to_dict(self) -> Dict[str, Dict]:
        """Convert fonts to dictionary."""
        return {
            name: {
                "family": font.family,
                "size": font.size,
                "bold": font.bold,
                "italic": font.italic,
                "underline": font.underline
            }
            for name, font in self._fonts.items()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Dict]) -> 'FontManager':
        """Create FontManager from dictionary."""
        manager = cls()
        for name, font_data in data.items():
            manager._fonts[name] = Font(
                family=font_data.get("family", "MS Sans Serif"),
                size=font_data.get("size", 8),
                bold=font_data.get("bold", False),
                italic=font_data.get("italic", False),
                underline=font_data.get("underline", False)
            )
        return manager


# Global font manager instance
_font_manager: Optional[FontManager] = None


def get_font_manager() -> FontManager:
    """Get the global font manager."""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager


def get_system_font() -> str:
    """Get the default system font family."""
    system = platform.system()
    if system == "Windows":
        return "MS Sans Serif"
    elif system == "Darwin":
        return "Lucida Grande"
    else:
        return "Sans"
