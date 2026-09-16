"""PVGUIY Core Widget System - Base widget classes and hierarchy."""

import tkinter as tk
from typing import Optional, List, Dict, Any, Callable
from pvguiy.events import EventEmitter, EVENT_CLICK, EVENT_DESTROY, EVENT_SHOW, EVENT_HIDE
from pvguiy.exceptions import WidgetError


class WidgetState:
    """Widget state enumeration."""
    NORMAL = "normal"
    HOVER = "hover"
    ARMED = "armed"
    PRESSED = "pressed"
    DISABLED = "disabled"
    FOCUSED = "focused"
    SELECTED = "selected"
    CHECKED = "checked"
    ACTIVE = "active"


class Widget(tk.Frame, EventEmitter):
    """Base widget class for all PVGUIY widgets."""
    
    def __init__(self, parent=None, scheme=None, **kwargs):
        self._scheme = scheme
        self._state = WidgetState.NORMAL
        self._enabled = True
        self._visible = True
        self._focusable = False
        self._children: List['Widget'] = []
        self._parent: Optional['Widget'] = None
        
        bg = kwargs.pop('bg', None)
        if bg is None and scheme:
            bg = scheme.panel
        
        tk.Frame.__init__(self, parent, bg=bg or '#444444', **kwargs)
        EventEmitter.__init__(self)
        
        if hasattr(parent, '_add_child'):
            parent._add_child(self)
    
    @property
    def scheme(self):
        if self._scheme:
            return self._scheme
        if hasattr(self.master, 'scheme'):
            return self.master.scheme
        return None
    
    @property
    def state(self) -> str:
        return self._state
    
    @state.setter
    def state(self, value: str):
        old_state = self._state
        self._state = value
        if old_state != value:
            self._on_state_change(old_state, value)
    
    @property
    def enabled(self) -> bool:
        return self._enabled
    
    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        if not enabled:
            self.state = WidgetState.DISABLED
        else:
            self.state = WidgetState.NORMAL
        self.emit(EVENT_ENABLE if enabled else EVENT_DISABLE)
    
    def set_scheme(self, scheme) -> None:
        self._scheme = scheme
    
    def _on_state_change(self, old_state: str, new_state: str) -> None:
        pass
    
    def _add_child(self, child: 'Widget') -> None:
        self._children.append(child)
        child._parent = self
    
    def remove_child(self, child: 'Widget') -> None:
        if child in self._children:
            self._children.remove(child)
            child.destroy()
    
    def find(self, name: str) -> Optional['Widget']:
        if hasattr(self, 'name') and self.name == name:
            return self
        for child in self._children:
            result = child.find(name)
            if result:
                return result
        return None
    
    def find_all(self, name: str) -> List['Widget']:
        results = []
        if hasattr(self, 'name') and self.name == name:
            results.append(self)
        for child in self._children:
            results.extend(child.find_all(name))
        return results
    
    def destroy(self) -> None:
        self.emit(EVENT_DESTROY)
        self.clear()
        for child in list(self._children):
            child.destroy()
        try:
            self.destroy()
        except:
            pass
        try:
            self.master.forget(self)
        except:
            pass
    
    def show(self) -> None:
        self._visible = True
        self.pack_configure()
        self.emit(EVENT_SHOW)
    
    def hide(self) -> None:
        self._visible = False
        self.pack_forget()
        self.emit(EVENT_HIDE)


class Container(Widget):
    """Base container for other widgets."""
    
    def __init__(self, parent=None, scheme=None, **kwargs):
        super().__init__(parent, scheme, **kwargs)
        self._layout = None
        self._widgets: List[Widget] = []
    
    def _add_child(self, child: Widget) -> None:
        super()._add_child(child)
        self._widgets.append(child)
        if self._layout:
            self._layout.add_widget(child)
    
    def add_child(self, child: Widget) -> None:
        self._add_child(child)
    
    def remove_child(self, child: Widget) -> None:
        if child in self._widgets:
            self._widgets.remove(child)
        super().remove_child(child)
    
    def set_layout(self, layout) -> None:
        self._layout = layout
        if layout:
            layout.apply(self)
    
    def get_children(self) -> List[Widget]:
        return list(self._widgets)
    
    def clear(self) -> None:
        for child in list(self._widgets):
            child.destroy()
        self._widgets.clear()


class Panel(Container):
    """Basic panel container with classic VGUI styling."""
    
    def __init__(self, parent=None, scheme=None, width=200, height=100, **kwargs):
        super().__init__(parent, scheme, **kwargs)
        self.configure(width=width, height=height)
        self.pack_propagate(False)
        
        if scheme:
            self.configure(bg=scheme.panel)
    
    def set_scheme(self, scheme) -> None:
        super().set_scheme(scheme)
        if scheme:
            self.configure(bg=scheme.panel)
        for child in self._widgets:
            if hasattr(child, 'set_scheme'):
                child.set_scheme(scheme)


class Frame(Container):
    """Frame with optional title (GroupBox style)."""
    
    def __init__(self, parent=None, title=None, scheme=None, 
                 width=300, height=200, **kwargs):
        super().__init__(parent, scheme, **kwargs)
        self.configure(width=width, height=height, bg=scheme.panel if scheme else '#596952')
        self.pack_propagate(False)
        
        self._title = title
        self._header = None
        self._content = None
        self._title_label = None
        
        if title:
            self._create_header()
        
        self._create_content()
    
    def _create_header(self) -> None:
        self._header = tk.Frame(self, bg=self.scheme.panel if self.scheme else '#596952')
        self._header.pack(fill='x', padx=10, pady=(7, 0))
        
        self._title_label = tk.Label(
            self._header,
            text=self._title,
            bg=self.scheme.panel if self.scheme else '#596952',
            fg=self.scheme.white if self.scheme else '#E7E9DD',
            font=('MS Sans Serif', 8, 'bold')
        )
        self._title_label.pack(side='left')
    
    def _create_content(self) -> None:
        self._content = tk.Frame(self, bg=self.scheme.panel if self.scheme else '#596952')
        if self._header:
            self._content.pack(fill='both', expand=True, padx=10, pady=8)
        else:
            self._content.pack(fill='both', expand=True, padx=10, pady=10)
    
    @property
    def content(self) -> tk.Frame:
        return self._content
    
    def set_scheme(self, scheme) -> None:
        super().set_scheme(scheme)
        if scheme:
            self.configure(bg=scheme.panel)
            if self._header:
                self._header.configure(bg=scheme.panel)
            if self._content:
                self._content.configure(bg=scheme.panel)
            if self._title_label:
                self._title_label.configure(bg=scheme.panel, fg=scheme.white)
        for child in self._widgets:
            if hasattr(child, 'set_scheme'):
                child.set_scheme(scheme)


class Label(tk.Label):
    """Label widget with VGUI styling."""
    
    def __init__(self, parent, text="", scheme=None, **kwargs):
        self._scheme = scheme
        scheme = scheme or (getattr(parent, 'scheme', None))
        
        bg = kwargs.pop('bg', scheme.panel if scheme else '#596952')
        fg = kwargs.pop('fg', scheme.text if scheme else '#E2E5D8')
        font = kwargs.pop('font', ('MS Sans Serif', 8))
        
        super().__init__(parent, text=text, bg=bg, fg=fg, font=font, **kwargs)
    
    @property
    def scheme(self):
        if self._scheme:
            return self._scheme
        if hasattr(self.master, 'scheme'):
            return self.master.scheme
        return None
    
    def set_scheme(self, scheme) -> None:
        self._scheme = scheme
        if scheme:
            self.configure(bg=scheme.panel, fg=scheme.text)
    
    def set_text(self, text: str) -> None:
        self.configure(text=text)
