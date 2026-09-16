import tkinter as tk

from .core import Panel
from .borders import Border


class Button(tk.Canvas):
    def __init__(
        self,
        master,
        text,
        command=None,
        width=120,
        height=27,
        scheme=None
    ):
        self.scheme = scheme or master.scheme

        super().__init__(
            master,
            width=width,
            height=height,
            bg=self.scheme.panel,
            highlightthickness=0,
            bd=0
        )

        self.text = text
        self.command = command
        self.state = "normal"
        self.enabled = True

        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<ButtonPress-1>", self._press)
        self.bind("<ButtonRelease-1>", self._release)

        self.draw()

    def draw(self):
        self.delete("all")

        w = int(self["width"])
        h = int(self["height"])

        if not self.enabled:
            fill = self.scheme.panel_dark
        elif self.state == "pressed":
            fill = self.scheme.background_dark
        elif self.state == "armed":
            fill = self.scheme.highlight
        else:
            fill = self.scheme.panel

        self.create_rectangle(
            0,
            0,
            w - 1,
            h - 1,
            fill=fill,
            outline=self.scheme.border_dark
        )

        if self.state == "pressed":
            light = self.scheme.border_dark
            dark = self.scheme.border_light
            ox = 1
            oy = 1
        else:
            light = self.scheme.border_light
            dark = self.scheme.black
            ox = 0
            oy = 0

        self.create_line(
            1,
            1,
            w - 2,
            1,
            fill=light
        )

        self.create_line(
            1,
            1,
            1,
            h - 2,
            fill=light
        )

        self.create_line(
            1,
            h - 2,
            w - 2,
            h - 2,
            fill=dark
        )

        self.create_line(
            w - 2,
            1,
            w - 2,
            h - 2,
            fill=dark
        )

        self.create_text(
            w // 2 + ox,
            h // 2 + oy,
            text=self.text,
            fill=(
                self.scheme.text
                if self.enabled
                else "#777777"
            ),
            font=("MS Sans Serif", 8)
        )

    def _enter(self, event):
        if self.enabled:
            self.state = "armed"
            self.draw()

    def _leave(self, event):
        if self.enabled:
            self.state = "normal"
            self.draw()

    def _press(self, event):
        if self.enabled:
            self.state = "pressed"
            self.draw()

    def _release(self, event):
        if not self.enabled:
            return

        w = int(self["width"])
        h = int(self["height"])

        inside = (
            0 <= event.x < w and
            0 <= event.y < h
        )

        self.state = (
            "armed"
            if inside
            else "normal"
        )

        self.draw()

        if inside and self.command:
            self.command()

    def configure_text(self, text):
        self.text = text
        self.draw()

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.state = "normal"
        self.draw()

    def set_scheme(self, scheme):
        self.scheme = scheme
        self.configure(
            bg=scheme.panel
        )
        self.draw()


class CheckButton(tk.Canvas):
    def __init__(
        self,
        master,
        text,
        variable=None,
        command=None,
        scheme=None
    ):
        self.scheme = scheme or master.scheme

        super().__init__(
            master,
            width=210,
            height=22,
            bg=self.scheme.panel,
            highlightthickness=0,
            bd=0
        )

        self.text = text
        self.variable = variable or tk.BooleanVar()
        self.command = command
        self.hovered = False

        self.bind(
            "<Button-1>",
            self._toggle
        )
        self.bind(
            "<Enter>",
            self._enter
        )
        self.bind(
            "<Leave>",
            self._leave
        )

        self.draw()

    def draw(self):
        self.delete("all")

        self.create_rectangle(
            2,
            4,
            16,
            18,
            fill=self.scheme.input,
            outline=self.scheme.border_dark
        )

        self.create_line(
            3,
            5,
            15,
            5,
            fill=self.scheme.black
        )

        self.create_line(
            3,
            5,
            3,
            17,
            fill=self.scheme.black
        )

        self.create_line(
            3,
            17,
            15,
            17,
            fill=self.scheme.border_light
        )

        self.create_line(
            15,
            5,
            15,
            17,
            fill=self.scheme.border_light
        )

        if self.variable.get():
            self.create_line(
                5,
                11,
                8,
                15,
                fill=self.scheme.accent,
                width=2
            )

            self.create_line(
                8,
                15,
                14,
                7,
                fill=self.scheme.accent,
                width=2
            )

        self.create_text(
            24,
            11,
            text=self.text,
            anchor="w",
            fill=(
                self.scheme.white
                if self.hovered
                else self.scheme.text
            ),
            font=("MS Sans Serif", 8)
        )

    def _toggle(self, event):
        self.variable.set(
            not self.variable.get()
        )

        self.draw()

        if self.command:
            self.command(
                self.variable.get()
            )

    def _enter(self, event):
        self.hovered = True
        self.draw()

    def _leave(self, event):
        self.hovered = False
        self.draw()

    def set_scheme(self, scheme):
        self.scheme = scheme
        self.configure(
            bg=scheme.panel
        )
        self.draw()


class TextEntry(Panel):
    def __init__(
        self,
        master,
        value="",
        width=300,
        scheme=None
    ):
        self.scheme = scheme or master.scheme

        super().__init__(
            master,
            scheme=self.scheme,
            width=width,
            height=24
        )

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=24,
            bg=self.scheme.input,
            highlightthickness=0,
            bd=0
        )

        self.canvas.place(
            x=0,
            y=0
        )

        Border(self.scheme).sunken(
            self.canvas,
            0,
            0,
            width - 1,
            23
        )

        self.entry = tk.Entry(
            self,
            bg=self.scheme.input,
            fg=self.scheme.white,
            insertbackground=self.scheme.white,
            selectbackground=self.scheme.highlight,
            selectforeground=self.scheme.white,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("MS Sans Serif", 8)
        )

        self.entry.place(
            x=5,
            y=4,
            width=width - 10,
            height=16
        )

        self.entry.insert(
            0,
            value
        )

    def get(self):
        return self.entry.get()

    def set(self, value):
        self.entry.delete(
            0,
            "end"
        )
        self.entry.insert(
            0,
            value
        )

    def focus(self):
        self.entry.focus_set()

    def set_scheme(self, scheme):
        self.scheme = scheme

        self.configure(
            bg=scheme.panel
        )

        self.canvas.configure(
            bg=scheme.input
        )

        self.entry.configure(
            bg=scheme.input,
            fg=scheme.white,
            insertbackground=scheme.white,
            selectbackground=scheme.highlight,
            selectforeground=scheme.white
        )

        self.canvas.delete("all")

        Border(scheme).sunken(
            self.canvas,
            0,
            0,
            int(self["width"]) - 1,
            23
        )


class Console(Panel):
    def __init__(
        self,
        master,
        scheme=None
    ):
        self.scheme = scheme or master.scheme

        super().__init__(
            master,
            scheme=self.scheme
        )

        self.text = tk.Text(
            self,
            bg=self.scheme.console,
            fg=self.scheme.text,
            insertbackground=self.scheme.white,
            selectbackground=self.scheme.highlight,
            relief="flat",
            bd=0,
            wrap="none",
            font=("Courier New", 8),
            padx=6,
            pady=5
        )

        self.scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.text.yview,
            troughcolor=self.scheme.background_dark,
            bg=self.scheme.panel,
            activebackground=self.scheme.highlight,
            relief="flat",
            bd=0,
            width=12
        )

        self.text.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.text.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.text.tag_configure(
            "normal",
            foreground=self.scheme.text
        )

        self.text.tag_configure(
            "info",
            foreground=self.scheme.highlight
        )

        self.text.tag_configure(
            "success",
            foreground=self.scheme.success
        )

        self.text.tag_configure(
            "error",
            foreground=self.scheme.error
        )

    def write(
        self,
        text,
        tag="normal"
    ):
        self.text.insert(
            "end",
            text,
            tag
        )

        self.text.see("end")

    def clear(self):
        self.text.delete(
            "1.0",
            "end"
        )

    def set_scheme(self, scheme):
        self.scheme = scheme

        self.configure(
            bg=scheme.panel
        )

        self.text.configure(
            bg=scheme.console,
            fg=scheme.text,
            insertbackground=scheme.white,
            selectbackground=scheme.highlight
        )

        self.scrollbar.configure(
            troughcolor=scheme.background_dark,
            bg=scheme.panel,
            activebackground=scheme.highlight
        )

        self.text.tag_configure(
            "normal",
            foreground=scheme.text
        )

        self.text.tag_configure(
            "info",
            foreground=scheme.highlight
        )

        self.text.tag_configure(
            "success",
            foreground=scheme.success
        )

        self.text.tag_configure(
            "error",
            foreground=scheme.error
        )