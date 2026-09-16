class Border:
    def __init__(self, scheme):
        self.scheme = scheme

    def raised(self, canvas, x, y, w, h):
        canvas.create_rectangle(
            x,
            y,
            x + w,
            y + h,
            fill=self.scheme.panel,
            outline=self.scheme.border_dark
        )

        canvas.create_line(
            x + 1,
            y + 1,
            x + w - 2,
            y + 1,
            fill=self.scheme.border_light
        )

        canvas.create_line(
            x + 1,
            y + 1,
            x + 1,
            y + h - 2,
            fill=self.scheme.border_light
        )

        canvas.create_line(
            x + 1,
            y + h - 2,
            x + w - 2,
            y + h - 2,
            fill=self.scheme.black
        )

        canvas.create_line(
            x + w - 2,
            y + 1,
            x + w - 2,
            y + h - 2,
            fill=self.scheme.black
        )

    def sunken(self, canvas, x, y, w, h):
        canvas.create_rectangle(
            x,
            y,
            x + w,
            y + h,
            fill=self.scheme.input,
            outline=self.scheme.border_dark
        )

        canvas.create_line(
            x + 1,
            y + 1,
            x + w - 2,
            y + 1,
            fill=self.scheme.black
        )

        canvas.create_line(
            x + 1,
            y + 1,
            x + 1,
            y + h - 2,
            fill=self.scheme.black
        )

        canvas.create_line(
            x + 1,
            y + h - 2,
            x + w - 2,
            y + h - 2,
            fill=self.scheme.border_light
        )

        canvas.create_line(
            x + w - 2,
            y + 1,
            x + w - 2,
            y + h - 2,
            fill=self.scheme.border_light
        )