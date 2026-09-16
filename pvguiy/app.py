"""PVGUIY Application System - Main application class."""

import tkinter as tk
from typing import Optional, Any
from pvguiy.theme import ThemeManager, get_theme, GREEN
from pvguiy.scheme import Scheme
from pvguiy.notifications import NotificationManager
from pvguiy.console import Console as ConsoleWidget
from pvguiy.dialogs import MessageBox


class VGUI:
    """Main PVGUIY application class."""
    
    def __init__(self, title: str = "PVGUIY Application", 
                 width: int = 900, height: int = 600,
                 theme: str = "green", borderless: bool = True):
        self.root = tk.Tk()
        self.root.title(title)
        
        self._theme_manager = ThemeManager(theme)
        self._scheme = Scheme(self._theme_manager.current_theme)
        
        if borderless:
            self.root.overrideredirect(True)
        
        self.root.configure(bg=self._scheme.background_dark)
        
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        self._width = width
        self._height = height
        self._drag_x = 0
        self._drag_y = 0
        
        self._titlebar = None
        self._content = None
        self._notifications = None
        self._console = None
        
        self._build()
        
        self._widgets = []
    
    def _build(self) -> None:
        """Build the application UI structure."""
        self._outer = tk.Frame(self.root, bg=self._scheme.border_dark, bd=0)
        self._outer.pack(fill='both', expand=True)
        
        self._titlebar = tk.Frame(self._outer, bg=self._scheme.background_dark, height=30)
        self._titlebar.pack(fill='x')
        self._titlebar.pack_propagate(False)
        
        self._titlebar.bind("<ButtonPress-1>", self._drag_start)
        self._titlebar.bind("<B1-Motion>", self._drag)
        
        self._title_label = tk.Label(
            self._titlebar, text="PVGUIY",
            bg=self._scheme.background_dark,
            fg=self._scheme.white,
            font=("MS Sans Serif", 8, "bold")
        )
        self._title_label.pack(side='left', padx=9)
        
        self._minimize = tk.Label(
            self._titlebar, text="—", width=4,
            bg=self._scheme.background_dark,
            fg=self._scheme.text,
            font=("MS Sans Serif", 10)
        )
        self._minimize.pack(side='right', fill='y')
        self._minimize.bind("<Button-1>", lambda e: self._minimize())
        
        self._close = tk.Label(
            self._titlebar, text="×", width=4,
            bg=self._scheme.background_dark,
            fg=self._scheme.text,
            font=("MS Sans Serif", 12, "bold")
        )
        self._close.pack(side='right', fill='y')
        self._close.bind("<Button-1>", lambda e: self.destroy())
        self._close.bind("<Enter>", lambda e: self._close.configure(bg=self._scheme.error, fg=self._scheme.white))
        self._close.bind("<Leave>", lambda e: self._close.configure(bg=self._scheme.background_dark, fg=self._scheme.text))
        
        self._content = tk.Frame(self._outer, bg=self._scheme.background)
        self._content.pack(fill='both', expand=True, padx=2, pady=(0, 2))
        
        self._notifications = NotificationManager(self.root, self._scheme)
    
    def _drag_start(self, event) -> None:
        self._drag_x = event.x
        self._drag_y = event.y
    
    def _drag(self, event) -> None:
        x = self.root.winfo_x() + event.x - self._drag_x
        y = self.root.winfo_y() + event.y - self._drag_y
        self.root.geometry(f"+{x}+{y}")
    
    def _minimize(self) -> None:
        self.root.overrideredirect(False)
        self.root.iconify()
        self.root.bind("<Map>", self._restore, add="+")
    
    def _restore(self, event=None) -> None:
        if self.root.state() == "normal":
            self.root.overrideredirect(True)
    
    @property
    def scheme(self):
        return self._scheme
    
    @property
    def notify(self):
        return self._notifications
    
    @property
    def console(self):
        return self._console
    
    def set_title(self, title: str) -> None:
        self._title_label.configure(text=title)
    
    def set_theme(self, theme_name: str) -> None:
        self._theme_manager.set_theme(theme_name)
        self._scheme = Scheme(self._theme_manager.current_theme)
        
        self.root.configure(bg=self._scheme.background_dark)
        self._outer.configure(bg=self._scheme.border_dark)
        self._titlebar.configure(bg=self._scheme.background_dark)
        self._title_label.configure(bg=self._scheme.background_dark, fg=self._scheme.white)
        self._close.configure(bg=self._scheme.background_dark, fg=self._scheme.text)
        self._minimize.configure(bg=self._scheme.background_dark, fg=self._scheme.text)
        self._content.configure(bg=self._scheme.background)
        
        if self._notifications:
            self._notifications.set_scheme(self._scheme)
        
        self._update_widgets(self._content)
    
    def _update_widgets(self, parent) -> None:
        for child in parent.winfo_children():
            if hasattr(child, "set_scheme"):
                child.set_scheme(self._scheme)
            if child.winfo_children():
                self._update_widgets(child)
    
    def show_message(self, title: str, message: str, kind: str = "info") -> None:
        """Show a message box."""
        MessageBox(self.root, title, message, kind, self._scheme)
    
    def show_about(self, title: str, version: str, description: str = "") -> None:
        """Show an about dialog."""
        msg = f"{title}\nVersion {version}\n\n{description}" if description else f"{title}\nVersion {version}"
        MessageBox(self.root, "About", msg, "info", self._scheme)
    
    def destroy(self) -> None:
        self.root.destroy()
    
    def run(self) -> None:
        self.root.mainloop()
    
    def mainloop(self) -> None:
        self.run()


class Application(VGUI):
    """Alias for VGUI class."""
    pass
