class Theme:
    def __init__(
        self,
        name,
        background,
        background_dark,
        background_light,
        panel,
        panel_dark,
        text,
        text_dark,
        highlight,
        accent,
        black,
        white,
        border_light,
        border_dark,
        input_bg,
        console_bg,
        error,
        success,
        warning
    ):
        self.name = name
        self.background = background
        self.background_dark = background_dark
        self.background_light = background_light
        self.panel = panel
        self.panel_dark = panel_dark
        self.text = text
        self.text_dark = text_dark
        self.highlight = highlight
        self.accent = accent
        self.black = black
        self.white = white
        self.border_light = border_light
        self.border_dark = border_dark
        self.input = input_bg
        self.console = console_bg
        self.error = error
        self.success = success
        self.warning = warning


GREEN = Theme(
    "green",
    "#4B5A45",
    "#30392D",
    "#68785F",
    "#596952",
    "#3B4637",
    "#E2E5D8",
    "#11150F",
    "#82966F",
    "#9BAD78",
    "#11140F",
    "#E7E9DD",
    "#8A9980",
    "#252B22",
    "#20261E",
    "#10140F",
    "#B94A48",
    "#75995B",
    "#B29A56"
)

ORANGE = Theme(
    "orange",
    "#5A4936",
    "#382C21",
    "#786047",
    "#66523E",
    "#443526",
    "#EEE2D2",
    "#17110C",
    "#A8784D",
    "#D38B45",
    "#15100C",
    "#F1E6D8",
    "#9A816A",
    "#30251C",
    "#241B14",
    "#120E0A",
    "#BE554C",
    "#789B5E",
    "#B79855"
)

BLACK = Theme(
    "black",
    "#303030",
    "#191919",
    "#444444",
    "#383838",
    "#242424",
    "#E5E5E5",
    "#090909",
    "#555555",
    "#9A9A9A",
    "#050505",
    "#F2F2F2",
    "#707070",
    "#121212",
    "#171717",
    "#080808",
    "#B84C4C",
    "#72975D",
    "#A68D51"
)


THEMES = {
    "green": GREEN,
    "orange": ORANGE,
    "black": BLACK
}


def get_theme(name):
    name = str(name).lower()

    if name not in THEMES:
        raise ValueError(
            f"Unknown VGUI theme: {name}"
        )

    return THEMES[name]