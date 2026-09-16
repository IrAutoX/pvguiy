"""PVGUIY Notifications System - In-app notification manager."""

import tkinter as tk
from typing import Optional, List


class Notification:
    """A single notification with animation support."""
    
    def __init__(self, manager, title: str, message: str, 
                 kind: str = "info", timeout: int = 3500):
        self._manager = manager
        self._scheme = manager.scheme
        self._width = 330
        self._height = 76
        self._timeout = timeout
        self._kind = kind
        
        self._frame = tk.Frame(
            manager.root, bg=self._scheme.panel_dark,
            bd=0, highlightthickness=0
        )
        
        self._canvas = tk.Canvas(
            self._frame, width=self._width, height=self._height,
            bg=self._scheme.panel_dark, highlightthickness=0, bd=0
        )
        self._canvas.pack()
        
        colors = {
            "info": self._scheme.highlight,
            "success": self._scheme.success,
            "warning": self._scheme.warning,
            "error": self._scheme.error
        }
        accent = colors.get(kind, self._scheme.highlight)
        
        self._draw(accent)
    
    def _draw(self, accent: str) -> None:
        c = self._canvas
        w, h = self._width, self._height
        
        c.create_rectangle(0, 0, w-1, h-1, fill=self._scheme.panel, outline=self._scheme.border_dark)
        c.create_line(1, 1, w-2, 1, fill=self._scheme.border_light)
        c.create_line(1, 1, 1, h-2, fill=self._scheme.border_light)
        c.create_line(1, h-2, w-2, h-2, fill=self._scheme.black)
        c.create_line(w-2, 1, w-2, h-2, fill=self._scheme.black)
        
        c.create_rectangle(5, 6, 9, h-7, fill=accent, outline=accent)
        
        c.create_text(18, 17, text=self._title_text if hasattr(self, '_title_text') else "",
                      anchor='w', fill=self._scheme.white, font=('MS Sans Serif', 8, 'bold'))
        c.create_text(18, 43, text=self._message_text if hasattr(self, '_message_text') else "",
                      anchor='w', fill=self._scheme.text, font=('MS Sans Serif', 8), width=w-55)
        c.create_text(w-15, 13, text="×", fill=self._scheme.text, font=('MS Sans Serif', 9, 'bold'))
        
        c.bind("<Button-1>", lambda e: self.close())
    
    @property
    def _title_text(self) -> str:
        return getattr(self, '_title', '')
    
    @property
    def _message_text(self) -> str:
        return getattr(self, '_message', '')
    
    @_title_text.setter
    def _title_text(self, value):
        self._title = value
    
    @_message_text.setter
    def _message_text(self, value):
        self._message = value
    
    def show(self, y: int) -> None:
        root_w = self._manager.root.winfo_width()
        target = root_w - self._width - 12
        
        self._frame.place(x=root_w, y=y, width=self._width, height=self._height)
        self._animate(root_w, target)
    
    def _animate(self, x: int, target: int) -> None:
        if not self._frame.winfo_exists():
            return
        
        if x <= target:
            self._frame.place_configure(x=target)
            self._manager.root.after(self._timeout, self.close)
            return
        
        x -= 25
        self._frame.place_configure(x=x)
        self._manager.root.after(10, lambda: self._animate(x, target))
    
    def close(self) -> None:
        if self._frame.winfo_exists():
            self._frame.destroy()
        if self in self._manager.notifications:
            self._manager.notifications.remove(self)
        self._manager.reposition()


class NotificationManager:
    """Manages in-app notifications."""
    
    def __init__(self, root, scheme):
        self.root = root
        self.scheme = scheme
        self.notifications: List[Notification] = []
    
    def show(self, title: str, message: str, kind: str = "info", 
             timeout: int = 3500) -> Notification:
        notification = Notification(self, title, message, kind, timeout)
        notification._title = title
        notification._message = message
        self.notifications.insert(0, notification)
        self.reposition()
        return notification
    
    def info(self, title: str, message: str, timeout: int = 3500) -> Notification:
        return self.show(title, message, "info", timeout)
    
    def success(self, title: str, message: str, timeout: int = 3500) -> Notification:
        return self.show(title, message, "success", timeout)
    
    def warning(self, title: str, message: str, timeout: int = 3500) -> Notification:
        return self.show(title, message, "warning", timeout)
    
    def error(self, title: str, message: str, timeout: int = 3500) -> Notification:
        return self.show(title, message, "error", timeout)
    
    def reposition(self) -> None:
        y = 40
        for notification in self.notifications:
            if notification._frame.winfo_exists():
                notification._frame.place_configure(
                    x=self.root.winfo_width() - notification._width - 12,
                    y=y
                )
                y += notification._height + 8
    
    def set_scheme(self, scheme) -> None:
        self.scheme = scheme
        for n in self.notifications:
            n._scheme = scheme
