"""PVGUIY Icons System - Simple icon rendering."""

import tkinter as tk
from typing import Optional, Dict, Tuple


class Icon:
    """Represents a simple icon that can be drawn on canvas."""
    
    def __init__(self, name: str, width: int = 16, height: int = 16):
        self.name = name
        self.width = width
        self.height = height
    
    def draw(self, canvas: tk.Canvas, x: int, y: int, color: str) -> None:
        raise NotImplementedError


class UnicodeIcon(Icon):
    """Icon using Unicode characters."""
    
    def __init__(self, name: str, char: str, size: int = 12):
        super().__init__(name, size, size)
        self.char = char
        self.size = size
    
    def draw(self, canvas: tk.Canvas, x: int, y: int, color: str) -> None:
        canvas.create_text(x + self.width // 2, y + self.height // 2,
                          text=self.char, fill=color,
                          font=("MS Sans Serif", self.size))


class GeometricIcon(Icon):
    """Icon using geometric shapes."""
    
    def __init__(self, name: str, shape: str, width: int = 16, height: int = 16):
        super().__init__(name, width, height)
        self.shape = shape
    
    def draw(self, canvas: tk.Canvas, x: int, y: int, color: str) -> None:
        w, h = self.width, self.height
        
        if self.shape == "check":
            # Checkmark
            canvas.create_line(x + 4, y + h // 2, x + w // 3, y + h - 4, fill=color, width=2)
            canvas.create_line(x + w // 3, y + h - 4, x + w - 4, y + 4, fill=color, width=2)
        
        elif self.shape == "cross":
            # X mark
            canvas.create_line(x + 4, y + 4, x + w - 4, y + h - 4, fill=color, width=2)
            canvas.create_line(x + w - 4, y + 4, x + 4, y + h - 4, fill=color, width=2)
        
        elif self.shape == "arrow_down":
            # Down arrow
            cx, cy = x + w // 2, y + h // 2
            canvas.create_line(x + 4, y + h // 3, cx, y + h - 4, fill=color, width=2)
            canvas.create_line(cx, y + h - 4, x + w - 4, y + h // 3, fill=color, width=2)
        
        elif self.shape == "arrow_up":
            # Up arrow
            cx, cy = x + w // 2, y + h // 2
            canvas.create_line(x + 4, y + h - 4, cx, y + 4, fill=color, width=2)
            canvas.create_line(cx, y + 4, x + w - 4, y + h - 4, fill=color, width=2)
        
        elif self.shape == "folder":
            # Folder icon
            canvas.create_rectangle(x + 2, y + 4, x + w - 2, y + h - 2, outline=color, width=1)
            canvas.create_line(x + 2, y + 4, x + w // 3, y + 4, fill=color, width=2)
            canvas.create_line(x + 2, y + 4, x + 2, y + 8, fill=color, width=2)
        
        elif self.shape == "file":
            # File icon
            canvas.create_rectangle(x + 4, y + 2, x + w - 4, y + h - 2, outline=color, width=1)
            canvas.create_line(x + w - 4, y + 2, x + w - 4, y + 6, fill=color, width=1)
            canvas.create_line(x + w - 4, y + 6, x + w - 8, y + 6, fill=color, width=1)
        
        elif self.shape == "gear":
            # Simple gear/cog
            cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 2
            canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, width=1)
            canvas.create_oval(cx - r // 3, cy - r // 3, cx + r // 3, cy + r // 3, outline=color, width=1)
        
        elif self.shape == "info":
            # Info icon (i in circle)
            cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 1
            canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, width=1)
            canvas.create_text(cx, cy + 2, text="i", fill=color, font=("MS Sans Serif", 8))
        
        elif self.shape == "warning":
            # Warning icon (! in triangle)
            pts = [x + w // 2, y + 2, x + w - 2, y + h - 2, x + 2, y + h - 2]
            canvas.create_polygon(pts, outline=color, fill="", width=1)
            canvas.create_text(x + w // 2, y + h // 2 + 2, text="!", fill=color, font=("MS Sans Serif", 10, "bold"))
        
        elif self.shape == "error":
            # Error icon (X in circle)
            cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 1
            canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, width=1)
            canvas.create_line(cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3, fill=color, width=2)
            canvas.create_line(cx + r - 3, cy - r + 3, cx - r + 3, cy + r - 3, fill=color, width=2)


class IconManager:
    """Manages icons for the application."""
    
    _instance: Optional['IconManager'] = None
    
    def __new__(cls) -> 'IconManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._icons: Dict[str, Icon] = {}
        self._setup_defaults()
        self._initialized = True
    
    def _setup_defaults(self) -> None:
        """Set up default icons."""
        self._icons = {
            "check": GeometricIcon("check", "check"),
            "cross": GeometricIcon("cross", "cross"),
            "arrow_down": GeometricIcon("arrow_down", "arrow_down"),
            "arrow_up": GeometricIcon("arrow_up", "arrow_up"),
            "folder": GeometricIcon("folder", "folder"),
            "file": GeometricIcon("file", "file"),
            "gear": GeometricIcon("gear", "gear"),
            "info": GeometricIcon("info", "info"),
            "warning": GeometricIcon("warning", "warning"),
            "error": GeometricIcon("error", "error"),
            "close": UnicodeIcon("close", "×", 14),
            "minimize": UnicodeIcon("minimize", "—", 14),
            "maximize": UnicodeIcon("maximize", "□", 10)
        }
    
    def get(self, name: str) -> Optional[Icon]:
        """Get an icon by name."""
        return self._icons.get(name)
    
    def register(self, name: str, icon: Icon) -> None:
        """Register a custom icon."""
        self._icons[name] = icon
    
    def draw(self, name: str, canvas: tk.Canvas, x: int, y: int, color: str) -> bool:
        """Draw an icon on a canvas."""
        icon = self._icons.get(name)
        if icon:
            icon.draw(canvas, x, y, color)
            return True
        return False


def get_icon_manager() -> IconManager:
    """Get the global icon manager."""
    return IconManager()
