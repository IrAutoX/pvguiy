import tkinter as tk


class Panel(tk.Frame):
    def __init__(self, master=None, scheme=None, **kwargs):
        self.scheme = scheme or getattr(
            master,
            "scheme",
            None
        )

        bg = kwargs.pop(
            "bg",
            self.scheme.panel if self.scheme else "#444444"
        )

        super().__init__(
            master,
            bg=bg,
            bd=0,
            highlightthickness=0,
            **kwargs
        )

        self.children_panels = []

        if master is not None and hasattr(
            master,
            "children_panels"
        ):
            master.children_panels.append(self)

    def set_scheme(self, scheme):
        self.scheme = scheme
        self.configure(bg=scheme.panel)

        for child in self.winfo_children():
            if hasattr(child, "set_scheme"):
                child.set_scheme(scheme)


class Frame(Panel):
    def __init__(
        self,
        master=None,
        title=None,
        width=300,
        height=200,
        scheme=None,
        **kwargs
    ):
        super().__init__(
            master,
            scheme=scheme,
            width=width,
            height=height,
            **kwargs
        )

        self.pack_propagate(False)

        self.title = title

        self.header = tk.Frame(
            self,
            bg=self.scheme.panel
        )
        self.header.pack(
            fill="x",
            padx=10,
            pady=(7, 0)
        )

        if title:
            self.title_label = tk.Label(
                self.header,
                text=title,
                bg=self.scheme.panel,
                fg=self.scheme.white,
                font=("MS Sans Serif", 8, "bold")
            )
            self.title_label.pack(
                side="left"
            )

        self.content = tk.Frame(
            self,
            bg=self.scheme.panel
        )
        self.content.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=8
        )

    def set_scheme(self, scheme):
        self.scheme = scheme

        self.configure(
            bg=scheme.panel
        )

        self.header.configure(
            bg=scheme.panel
        )

        self.content.configure(
            bg=scheme.panel
        )

        if hasattr(self, "title_label"):
            self.title_label.configure(
                bg=scheme.panel,
                fg=scheme.white
            )


class Label(tk.Label):
    def __init__(
        self,
        master,
        text="",
        scheme=None,
        **kwargs
    ):
        self.scheme = scheme or master.scheme

        super().__init__(
            master,
            text=text,
            bg=kwargs.pop(
                "bg",
                self.scheme.panel
            ),
            fg=kwargs.pop(
                "fg",
                self.scheme.text
            ),
            font=kwargs.pop(
                "font",
                ("MS Sans Serif", 8)
            ),
            **kwargs
        )

    def set_scheme(self, scheme):
        self.scheme = scheme

        self.configure(
            bg=scheme.panel,
            fg=scheme.text
        )


class Scheme:
    def __init__(self, theme):
        self.theme = theme

    def __getattr__(self, name):
        return getattr(
            self.theme,
            name
        )