import tkinter as tk

from .themes import get_theme
from .core import Scheme
from .notifications import NotificationManager


class VGUI:
    def __init__(
        self,
        title="VGUI Application",
        width=900,
        height=600,
        theme="green",
        borderless=True
    ):
        self.root = tk.Tk()

        self.scheme = Scheme(
            get_theme(theme)
        )

        self.root.title(title)

        if borderless:
            self.root.overrideredirect(True)

        self.root.configure(
            bg=self.scheme.background_dark
        )

        self.width = width
        self.height = height

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        x = (sw - width) // 2
        y = (sh - height) // 2

        self.root.geometry(
            f"{width}x{height}+{x}+{y}"
        )

        self.drag_x = 0
        self.drag_y = 0

        self.notifications = NotificationManager(
            self.root,
            self.scheme
        )

        self.titlebar = None
        self.content = None

        self._build()

    def _build(self):
        self.outer = tk.Frame(
            self.root,
            bg=self.scheme.border_dark,
            bd=0
        )

        self.outer.pack(
            fill="both",
            expand=True
        )

        self.titlebar = tk.Frame(
            self.outer,
            bg=self.scheme.background_dark,
            height=30
        )

        self.titlebar.pack(
            fill="x"
        )

        self.titlebar.pack_propagate(
            False
        )

        self.titlebar.bind(
            "<ButtonPress-1>",
            self._drag_start
        )

        self.titlebar.bind(
            "<B1-Motion>",
            self._drag
        )

        self.title_label = tk.Label(
            self.titlebar,
            text="VGUI",
            bg=self.scheme.background_dark,
            fg=self.scheme.white,
            font=("MS Sans Serif", 8, "bold")
        )

        self.title_label.pack(
            side="left",
            padx=9
        )

        self.close = tk.Label(
            self.titlebar,
            text="×",
            width=4,
            bg=self.scheme.background_dark,
            fg=self.scheme.text,
            font=("MS Sans Serif", 10, "bold")
        )

        self.close.pack(
            side="right",
            fill="y"
        )

        self.close.bind(
            "<Button-1>",
            lambda e: self.destroy()
        )

        self.close.bind(
            "<Enter>",
            lambda e: self.close.configure(
                bg=self.scheme.error,
                fg=self.scheme.white
            )
        )

        self.close.bind(
            "<Leave>",
            lambda e: self.close.configure(
                bg=self.scheme.background_dark,
                fg=self.scheme.text
            )
        )

        self.minimize = tk.Label(
            self.titlebar,
            text="—",
            width=4,
            bg=self.scheme.background_dark,
            fg=self.scheme.text,
            font=("MS Sans Serif", 8)
        )

        self.minimize.pack(
            side="right",
            fill="y"
        )

        self.minimize.bind(
            "<Button-1>",
            lambda e: self._minimize()
        )

        self.content = tk.Frame(
            self.outer,
            bg=self.scheme.background
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=2,
            pady=(0, 2)
        )

    def _drag_start(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def _drag(self, event):
        x = (
            self.root.winfo_x()
            + event.x
            - self.drag_x
        )

        y = (
            self.root.winfo_y()
            + event.y
            - self.drag_y
        )

        self.root.geometry(
            f"+{x}+{y}"
        )

    def _minimize(self):
        self.root.overrideredirect(False)
        self.root.iconify()

        self.root.bind(
            "<Map>",
            self._restore,
            add="+"
        )

    def _restore(self, event=None):
        if self.root.state() == "normal":
            self.root.overrideredirect(True)

    def set_title(self, title):
        self.title_label.configure(
            text=title
        )

    def set_theme(self, theme):
        self.scheme = Scheme(
            get_theme(theme)
        )

        self.root.configure(
            bg=self.scheme.background_dark
        )

        self.outer.configure(
            bg=self.scheme.border_dark
        )

        self.titlebar.configure(
            bg=self.scheme.background_dark
        )

        self.title_label.configure(
            bg=self.scheme.background_dark,
            fg=self.scheme.white
        )

        self.close.configure(
            bg=self.scheme.background_dark,
            fg=self.scheme.text
        )

        self.minimize.configure(
            bg=self.scheme.background_dark,
            fg=self.scheme.text
        )

        self.content.configure(
            bg=self.scheme.background
        )

        self.notifications.set_scheme(
            self.scheme
        )

        self._update_widgets(
            self.content
        )

    def _update_widgets(self, parent):
        for child in parent.winfo_children():
            if hasattr(child, "set_scheme"):
                child.set_scheme(
                    self.scheme
                )

            if child.winfo_children():
                self._update_widgets(
                    child
                )

    def destroy(self):
        self.root.destroy()

    def mainloop(self):
        self.root.mainloop()