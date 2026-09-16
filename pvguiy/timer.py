"""PVGUIY Timer System - Scheduling and timing utilities."""

import time
from typing import Callable, Optional


class Timer:
    """One-shot timer using Tkinter's after method."""
    
    def __init__(self, root):
        self.root = root
        self._job_id: Optional[int] = None
    
    @classmethod
    def after(cls, root, delay_ms: int, callback: Callable) -> 'Timer':
        """Schedule a callback after delay_ms milliseconds."""
        timer = cls(root)
        timer._job_id = root.after(delay_ms, callback)
        return timer
    
    @staticmethod
    def after_ms(delay_ms: int, callback: Callable) -> None:
        """Static method to schedule a callback."""
        import tkinter as tk
        temp_root = tk.Tk()
        temp_root.withdraw()
        temp_root.after(delay_ms, lambda: [callback(), temp_root.destroy()])
        temp_root.mainloop()
    
    def cancel(self) -> None:
        if self._job_id is not None:
            try:
                self.root.after_cancel(self._job_id)
            except:
                pass
            self._job_id = None


class RepeatingTimer:
    """Repeating timer that calls callback at intervals."""
    
    def __init__(self, root, interval_ms: int, callback: Callable):
        self.root = root
        self.interval_ms = interval_ms
        self.callback = callback
        self._running = False
        self._job_id: Optional[int] = None
    
    def start(self) -> 'RepeatingTimer':
        self._running = True
        self._schedule()
        return self
    
    def _schedule(self) -> None:
        if self._running:
            self._job_id = self.root.after(self.interval_ms, self._on_tick)
    
    def _on_tick(self) -> None:
        if self._running:
            try:
                self.callback()
            except:
                pass
            self._schedule()
    
    def stop(self) -> None:
        self._running = False
        if self._job_id is not None:
            try:
                self.root.after_cancel(self._job_id)
            except:
                pass
            self._job_id = None
    
    @property
    def running(self) -> bool:
        return self._running


class DelayedCall:
    """A delayed function call that can be cancelled."""
    
    def __init__(self, root, delay_ms: int, callback: Callable, *args, **kwargs):
        self.root = root
        self.delay_ms = delay_ms
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self._job_id: Optional[int] = None
        self._called = False
        self._schedule()
    
    def _schedule(self) -> None:
        self._job_id = self.root.after(self.delay_ms, self._execute)
    
    def _execute(self) -> None:
        if not self._called:
            self._called = True
            try:
                self.callback(*self.args, **self.kwargs)
            except:
                pass
    
    def cancel(self) -> None:
        if not self._called and self._job_id is not None:
            try:
                self.root.after_cancel(self._job_id)
            except:
                pass
            self._called = True
    
    @property
    def called(self) -> bool:
        return self._called


class Clock:
    """Simple clock for measuring elapsed time."""
    
    def __init__(self):
        self._start_time: Optional[float] = None
        self._elapsed: float = 0.0
        self._paused: bool = False
    
    def start(self) -> 'Clock':
        self._start_time = time.time()
        self._paused = False
        return self
    
    def stop(self) -> float:
        if self._start_time and not self._paused:
            self._elapsed += time.time() - self._start_time
        self._start_time = None
        return self._elapsed
    
    def pause(self) -> None:
        if self._start_time and not self._paused:
            self._elapsed += time.time() - self._start_time
            self._paused = True
            self._start_time = None
    
    def resume(self) -> None:
        if self._paused:
            self._start_time = time.time()
            self._paused = False
    
    def reset(self) -> 'Clock':
        self._start_time = None
        self._elapsed = 0.0
        self._paused = False
        return self
    
    @property
    def elapsed(self) -> float:
        if self._paused:
            return self._elapsed
        if self._start_time:
            return self._elapsed + (time.time() - self._start_time)
        return self._elapsed
    
    @property
    def elapsed_ms(self) -> int:
        return int(self.elapsed * 1000)
