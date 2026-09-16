"""PVGUIY Layout System - Automatic widget positioning."""

from typing import List, Optional, Dict, Any
from pvguiy.exceptions import LayoutError


class Layout:
    """Base layout class."""
    
    def __init__(self, spacing: int = 4, padding: int = 6):
        self.spacing = spacing
        self.padding = padding
        self._widgets: List = []
    
    def add_widget(self, widget) -> None:
        self._widgets.append(widget)
    
    def remove_widget(self, widget) -> None:
        if widget in self._widgets:
            self._widgets.remove(widget)
    
    def apply(self, container) -> None:
        raise NotImplementedError
    
    def calculate(self, container_width: int, container_height: int) -> Dict[str, Any]:
        raise NotImplementedError


class AbsoluteLayout(Layout):
    """Absolute positioning layout."""
    
    def apply(self, container) -> None:
        pass  # Widgets are positioned manually
    
    def calculate(self, container_width: int, container_height: int) -> Dict[str, Any]:
        return {"type": "absolute"}


class VerticalLayout(Layout):
    """Vertical box layout."""
    
    def __init__(self, spacing: int = 4, padding: int = 6, fill_x: bool = True):
        super().__init__(spacing, padding)
        self.fill_x = fill_x
    
    def apply(self, container) -> None:
        y = self.padding
        container_width = container.winfo_width()
        
        for widget in self._widgets:
            if not widget.winfo_viewable():
                continue
            
            widget.place(x=self.padding, y=y, 
                        width=container_width - 2 * self.padding if self.fill_x else None)
            
            h = widget.winfo_reqheight()
            y += h + self.spacing
    
    def calculate(self, container_width: int, container_height: int) -> Dict[str, Any]:
        total_height = 2 * self.padding
        for widget in self._widgets:
            total_height += getattr(widget, '_req_height', 20) + self.spacing
        
        return {
            "type": "vertical",
            "total_height": total_height,
            "width": container_width - 2 * self.padding
        }


class HorizontalLayout(Layout):
    """Horizontal box layout."""
    
    def __init__(self, spacing: int = 4, padding: int = 6, fill_y: bool = False):
        super().__init__(spacing, padding)
        self.fill_y = fill_y
    
    def apply(self, container) -> None:
        x = self.padding
        container_height = container.winfo_height()
        
        for widget in self._widgets:
            if not widget.winfo_viewable():
                continue
            
            h = container_height - 2 * self.padding if self.fill_y else None
            widget.place(x=x, y=self.padding, height=h)
            
            w = widget.winfo_reqwidth()
            x += w + self.spacing
    
    def calculate(self, container_width: int, container_height: int) -> Dict[str, Any]:
        total_width = 2 * self.padding
        for widget in self._widgets:
            total_width += getattr(widget, '_req_width', 80) + self.spacing
        
        return {
            "type": "horizontal",
            "total_width": total_width,
            "height": container_height - 2 * self.padding
        }


class GridLayout(Layout):
    """Grid-based layout with rows and columns."""
    
    def __init__(self, columns: int = 2, spacing: int = 4, padding: int = 6,
                 column_weights: Optional[List[int]] = None):
        super().__init__(spacing, padding)
        self.columns = columns
        self.column_weights = column_weights or [1] * columns
    
    def apply(self, container) -> None:
        container_width = container.winfo_width()
        col_width = (container_width - 2 * self.padding - (self.columns - 1) * self.spacing) / self.columns
        
        row = 0
        col = 0
        max_row_height = 0
        
        for widget in self._widgets:
            if not widget.winfo_viewable():
                continue
            
            x = self.padding + col * (col_width + self.spacing)
            y = self.padding + row * (max_row_height + self.spacing) if row > 0 else self.padding
            
            widget.place(x=x, y=y, width=int(col_width))
            
            h = widget.winfo_reqheight()
            if h > max_row_height:
                max_row_height = h
            
            col += 1
            if col >= self.columns:
                col = 0
                row += 1
                max_row_height = 0
    
    def calculate(self, container_width: int, container_height: int) -> Dict[str, Any]:
        col_width = (container_width - 2 * self.padding - (self.columns - 1) * self.spacing) / self.columns
        rows = (len(self._widgets) + self.columns - 1) // self.columns
        
        return {
            "type": "grid",
            "columns": self.columns,
            "rows": rows,
            "column_width": col_width
        }


class StackLayout(Layout):
    """Stack widgets on top of each other."""
    
    def __init__(self, align: str = "center"):
        super().__init__()
        self.align = align
    
    def apply(self, container) -> None:
        container_width = container.winfo_width()
        container_height = container.winfo_height()
        
        for widget in self._widgets:
            if not widget.winfo_viewable():
                continue
            
            w = widget.winfo_reqwidth()
            h = widget.winfo_reqheight()
            
            if self.align == "center":
                x = (container_width - w) // 2
                y = (container_height - h) // 2
            elif self.align == "topleft":
                x, y = 0, 0
            elif self.align == "topright":
                x = container_width - w
                y = 0
            elif self.align == "bottomleft":
                x = 0
                y = container_height - h
            elif self.align == "bottomright":
                x = container_width - w
                y = container_height - h
            else:
                x, y = 0, 0
            
            widget.place(x=x, y=y)
    
    def calculate(self, container_width: int, container_height: int) -> Dict[str, Any]:
        return {
            "type": "stack",
            "align": self.align
        }


class AnchorLayout(Layout):
    """Layout with anchor-based positioning."""
    
    def __init__(self, spacing: int = 4, padding: int = 6):
        super().__init__(spacing, padding)
        self._anchors: Dict = {}
    
    def set_anchor(self, widget, anchor: str) -> None:
        self._anchors[id(widget)] = anchor
        self.add_widget(widget)
    
    def apply(self, container) -> None:
        cw = container.winfo_width()
        ch = container.winfo_height()
        
        for widget in self._widgets:
            if not widget.winfo_viewable():
                continue
            
            anchor = self._anchors.get(id(widget), "nw")
            w = widget.winfo_reqwidth()
            h = widget.winfo_reqheight()
            
            x, y = self._calculate_position(anchor, cw, ch, w, h)
            widget.place(x=x, y=y)
    
    def _calculate_position(self, anchor: str, cw: int, ch: int, w: int, h: int) -> tuple:
        pad = self.padding
        
        if anchor == "n":
            return (cw - w) // 2, pad
        elif anchor == "s":
            return (cw - w) // 2, ch - h - pad
        elif anchor == "e":
            return cw - w - pad, (ch - h) // 2
        elif anchor == "w":
            return pad, (ch - h) // 2
        elif anchor == "ne":
            return cw - w - pad, pad
        elif anchor == "nw":
            return pad, pad
        elif anchor == "se":
            return cw - w - pad, ch - h - pad
        elif anchor == "sw":
            return pad, ch - h - pad
        elif anchor == "center":
            return (cw - w) // 2, (ch - h) // 2
        else:
            return pad, pad
    
    def calculate(self, container_width: int, container_height: int) -> Dict[str, Any]:
        return {"type": "anchor"}
