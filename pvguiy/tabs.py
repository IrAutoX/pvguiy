"""PVGUIY Tab System - Tab control widget."""

import tkinter as tk
from typing import Optional, List, Dict


class Tab:
    """Represents a single tab."""
    
    def __init__(self, title: str, content: tk.Frame, disabled: bool = False):
        self.title = title
        self.content = content
        self.disabled = disabled
        self._button: Optional[tk.Label] = None


class TabControl(tk.Frame):
    """Tab control with multiple tabs."""
    
    def __init__(self, parent, scheme=None):
        self._scheme = scheme
        bg = scheme.panel if scheme else "#596952"
        
        super().__init__(parent, bg=bg)
        
        self._tabs: List[Tab] = []
        self._active_index: int = -1
        self._tab_buttons: List[tk.Label] = []
        self._tab_frame: Optional[tk.Frame] = None
        
        self._build()
    
    def _build(self) -> None:
        # Tab bar
        self._tab_bar = tk.Frame(
            self, bg=self._scheme.background_dark if self._scheme else "#30392D",
            height=24
        )
        self._tab_bar.pack(fill='x')
        self._tab_bar.pack_propagate(False)
        
        # Content area
        self._content_frame = tk.Frame(
            self, bg=self._scheme.panel if self._scheme else "#596952"
        )
        self._content_frame.pack(fill='both', expand=True)
    
    def add_tab(self, title: str, content: tk.Frame, disabled: bool = False) -> Tab:
        tab = Tab(title, content, disabled)
        self._tabs.append(tab)
        
        idx = len(self._tabs) - 1
        
        # Create tab button
        is_active = (idx == self._active_index)
        bg = self._scheme.button_pressed if is_active and self._scheme else "#3B4637"
        fg = self._scheme.white if is_active and self._scheme else "#E2E5D8"
        
        btn = tk.Label(
            self._tab_bar, text=title,
            bg=bg, fg=fg,
            font=("MS Sans Serif", 8),
            padx=10, pady=4
        )
        btn.pack(side='left', padx=1)
        
        if not disabled:
            def on_click(i=idx):
                self._select_tab(i)
            
            btn.bind("<Button-1>", on_click)
        
        self._tab_buttons.append(btn)
        
        # Select first tab by default
        if self._active_index < 0:
            self._select_tab(0)
        
        return tab
    
    def remove_tab(self, index: int) -> None:
        if 0 <= index < len(self._tabs):
            tab = self._tabs.pop(index)
            btn = self._tab_buttons.pop(index)
            btn.destroy()
            
            if self._active_index >= len(self._tabs):
                self._active_index = max(0, len(self._tabs) - 1)
            
            if self._active_index >= 0:
                self._select_tab(self._active_index)
    
    def get_tab(self, index: int) -> Optional[Tab]:
        if 0 <= index < len(self._tabs):
            return self._tabs[index]
        return None
    
    def get_active_tab(self) -> Optional[Tab]:
        if 0 <= self._active_index < len(self._tabs):
            return self._tabs[self._active_index]
        return None
    
    def set_active_tab(self, index: int) -> None:
        if 0 <= index < len(self._tabs):
            self._select_tab(index)
    
    def _select_tab(self, index: int) -> None:
        if index < 0 or index >= len(self._tabs):
            return
        
        old_index = self._active_index
        self._active_index = index
        
        # Update all tab buttons
        for i, (tab, btn) in enumerate(zip(self._tabs, self._tab_buttons)):
            if i == index:
                bg = self._scheme.button_pressed if self._scheme else "#3B4637"
                fg = self._scheme.white if self._scheme else "#E7E9DD"
            else:
                bg = self._scheme.button if self._scheme else "#596952"
                fg = self._scheme.text if self._scheme else "#E2E5D8"
            
            if tab.disabled:
                bg = self._scheme.button_disabled if self._scheme else "#444444"
                fg = self._scheme.text_disabled if self._scheme else "#777777"
            
            btn.configure(bg=bg, fg=fg)
        
        # Show/hide content
        for i, tab in enumerate(self._tabs):
            if i == index:
                tab.content.pack(in_=self._content_frame, fill='both', expand=True)
            else:
                tab.content.pack_forget()
