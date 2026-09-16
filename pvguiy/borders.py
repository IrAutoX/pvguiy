"""PVGUIY Borders System - Classic VGUI-style border rendering."""

from typing import Any, Optional


class Border:
    """Base border class for drawing classic VGUI-style borders."""
    
    def __init__(self, scheme):
        self.scheme = scheme
    
    def raised(self, canvas: Any, x: int, y: int, w: int, h: int) -> None:
        """Draw a raised border (button-style)."""
        light = self.scheme.border_light
        dark = self.scheme.black if hasattr(self.scheme, 'black') else self.scheme.border_dark
        
        # Top and left (light)
        canvas.create_line(x + 1, y + 1, x + w - 2, y + 1, fill=light)
        canvas.create_line(x + 1, y + 1, x + 1, y + h - 2, fill=light)
        
        # Bottom and right (dark)
        canvas.create_line(x + 1, y + h - 2, x + w - 2, y + h - 2, fill=dark)
        canvas.create_line(x + w - 2, y + 1, x + w - 2, y + h - 2, fill=dark)
    
    def sunken(self, canvas: Any, x: int, y: int, w: int, h: int) -> None:
        """Draw a sunken border (input field-style)."""
        black = self.scheme.black if hasattr(self.scheme, 'black') else '#000000'
        light = self.scheme.border_light
        
        # Top and left (dark/black)
        canvas.create_line(x + 1, y + 1, x + w - 2, y + 1, fill=black)
        canvas.create_line(x + 1, y + 1, x + 1, y + h - 2, fill=black)
        
        # Bottom and right (light)
        canvas.create_line(x + 1, y + h - 2, x + w - 2, y + h - 2, fill=light)
        canvas.create_line(x + w - 2, y + 1, x + w - 2, y + h - 2, fill=light)
    
    def flat(self, canvas: Any, x: int, y: int, w: int, h: int, color: Optional[str] = None) -> None:
        """Draw a flat border."""
        c = color or self.scheme.border_dark
        canvas.create_rectangle(x, y, x + w, y + h, outline=c, width=1)
    
    def focus(self, canvas: Any, x: int, y: int, w: int, h: int) -> None:
        """Draw a focus border."""
        c = self.scheme.border_focus if hasattr(self.scheme, 'border_focus') else self.scheme.highlight
        canvas.create_rectangle(x, y, x + w, y + h, outline=c, width=2)
    
    def disabled(self, canvas: Any, x: int, y: int, w: int, h: int) -> None:
        """Draw a disabled border."""
        c = self.scheme.border_dark
        canvas.create_rectangle(x, y, x + w, y + h, outline=c, width=1)


class RaisedBorder(Border):
    """Raised border for buttons and panels."""
    
    def draw(self, canvas: Any, x: int, y: int, w: int, h: int) -> None:
        self.raised(canvas, x, y, w, h)


class SunkenBorder(Border):
    """Sunken border for input fields."""
    
    def draw(self, canvas: Any, x: int, y: int, w: int, h: int) -> None:
        self.sunken(canvas, x, y, w, h)


class FlatBorder(Border):
    """Flat border for simple containers."""
    
    def __init__(self, scheme, color: Optional[str] = None):
        super().__init__(scheme)
        self.color = color
    
    def draw(self, canvas: Any, x: int, y: int, w: int, h: int) -> None:
        self.flat(canvas, x, y, w, h, self.color)


class LineBorder(Border):
    """Simple line border."""
    
    def __init__(self, scheme, color: str, width: int = 1):
        super().__init__(scheme)
        self.color = color
        self.width = width
    
    def draw(self, canvas: Any, x: int, y: int, w: int, h: int) -> None:
        canvas.create_rectangle(x, y, x + w, y + h, outline=self.color, width=self.width)


class FocusBorder(Border):
    """Focus indicator border."""
    
    def draw(self, canvas: Any, x: int, y: int, w: int, h: int) -> None:
        self.focus(canvas, x, y, w, h)


class DisabledBorder(Border):
    """Disabled state border."""
    
    def draw(self, canvas: Any, x: int, y: int, w: int, h: int) -> None:
        self.disabled(canvas, x, y, w, h)
