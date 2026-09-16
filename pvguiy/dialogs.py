"""PVGUIY Dialog System - Message boxes and dialogs."""

import tkinter as tk
from typing import Optional, Callable


class Dialog(tk.Toplevel):
    """Base dialog class."""
    
    def __init__(self, parent, title: str = "Dialog", scheme=None, modal: bool = True):
        super().__init__(parent)
        
        self._scheme = scheme
        self._result = None
        
        self.title(title)
        self.configure(bg=scheme.background_dark if scheme else "#30392D")
        
        self.resizable(False, False)
        
        if modal:
            self.transient(parent)
            self.grab_set()
        
        self._center_on_parent(parent)
    
    def _center_on_parent(self, parent) -> None:
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        
        self.geometry(f"+{x}+{y}")
    
    def set_result(self, result) -> None:
        self._result = result
        self.destroy()
    
    def get_result(self):
        return self._result


class MessageBox(Dialog):
    """Classic message box dialog."""
    
    def __init__(self, parent, title: str, message: str, 
                 kind: str = "info", scheme=None):
        super().__init__(parent, title, scheme, modal=True)
        
        self._kind = kind
        self._message = message
        
        self._build()
        
        # Wait for user response
        self.wait_window(self)
    
    def _build(self) -> None:
        colors = {
            "info": self._scheme.highlight if self._scheme else "#82966F",
            "success": self._scheme.success if self._scheme else "#75995B",
            "warning": self._scheme.warning if self._scheme else "#B29A56",
            "error": self._scheme.error if self._scheme else "#B94A48"
        }
        accent = colors.get(self._kind, self._scheme.highlight if self._scheme else "#82966F")
        
        # Icon based on kind
        icons = {
            "info": "ℹ",
            "success": "✓",
            "warning": "⚠",
            "error": "✕"
        }
        icon = icons.get(self._kind, "ℹ")
        
        main_frame = tk.Frame(self, bg=self._scheme.panel if self._scheme else "#596952")
        main_frame.pack(padx=15, pady=15)
        
        # Top section with icon and message
        top_frame = tk.Frame(main_frame, bg=self._scheme.panel if self._scheme else "#596952")
        top_frame.pack(fill='x', pady=(0, 15))
        
        icon_label = tk.Label(
            top_frame, text=icon, font=('MS Sans Serif', 24),
            bg=self._scheme.panel if self._scheme else "#596952",
            fg=accent
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        msg_label = tk.Label(
            top_frame, text=self._message,
            bg=self._scheme.panel if self._scheme else "#596952",
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            font=('MS Sans Serif', 9),
            wraplength=300, justify='left'
        )
        msg_label.pack(side='left', fill='x', expand=True)
        
        # Bottom section with OK button
        btn_frame = tk.Frame(main_frame, bg=self._scheme.panel if self._scheme else "#596952")
        btn_frame.pack(fill='x')
        
        ok_btn = tk.Button(
            btn_frame, text="OK", width=10,
            bg=self._scheme.button if self._scheme else "#596952",
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            font=('MS Sans Serif', 8),
            relief='flat',
            command=lambda: self.set_result(True)
        )
        ok_btn.pack(side='right')


class ConfirmDialog(Dialog):
    """Confirmation dialog with Yes/No buttons."""
    
    def __init__(self, parent, title: str, message: str, scheme=None):
        super().__init__(parent, title, scheme, modal=True)
        self._message = message
        self._build()
        self.wait_window(self)
    
    def _build(self) -> None:
        main_frame = tk.Frame(self, bg=self._scheme.panel if self._scheme else "#596952")
        main_frame.pack(padx=15, pady=15)
        
        msg_label = tk.Label(
            main_frame, text=self._message,
            bg=self._scheme.panel if self._scheme else "#596952",
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            font=('MS Sans Serif', 9),
            wraplength=300
        )
        msg_label.pack(fill='x', pady=(0, 15))
        
        btn_frame = tk.Frame(main_frame, bg=self._scheme.panel if self._scheme else "#596952")
        btn_frame.pack(fill='x')
        
        yes_btn = tk.Button(
            btn_frame, text="Yes", width=10,
            bg=self._scheme.button if self._scheme else "#596952",
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            relief='flat',
            command=lambda: self.set_result(True)
        )
        yes_btn.pack(side='left')
        
        no_btn = tk.Button(
            btn_frame, text="No", width=10,
            bg=self._scheme.button if self._scheme else "#596952",
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            relief='flat',
            command=lambda: self.set_result(False)
        )
        no_btn.pack(side='right')


class InputDialog(Dialog):
    """Input dialog for getting text from user."""
    
    def __init__(self, parent, title: str, prompt: str, 
                 default: str = "", scheme=None):
        super().__init__(parent, title, scheme, modal=True)
        self._prompt = prompt
        self._default = default
        self._value = default
        self._build()
        self.wait_window(self)
    
    def _build(self) -> None:
        main_frame = tk.Frame(self, bg=self._scheme.panel if self._scheme else "#596952")
        main_frame.pack(padx=15, pady=15)
        
        prompt_label = tk.Label(
            main_frame, text=self._prompt,
            bg=self._scheme.panel if self._scheme else "#596952",
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            font=('MS Sans Serif', 9)
        )
        prompt_label.pack(anchor='w', pady=(0, 8))
        
        self._entry = tk.Entry(
            main_frame,
            bg=self._scheme.input if self._scheme else "#20261E",
            fg=self._scheme.white if self._scheme else "#E7E9DD",
            insertbackground=self._scheme.white if self._scheme else "#E7E9DD",
            font=('MS Sans Serif', 9)
        )
        self._entry.pack(fill='x', pady=(0, 15))
        self._entry.insert(0, self._default)
        
        btn_frame = tk.Frame(main_frame, bg=self._scheme.panel if self._scheme else "#596952")
        btn_frame.pack(fill='x')
        
        ok_btn = tk.Button(
            btn_frame, text="OK", width=10,
            bg=self._scheme.button if self._scheme else "#596952",
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            relief='flat',
            command=self._on_ok
        )
        ok_btn.pack(side='right')
        
        cancel_btn = tk.Button(
            btn_frame, text="Cancel", width=10,
            bg=self._scheme.button if self._scheme else "#596952",
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            relief='flat',
            command=lambda: self.set_result(None)
        )
        cancel_btn.pack(side='right', padx=(0, 8))
    
    def _on_ok(self) -> None:
        self._value = self._entry.get()
        self.set_result(self._value)
    
    def get_value(self) -> str:
        return self._value


class ErrorDialog(MessageBox):
    """Error message dialog."""
    
    def __init__(self, parent, title: str, message: str, scheme=None):
        super().__init__(parent, title, message, "error", scheme)


class WarningDialog(MessageBox):
    """Warning message dialog."""
    
    def __init__(self, parent, title: str, message: str, scheme=None):
        super().__init__(parent, title, message, "warning", scheme)


class AboutDialog(Dialog):
    """About dialog."""
    
    def __init__(self, parent, title: str, version: str, 
                 description: str = "", scheme=None):
        super().__init__(parent, title, scheme, modal=True)
        self._app_title = title
        self._version = version
        self._description = description
        self._build()
        self.wait_window(self)
    
    def _build(self) -> None:
        main_frame = tk.Frame(self, bg=self._scheme.panel if self._scheme else "#596952")
        main_frame.pack(padx=20, pady=20)
        
        title_label = tk.Label(
            main_frame, text=self._app_title,
            bg=self._scheme.panel if self._scheme else "#596952",
            fg=self._scheme.white if self._scheme else "#E7E9DD",
            font=('MS Sans Serif', 12, 'bold')
        )
        title_label.pack(pady=(0, 5))
        
        version_label = tk.Label(
            main_frame, text=f"Version {self._version}",
            bg=self._scheme.panel if self._scheme else "#596952",
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            font=('MS Sans Serif', 9)
        )
        version_label.pack(pady=(0, 10))
        
        if self._description:
            desc_label = tk.Label(
                main_frame, text=self._description,
                bg=self._scheme.panel if self._scheme else "#596952",
                fg=self._scheme.text if self._scheme else "#E2E5D8",
                font=('MS Sans Serif', 8),
                wraplength=250
            )
            desc_label.pack(pady=(0, 15))
        
        ok_btn = tk.Button(
            main_frame, text="OK", width=10,
            bg=self._scheme.button if self._scheme else "#596952",
            fg=self._scheme.text if self._scheme else "#E2E5D8",
            relief='flat',
            command=lambda: self.set_result(True)
        )
        ok_btn.pack()
