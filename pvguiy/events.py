"""PVGUIY Event System - Custom event handling and dispatch."""

from typing import Callable, Dict, List, Any, Optional
from pvguiy.exceptions import EventError


class Event:
    """Represents an event with type and data."""
    
    def __init__(self, event_type: str, data: Any = None, source: Any = None):
        self.type = event_type
        self.data = data
        self.source = source
        self._stopped = False
    
    def stop_propagation(self) -> None:
        """Stop event propagation."""
        self._stopped = True
    
    @property
    def stopped(self) -> bool:
        return self._stopped
    
    def __repr__(self) -> str:
        return f"Event(type='{self.type}', data={self.data})"


class EventEmitter:
    """Mixin class for objects that emit events."""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._once_handlers: Dict[str, List[Callable]] = {}
    
    def on(self, event_type: str, handler: Callable) -> 'EventEmitter':
        """Register an event handler."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        return self
    
    def off(self, event_type: str, handler: Optional[Callable] = None) -> 'EventEmitter':
        """Remove an event handler."""
        if event_type in self._handlers:
            if handler is None:
                self._handlers[event_type] = []
            elif handler in self._handlers[event_type]:
                self._handlers[event_type].remove(handler)
        return self
    
    def once(self, event_type: str, handler: Callable) -> 'EventEmitter':
        """Register a one-time event handler."""
        if event_type not in self._once_handlers:
            self._once_handlers[event_type] = []
        self._once_handlers[event_type].append(handler)
        return self
    
    def emit(self, event_type: str, data: Any = None) -> 'EventEmitter':
        """Emit an event."""
        event = Event(event_type, data, self)
        
        # Call regular handlers
        if event_type in self._handlers:
            for handler in list(self._handlers[event_type]):
                if event.stopped:
                    break
                try:
                    handler(event)
                except Exception as e:
                    pass  # Silently ignore handler errors
        
        # Call once handlers and remove them
        if event_type in self._once_handlers:
            handlers = self._once_handlers.pop(event_type, [])
            for handler in handlers:
                if event.stopped:
                    break
                try:
                    handler(event)
                except Exception as e:
                    pass
        
        return self
    
    def has_listener(self, event_type: str) -> bool:
        """Check if there are any listeners for an event type."""
        return (event_type in self._handlers and len(self._handlers[event_type]) > 0) or \
               (event_type in self._once_handlers and len(self._once_handlers[event_type]) > 0)
    
    def clear(self) -> None:
        """Clear all event handlers."""
        self._handlers.clear()
        self._once_handlers.clear()


class EventSystem:
    """Global event system for application-wide events."""
    
    _instance: Optional['EventSystem'] = None
    
    def __new__(cls) -> 'EventSystem':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._channels: Dict[str, EventEmitter] = {}
        self._initialized = True
    
    def channel(self, name: str) -> EventEmitter:
        """Get or create an event channel."""
        if name not in self._channels:
            self._channels[name] = EventEmitter()
        return self._channels[name]
    
    def on(self, channel: str, event_type: str, handler: Callable) -> 'EventSystem':
        """Subscribe to an event on a channel."""
        self.channel(channel).on(event_type, handler)
        return self
    
    def off(self, channel: str, event_type: str, handler: Optional[Callable] = None) -> 'EventSystem':
        """Unsubscribe from an event on a channel."""
        self.channel(channel).off(event_type, handler)
        return self
    
    def emit(self, channel: str, event_type: str, data: Any = None) -> 'EventSystem':
        """Emit an event on a channel."""
        self.channel(channel).emit(event_type, data)
        return self
    
    def clear(self) -> None:
        """Clear all channels."""
        self._channels.clear()


# Common event types
EVENT_CLICK = "click"
EVENT_DOUBLE_CLICK = "double_click"
EVENT_MOUSE_DOWN = "mouse_down"
EVENT_MOUSE_UP = "mouse_up"
EVENT_MOUSE_MOVE = "mouse_move"
EVENT_MOUSE_ENTER = "mouse_enter"
EVENT_MOUSE_LEAVE = "mouse_leave"
EVENT_KEY_DOWN = "key_down"
EVENT_KEY_UP = "key_up"
EVENT_FOCUS = "focus"
EVENT_BLUR = "blur"
EVENT_CHANGE = "change"
EVENT_SUBMIT = "submit"
EVENT_CLOSE = "close"
EVENT_RESIZE = "resize"
EVENT_MOVE = "move"
EVENT_SHOW = "show"
EVENT_HIDE = "hide"
EVENT_ENABLE = "enable"
EVENT_DISABLE = "disable"
EVENT_DESTROY = "destroy"
EVENT_HOVER = "hover"
EVENT_ARMED = "armed"
EVENT_PRESSED = "pressed"
