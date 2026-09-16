"""PVGUIY Window System - Custom window implementation."""

import tkinter as tk
from typing import Optional, Callable


class TitleBar(tk.Frame):
    """Custom titlebar for PVGUIY windows."""
    
    def __init__(self, parent, title="Window", scheme=None, 
                 on_close: Optional[Callable] = None,
                 on_minimize: Optional[Callable] = None,
                 on_maximize: Optional[Callable] = None):
        self._scheme = scheme
        bg = scheme.background_dark if scheme else "#30392D"
        text_color = scheme.titlebar_text if scheme else "#E7E9DD"
        
        super().__init__(parent, bg=bg, height=30)
        self.pack_propagate(False)
        
        self._title = title
        self._on_close = on_close
        self._on_minimize = on_minimize
        self._on_maximize = on_maximize
        
        self._drag_x = 0
        self._drag_y = 0
        
        self.bind("<ButtonPress-1>", self._drag_start)
        self.bind("<B1-Motion>", self._drag)
        
        self._title_label = tk.Label(
            self, text=title, bg=bg, fg=text_color,
            font=("MS Sans Serif", 8, "bold")
        )
        self._title_label.pack(side='left', padx=9)
        
        self._create_buttons()
    
    def _create_buttons(self) -> None:
        bg = self.cget('bg')
        
        if self._on_minimize:
            self._min_btn = tk.Label(
                self, text="—", width=4, bg=bg,
                fg=self._scheme.text if self._scheme else "#E2E5D8",
                font=("MS Sans Serif", 10)
            )
            self._min_btn.pack(side='right', fill='y')
            self._min_btn.bind("<Button-1>", lambda e: self._on_minimize())
        
        if self._on_maximize:
            self._max_btn = tk.Label(
                self, text="□", width=4, bg=bg,
                fg=self._scheme.text if self._scheme else "#E2E5D8",
                font=("MS Sans Serif", 8)
            )
            self._max_btn.pack(side='right', fill='y')
            self._max_btn.bind("<Button-1>", lambda e: self._on_maximize())
        
        self._close_btn = tk.Label(
            self, text="×", width=4, bg=bg,
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            font=("MS Sans Serif", 12, "bold")
        )
        self._close_btn.pack(side='right', fill='y')
        self._close_btn.bind("<Button-1>", lambda e: self._on_close() if self._on_close else None)
        self._close_btn.bind("<Enter>", lambda e: self._close_btn.configure(
            bg=self._scheme.error if self._scheme else "#B94A48",
            fg=self._scheme.white if self._scheme else "#E7E9DD"
        ))
        self._close_btn.bind("<Leave>", lambda e: self._close_btn.configure(
            bg=self.cget('bg'),
            fg=self._scheme.text if self._scheme else "#E2E5D8"
        ))
    
    def _drag_start(self, event) -> None:
        self._drag_x = event.x
        self._drag_y = event.y
    
    def _drag(self, event) -> None:
        if hasattr(self.master, 'root'):
            root = self.master.root
        else:
            root = self.winfo_toplevel()
        
        x = root.winfo_x() + event.x - self._drag_x
        y = root.winfo_y() + event.y - self._drag_y
        root.geometry(f"+{x}+{y}")
    
    def set_title(self, title: str) -> None:
        self._title = title
        self._title_label.configure(text=title)


class Window(tk.Toplevel):
    """Custom window with PVGUIY styling."""
    
    def __init__(self, app, title="Window", width=600, height=400,
                 borderless=True, modal=False, **kwargs):
        super().__init__(app.root, **kwargs)
        
        self._app = app
        self._scheme = app.scheme
        self._width = width
        self._height = height
        
        if borderless:
            self.overrideredirect(True)
        
        self.configure(bg=self._scheme.background_dark)
        
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self._titlebar = TitleBar(
            self, title=title, scheme=self._scheme,
            on_close=self.destroy,
            on_minimize=self._iconify,
            on_maximize=self._toggle_maximize
        )
        
        self._content = tk.Frame(self, bg=self._scheme.background)
        self._content.pack(fill='both', expand=True, padx=2, pady=(0, 2))
        
        if modal:
            self.transient(app.root)
            self.grab_set()
            app.root.wait_window(self)
    
    def _iconify(self) -> None:
        self.overrideredirect(False)
        self.iconify()
    
    def _toggle_maximize(self) -> None:
        if self.state() == 'zoomed':
            self.state('normal')
            self.overrideredirect(True)
        else:
            self.overrideredirect(False)
            self.state('zoomed')
    
    @property
    def content(self) -> tk.Frame:
        return self._content
    
    def set_title(self, title: str) -> None:
        if self._titlebar:
            self._titlebar.set_title(title)
