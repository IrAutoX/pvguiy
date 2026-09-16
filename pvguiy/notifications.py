import tkinter as tk


class Notification:
    def __init__(
        self,
        manager,
        title,
        message,
        kind="info",
        timeout=3500
    ):
        self.manager = manager
        self.scheme = manager.scheme
        self.width = 330
        self.height = 76
        self.timeout = timeout

        self.frame = tk.Frame(
            manager.root,
            bg=self.scheme.panel_dark,
            bd=0,
            highlightthickness=0
        )

        self.canvas = tk.Canvas(
            self.frame,
            width=self.width,
            height=self.height,
            bg=self.scheme.panel_dark,
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack()

        self.kind = kind

        colors = {
            "info": self.scheme.highlight,
            "success": self.scheme.success,
            "warning": self.scheme.warning,
            "error": self.scheme.error
        }

        accent = colors.get(
            kind,
            self.scheme.highlight
        )

        self.canvas.create_rectangle(
            0,
            0,
            self.width - 1,
            self.height - 1,
            fill=self.scheme.panel,
            outline=self.scheme.border_dark
        )

        self.canvas.create_line(
            1,
            1,
            self.width - 2,
            1,
            fill=self.scheme.border_light
        )

        self.canvas.create_line(
            1,
            1,
            1,
            self.height - 2,
            fill=self.scheme.border_light
        )

        self.canvas.create_line(
            1,
            self.height - 2,
            self.width - 2,
            self.height - 2,
            fill=self.scheme.black
        )

        self.canvas.create_line(
            self.width - 2,
            1,
            self.width - 2,
            self.height - 2,
            fill=self.scheme.black
        )

        self.canvas.create_rectangle(
            5,
            6,
            9,
            self.height - 7,
            fill=accent,
            outline=accent
        )

        self.canvas.create_text(
            18,
            17,
            text=title,
            anchor="w",
            fill=self.scheme.white,
            font=("MS Sans Serif", 8, "bold")
        )

        self.canvas.create_text(
            18,
            43,
            text=message,
            anchor="w",
            fill=self.scheme.text,
            font=("MS Sans Serif", 8),
            width=self.width - 55
        )

        self.canvas.create_text(
            self.width - 15,
            13,
            text="×",
            fill=self.scheme.text,
            font=("MS Sans Serif", 9, "bold")
        )

        self.canvas.bind(
            "<Button-1>",
            lambda e: self.close()
        )

    def show(self, y):
        x = self.manager.root.winfo_width()

        target = (
            self.manager.root.winfo_width()
            - self.width
            - 12
        )

        self.frame.place(
            x=x,
            y=y,
            width=self.width,
            height=self.height
        )

        self.animate(
            x,
            target
        )

    def animate(self, x, target):
        if not self.frame.winfo_exists():
            return

        if x <= target:
            self.frame.place_configure(
                x=target
            )

            self.manager.root.after(
                self.timeout,
                self.close
            )

            return

        x -= 25

        self.frame.place_configure(
            x=x
        )

        self.manager.root.after(
            10,
            lambda: self.animate(
                x,
                target
            )
        )

    def close(self):
        if self.frame.winfo_exists():
            self.frame.destroy()

        if self in self.manager.notifications:
            self.manager.notifications.remove(
                self
            )

        self.manager.reposition()


class NotificationManager:
    def __init__(
        self,
        root,
        scheme
    ):
        self.root = root
        self.scheme = scheme
        self.notifications = []

    def show(
        self,
        title,
        message,
        kind="info",
        timeout=3500
    ):
        notification = Notification(
            self,
            title,
            message,
            kind,
            timeout
        )

        self.notifications.insert(
            0,
            notification
        )

        self.reposition()

        return notification

    def info(
        self,
        title,
        message,
        timeout=3500
    ):
        return self.show(
            title,
            message,
            "info",
            timeout
        )

    def success(
        self,
        title,
        message,
        timeout=3500
    ):
        return self.show(
            title,
            message,
            "success",
            timeout
        )

    def warning(
        self,
        title,
        message,
        timeout=3500
    ):
        return self.show(
            title,
            message,
            "warning",
            timeout
        )

    def error(
        self,
        title,
        message,
        timeout=3500
    ):
        return self.show(
            title,
            message,
            "error",
            timeout
        )

    def reposition(self):
        y = 40

        for notification in self.notifications:
            if notification.frame.winfo_exists():
                notification.frame.place_configure(
                    x=(
                        self.root.winfo_width()
                        - notification.width
                        - 12
                    ),
                    y=y
                )

                y += notification.height + 8

    def set_scheme(self, scheme):
        self.scheme = scheme