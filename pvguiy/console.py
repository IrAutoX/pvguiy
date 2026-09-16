"""PVGUIY Console Widget - Log console with colored output."""

import tkinter as tk
from typing import Optional, List
from datetime import datetime


class Console(tk.Frame):
    """Console widget for displaying log messages."""
    
    def __init__(self, parent, scheme=None, width=400, height=200, max_lines=1000):
        self._scheme = scheme
        bg = scheme.console if scheme else "#10140F"
        
        super().__init__(parent, bg=bg)
        
        self._max_lines = max_lines
        self._line_count = 0
        
        # Text widget
        self._text = tk.Text(
            self,
            bg=bg,
            fg=scheme.text if scheme else "#E2E5D8",
            insertbackground=scheme.white if scheme else "#E7E9DD",
            selectbackground=scheme.selection if scheme else "#4a5a45",
            font=("Courier New", 8),
            wrap='word',
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        self._text.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        self._scrollbar = tk.Scrollbar(
            self, orient='vertical', command=self._text.yview,
            bg=scheme.scrollbar if scheme else "#3B4637",
            troughcolor=scheme.background_dark if scheme else "#30392D",
            activebackground=scheme.highlight if scheme else "#82966F"
        )
        self._scrollbar.pack(side='right', fill='y')
        
        self._text.configure(yscrollcommand=self._scrollbar.set)
        
        # Configure tags for different log levels
        self._configure_tags()
    
    def _configure_tags(self) -> None:
        scheme = self._scheme
        
        self._text.tag_configure("timestamp", foreground="#666666")
        self._text.tag_configure("normal", foreground=scheme.text if scheme else "#E2E5D8")
        self._text.tag_configure("info", foreground=scheme.highlight if scheme else "#82966F")
        self._text.tag_configure("success", foreground=scheme.success if scheme else "#75995B")
        self._text.tag_configure("warning", foreground=scheme.warning if scheme else "#B29A56")
        self._text.tag_configure("error", foreground=scheme.error if scheme else "#B94A48")
    
    def _get_timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")
    
    def _append(self, message: str, tag: str = "normal") -> None:
        timestamp = f"[{self._get_timestamp()}] "
        
        self._text.insert('end', timestamp, "timestamp")
        self._text.insert('end', message + "\n", tag)
        
        self._line_count += 1
        
        # Auto-scroll
        self._text.see('end')
        
        # Limit lines
        if self._line_count > self._max_lines:
            lines_to_delete = self._line_count - self._max_lines
            self._text.delete('1.0', f'{lines_to_delete}.0')
            self._line_count = self._max_lines
    
    def write(self, message: str) -> 'Console':
        """Write a normal message."""
        self._append(message, "normal")
        return self
    
    def info(self, message: str) -> 'Console':
        """Write an info message."""
        self._append(f"INFO: {message}", "info")
        return self
    
    def success(self, message: str) -> 'Console':
        """Write a success message."""
        self._append(f"SUCCESS: {message}", "success")
        return self
    
    def warning(self, message: str) -> 'Console':
        """Write a warning message."""
        self._append(f"WARNING: {message}", "warning")
        return self
    
    def error(self, message: str) -> 'Console':
        """Write an error message."""
        self._append(f"ERROR: {message}", "error")
        return self
    
    def clear(self) -> 'Console':
        """Clear the console."""
        self._text.delete('1.0', 'end')
        self._line_count = 0
        return self
    
    def set_scheme(self, scheme) -> None:
        self._scheme = scheme
        self._text.configure(
            bg=scheme.console,
            fg=scheme.text,
            insertbackground=scheme.white,
            selectbackground=scheme.selection
        )
        self._scrollbar.configure(
            bg=scheme.scrollbar,
            troughcolor=scheme.background_dark,
            activebackground=scheme.highlight
        )
        self._configure_tags()
