"""PVGUIY Menu System - Menu bars and context menus."""

import tkinter as tk
from typing import Optional, List, Callable


class MenuItem:
    """Represents a menu item."""
    
    def __init__(self, label: str, command: Optional[Callable] = None, 
                 shortcut: str = "", checked: bool = False, disabled: bool = False):
        self.label = label
        self.command = command
        self.shortcut = shortcut
        self.checked = checked
        self.disabled = disabled
        self._submenu: Optional['Menu'] = None
    
    def set_submenu(self, submenu: 'Menu') -> None:
        self._submenu = submenu
    
    def has_submenu(self) -> bool:
        return self._submenu is not None
    
    def get_submenu(self) -> Optional['Menu']:
        return self._submenu


class Separator:
    """Menu separator."""
    pass


class Menu(tk.Menu):
    """Popup menu."""
    
    def __init__(self, title: str = "", scheme=None):
        self._scheme = scheme
        bg = scheme.panel if scheme else "#596952"
        fg = scheme.text if scheme else "#E2E5D8"
        
        super().__init__(None, tearoff=False, bg=bg, fg=fg,
                        activebackground=scheme.highlight if scheme else "#82966F",
                        activeforeground=scheme.white if scheme else "#E7E9DD",
                        font=("MS Sans Serif", 9),
                        relief='flat', bd=1)
        
        self._title = title
        self._items: List[MenuItem] = []
    
    def add_item(self, label: str, command: Optional[Callable] = None,
                 shortcut: str = "", checked: bool = False) -> 'Menu':
        item = MenuItem(label, command, shortcut, checked)
        self._items.append(item)
        self.add_command(label=label, command=command)
        return self
    
    def add_separator(self) -> 'Menu':
        self._items.append(Separator())
        self.add_separator()
        return self
    
    def add_cascade(self, label: str, submenu: 'Menu') -> 'Menu':
        item = MenuItem(label)
        item.set_submenu(submenu)
        self._items.append(item)
        self.add_cascade(label=label, menu=submenu)
        return self
    
    def get_items(self) -> List[MenuItem]:
        return list(self._items)


class MenuBar(tk.Frame):
    """Main menu bar."""
    
    def __init__(self, parent, scheme=None):
        self._scheme = scheme
        bg = scheme.background_dark if scheme else "#30392D"
        
        super().__init__(parent, bg=bg, height=24)
        self.pack_propagate(False)
        self.pack(fill='x')
        
        self._menus: List[tuple] = []
        self._open_menu: Optional[tk.Menu] = None
        self._menu_buttons: List[tk.Label] = []
    
    def add_menu(self, menu: Menu) -> 'MenuBar':
        title = menu._title
        
        btn = tk.Label(
            self, text=title,
            bg=self.cget('bg'),
            fg=self._scheme.titlebar_text if self._scheme else "#E7E9DD",
            font=("MS Sans Serif", 8),
            padx=8, pady=3
        )
        btn.pack(side='left')
        
        def on_click(event=None):
            self._show_menu(menu, btn)
        
        btn.bind("<Button-1>", on_click)
        btn.bind("<Enter>", lambda e: btn.configure(
            fg=self._scheme.white if self._scheme else "#E7E9DD"
        ))
        btn.bind("<Leave>", lambda e: btn.configure(
            fg=self._scheme.titlebar_text if self._scheme else "#E7E9DD"
        ))
        
        self._menus.append((menu, btn))
        self._menu_buttons.append(btn)
        
        return self
    
    def _show_menu(self, menu: Menu, button: tk.Label) -> None:
        if self._open_menu:
            self._open_menu.unpost()
        
        self._open_menu = menu
        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()
        
        menu.post(x, y)
        
        def on_focus_out(event=None):
            if self._open_menu:
                self._open_menu.unpost()
                self._open_menu = None
        
        button.bind("<FocusOut>", on_focus_out)
    
    def clear(self) -> None:
        for widget in self._menu_buttons:
            widget.destroy()
        self._menu_buttons.clear()
        self._menus.clear()


class ContextMenu(Menu):
    """Context (right-click) menu."""
    
    def __init__(self, scheme=None):
        super().__init__("", scheme)
    
    def show(self, event) -> None:
        self.post(event.x_root, event.y_root)
    
    def bind_to(self, widget) -> None:
        widget.bind("<Button-3>", lambda e: self.show(e))
