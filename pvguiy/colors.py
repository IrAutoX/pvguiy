"""PVGUIY Color System - Handle colors with HEX, RGB, RGBA operations."""

from typing import Tuple, Union


class Color:
    """Represents a color with various conversion and manipulation methods."""
    
    def __init__(self, value: Union[str, Tuple[int, int, int], Tuple[int, int, int, float]]):
        """
        Initialize a Color.
        
        Args:
            value: Can be HEX string ("#RRGGBB"), RGB tuple (r, g, b), or RGBA tuple (r, g, b, a)
        """
        if isinstance(value, str):
            self._from_hex(value)
        elif isinstance(value, (tuple, list)):
            if len(value) == 3:
                self.r, self.g, self.b = value
                self.a = 1.0
            elif len(value) == 4:
                self.r, self.g, self.b = value[:3]
                self.a = value[3]
            else:
                raise ValueError(f"Invalid color tuple: {value}")
        else:
            raise ValueError(f"Invalid color value: {value}")
    
    def _from_hex(self, hex_color: str) -> None:
        """Parse a HEX color string."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            self.r = int(hex_color[0:2], 16)
            self.g = int(hex_color[2:4], 16)
            self.b = int(hex_color[4:6], 16)
            self.a = 1.0
        elif len(hex_color) == 8:
            self.r = int(hex_color[0:2], 16)
            self.g = int(hex_color[2:4], 16)
            self.b = int(hex_color[4:6], 16)
            self.a = int(hex_color[6:8], 16) / 255.0
        else:
            raise ValueError(f"Invalid HEX color: #{hex_color}")
    
    def to_hex(self) -> str:
        """Return the color as a HEX string."""
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"
    
    def to_rgba(self) -> Tuple[int, int, int, float]:
        """Return the color as an RGBA tuple."""
        return (self.r, self.g, self.b, self.a)
    
    def to_rgb(self) -> Tuple[int, int, int]:
        """Return the color as an RGB tuple."""
        return (self.r, self.g, self.b)
    
    def to_tkinter(self) -> str:
        """Return the color in Tkinter format."""
        return self.to_hex()
    
    @property
    def brightness(self) -> float:
        """Calculate perceived brightness (0-1)."""
        return (0.299 * self.r + 0.587 * self.g + 0.114 * self.b) / 255.0
    
    def lighten(self, factor: float = 0.1) -> 'Color':
        """Return a lighter version of this color."""
        factor = max(0, min(1, factor))
        r = int(self.r + (255 - self.r) * factor)
        g = int(self.g + (255 - self.g) * factor)
        b = int(self.b + (255 - self.b) * factor)
        return Color((r, g, b))
    
    def darken(self, factor: float = 0.1) -> 'Color':
        """Return a darker version of this color."""
        factor = max(0, min(1, factor))
        r = int(self.r * (1 - factor))
        g = int(self.g * (1 - factor))
        b = int(self.b * (1 - factor))
        return Color((r, g, b))
    
    def blend(self, other: 'Color', factor: float = 0.5) -> 'Color':
        """Blend with another color."""
        factor = max(0, min(1, factor))
        r = int(self.r * (1 - factor) + other.r * factor)
        g = int(self.g * (1 - factor) + other.g * factor)
        b = int(self.b * (1 - factor) + other.b * factor)
        return Color((r, g, b))
    
    def interpolate(self, other: 'Color', t: float) -> 'Color':
        """Interpolate between this color and another (t from 0 to 1)."""
        return self.blend(other, t)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return False
        return self.r == other.r and self.g == other.g and self.b == other.b
    
    def __repr__(self) -> str:
        return f"Color('{self.to_hex()}')"
    
    @staticmethod
    def from_rgb(r: int, g: int, b: int) -> 'Color':
        """Create a color from RGB values."""
        return Color((r, g, b))
    
    @staticmethod
    def from_rgba(r: int, g: int, b: int, a: float) -> 'Color':
        """Create a color from RGBA values."""
        return Color((r, g, b, a))
