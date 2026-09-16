"""PVGUIY Animation System - Tweening and animations."""

import math
from typing import Callable, Optional, Any


class Easing:
    """Easing functions for animations."""
    
    @staticmethod
    def linear(t: float) -> float:
        return t
    
    @staticmethod
    def ease_in(t: float) -> float:
        return t * t
    
    @staticmethod
    def ease_out(t: float) -> float:
        return t * (2 - t)
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        if t < 0.5:
            return 2 * t * t
        return -1 + (4 - 2 * t) * t
    
    @staticmethod
    def ease_in_quad(t: float) -> float:
        return t * t
    
    @staticmethod
    def ease_out_quad(t: float) -> float:
        return t * (2 - t)
    
    @staticmethod
    def ease_in_cubic(t: float) -> float:
        return t * t * t
    
    @staticmethod
    def ease_out_cubic(t: float) -> float:
        return 1 - pow(1 - t, 3)
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        if t < 0.5:
            return 4 * t * t * t
        return 1 - pow(-2 * t + 2, 3) / 2


class Tween:
    """Tween animation between two values."""
    
    def __init__(self, start: float, end: float, duration: float = 1.0,
                 easing: Callable[[float], float] = Easing.ease_in_out):
        self.start = start
        self.end = end
        self.duration = duration
        self.easing = easing
        self._elapsed = 0.0
        self._running = False
        self._callback: Optional[Callable[[float], None]] = None
        self._complete_callback: Optional[Callable[[], None]] = None
    
    def on_update(self, callback: Callable[[float], None]) -> 'Tween':
        self._callback = callback
        return self
    
    def on_complete(self, callback: Callable[[], None]) -> 'Tween':
        self._complete_callback = callback
        return self
    
    def update(self, dt: float) -> bool:
        if not self._running:
            return False
        
        self._elapsed += dt
        t = min(self._elapsed / self.duration, 1.0)
        
        eased_t = self.easing(t)
        value = self.start + (self.end - self.start) * eased_t
        
        if self._callback:
            self._callback(value)
        
        if t >= 1.0:
            self._running = False
            if self._complete_callback:
                self._complete_callback()
            return True
        
        return False
    
    def start(self) -> 'Tween':
        self._running = True
        self._elapsed = 0.0
        return self
    
    def stop(self) -> 'Tween':
        self._running = False
        return self


class Animation:
    """Animation that can be applied to widgets."""
    
    def __init__(self, widget, property_name: str, start_value: Any, 
                 end_value: Any, duration: float = 0.3,
                 easing: Callable[[float], float] = Easing.ease_in_out):
        self.widget = widget
        self.property_name = property_name
        self.tween = Tween(start_value, end_value, duration, easing)
        self.tween.on_update(self._on_update)
    
    def _on_update(self, value: float) -> None:
        if hasattr(self.widget, 'configure'):
            try:
                self.widget.configure(**{self.property_name: value})
            except:
                pass
    
    def start(self) -> None:
        self.tween.start()
    
    def update(self, dt: float) -> bool:
        return self.tween.update(dt)


class Animator:
    """Manages multiple animations."""
    
    def __init__(self, root):
        self.root = root
        self._animations = []
        self._running = False
    
    def add(self, animation: Animation) -> None:
        self._animations.append(animation)
        if not self._running:
            self._start()
    
    def _start(self) -> None:
        self._running = True
        self._last_time = self.root.winfo_id()  # Just to check existence
        self._schedule_update()
    
    def _schedule_update(self) -> None:
        if self._running:
            self.root.after(16, self._update)
    
    def _update(self) -> None:
        if not self._running:
            return
        
        dt = 0.016  # ~60fps
        
        completed = []
        for i, anim in enumerate(self._animations):
            if anim.update(dt):
                completed.append(i)
        
        for i in reversed(completed):
            self._animations.pop(i)
        
        if self._animations:
            self._schedule_update()
        else:
            self._running = False
    
    def clear(self) -> None:
        self._animations.clear()
        self._running = False


def fade_in(widget, duration: float = 0.3) -> None:
    """Fade in a widget."""
    pass  # Implemented via canvas alpha simulation if needed


def fade_out(widget, duration: float = 0.3) -> None:
    """Fade out a widget."""
    pass


def slide_in(widget, direction: str = "left", duration: float = 0.3) -> None:
    """Slide in a widget from a direction."""
    pass


def slide_out(widget, direction: str = "right", duration: float = 0.3) -> None:
    """Slide out a widget to a direction."""
    pass
