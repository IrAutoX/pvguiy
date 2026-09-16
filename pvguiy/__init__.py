"""
PVGUIY - Classic GoldSrc-inspired Python GUI Framework

A standalone, zero-dependency GUI framework inspired by Half-Life 1 / GoldSrc VGUI.
"""

from pvguiy.app import VGUI, Application
from pvguiy.core import Widget, Container, Panel, Frame, Label, Scheme
from pvguiy.window import Window, TitleBar
from pvguiy.events import Event, EventEmitter, EventSystem
from pvguiy.theme import Theme, ThemeManager
from pvguiy.scheme import Scheme as SchemeClass
from pvguiy.borders import Border, RaisedBorder, SunkenBorder, FlatBorder, LineBorder
from pvguiy.colors import Color
from pvguiy.fonts import Font, FontManager
from pvguiy.layout import Layout, AbsoluteLayout, VerticalLayout, HorizontalLayout, GridLayout, StackLayout, AnchorLayout
from pvguiy.animation import Animator, Tween, Timer, Animation
from pvguiy.timer import Timer as TimerClass, RepeatingTimer, DelayedCall
from pvguiy.dialogs import Dialog, MessageBox, ConfirmDialog, InputDialog, ErrorDialog, WarningDialog, AboutDialog
from pvguiy.notifications import Notification, NotificationManager
from pvguiy.menus import MenuBar, Menu, MenuItem, Separator, ContextMenu
from pvguiy.tabs import TabControl, Tab
from pvguiy.console import Console
from pvguiy.config import Config
from pvguiy.logging import Logger, LogLevel
from pvguiy.icons import Icon, IconManager
from pvguiy.serialization import Serializable
from pvguiy.exceptions import (
    PVGUIYError, ThemeError, WidgetError, LayoutError,
    ConfigurationError, EventError, WindowError
)

# Widgets
from pvguiy.widgets.label import Label as WidgetLabel
from pvguiy.widgets.button import Button
from pvguiy.widgets.checkbox import CheckButton
from pvguiy.widgets.radio import RadioButton
from pvguiy.widgets.entry import TextEntry, PasswordEntry
from pvguiy.widgets.textarea import TextArea
from pvguiy.widgets.progress import ProgressBar
from pvguiy.widgets.slider import Slider
from pvguiy.widgets.listbox import ListBox
from pvguiy.widgets.combobox import ComboBox
from pvguiy.widgets.scrollbar import ScrollBar
from pvguiy.widgets.groupbox import GroupBox
from pvguiy.widgets.statusbar import StatusBar
from pvguiy.widgets.tooltip import ToolTip

# Built-in themes
from pvguiy.theme import GREEN, ORANGE, BLACK, THEMES, get_theme

__version__ = "1.0.0"
__author__ = "PVGUIY Team"
__all__ = [
    # Core
    "VGUI", "Application",
    "Widget", "Container", "Panel", "Frame", "Label", "Scheme",
    "Window", "TitleBar",
    
    # Events
    "Event", "EventEmitter", "EventSystem",
    
    # Theme & Colors
    "Theme", "ThemeManager", "SchemeClass", "Color",
    "GREEN", "ORANGE", "BLACK", "THEMES", "get_theme",
    
    # Borders
    "Border", "RaisedBorder", "SunkenBorder", "FlatBorder", "LineBorder",
    
    # Fonts
    "Font", "FontManager",
    
    # Layout
    "Layout", "AbsoluteLayout", "VerticalLayout", "HorizontalLayout", 
    "GridLayout", "StackLayout", "AnchorLayout",
    
    # Animation & Timer
    "Animator", "Tween", "Timer", "Animation",
    "TimerClass", "RepeatingTimer", "DelayedCall",
    
    # Dialogs
    "Dialog", "MessageBox", "ConfirmDialog", "InputDialog", 
    "ErrorDialog", "WarningDialog", "AboutDialog",
    
    # Notifications
    "Notification", "NotificationManager",
    
    # Menus
    "MenuBar", "Menu", "MenuItem", "Separator", "ContextMenu",
    
    # Tabs
    "TabControl", "Tab",
    
    # Console
    "Console",
    
    # Config & Logging
    "Config", "Logger", "LogLevel",
    
    # Icons & Serialization
    "Icon", "IconManager", "Serializable",
    
    # Exceptions
    "PVGUIYError", "ThemeError", "WidgetError", "LayoutError",
    "ConfigurationError", "EventError", "WindowError",
    
    # Widgets
    "WidgetLabel", "Button", "CheckButton", "RadioButton",
    "TextEntry", "PasswordEntry", "TextArea",
    "ProgressBar", "Slider", "ListBox", "ComboBox",
    "ScrollBar", "GroupBox", "StatusBar", "ToolTip",
]
