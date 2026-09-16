"""PVGUIY Exceptions Module."""


class PVGUIYError(Exception):
    """Base exception for PVGUIY framework."""
    pass


class ThemeError(PVGUIYError):
    """Exception raised for theme-related errors."""
    pass


class WidgetError(PVGUIYError):
    """Exception raised for widget-related errors."""
    pass


class LayoutError(PVGUIYError):
    """Exception raised for layout-related errors."""
    pass


class ConfigurationError(PVGUIYError):
    """Exception raised for configuration-related errors."""
    pass


class EventError(PVGUIYError):
    """Exception raised for event system-related errors."""
    pass


class WindowError(PVGUIYError):
    """Exception raised for window-related errors."""
    pass
