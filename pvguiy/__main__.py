"""PVGUIY - Classic GoldSrc-inspired Python GUI Framework."""

if __name__ == "__main__":
    import argparse
    from pvguiy import VGUI, Window, Panel, Label, Button, CheckButton, RadioButton
    from pvguiy import TextEntry, PasswordEntry, TextArea, Console, ProgressBar
    from pvguiy import Slider, ListBox, ComboBox, TabControl, Tab
    from pvguiy import MenuBar, Menu, MenuItem, Separator
    from pvguiy import GroupBox, StatusBar, ToolTip
    from pvguiy import GREEN, ORANGE, BLACK
    
    parser = argparse.ArgumentParser(description="PVGUIY Showcase Application")
    parser.add_argument("--theme", default="green", choices=["green", "orange", "black"],
                        help="Theme to use (default: green)")
    args = parser.parse_args()
    
    app = VGUI(title="PVGUIY Studio", theme=args.theme, width=900, height=650)
    window = Window(app, title="PVGUIY Studio", width=900, height=650)
    
    # Menu bar
    menubar = MenuBar(window)
    file_menu = Menu("File")
    file_menu.add_item("New", command=lambda: app.notify.info("New", "Creating new file"))
    file_menu.add_item("Open", command=lambda: app.notify.info("Open", "Opening file"), shortcut="Ctrl+O")
    file_menu.add_separator()
    file_menu.add_item("Exit", command=app.destroy)
    
    edit_menu = Menu("Edit")
    edit_menu.add_item("Cut", shortcut="Ctrl+X")
    edit_menu.add_item("Copy", shortcut="Ctrl+C")
    edit_menu.add_item("Paste", shortcut="Ctrl+V")
    
    help_menu = Menu("Help")
    help_menu.add_item("About", command=lambda: app.show_about("PVGUIY", "1.0.0", "Classic GoldSrc-inspired GUI Framework"))
    
    menubar.add_menu(file_menu)
    menubar.add_menu(edit_menu)
    menubar.add_menu(help_menu)
    
    # Main panel with layout
    main_panel = Panel(window)
    main_panel.place(x=0, y=30, relwidth=1.0, relheight=1.0)
    
    # Left panel with controls
    left_panel = Panel(main_panel)
    left_panel.place(x=8, y=8, width=280, height=580)
    
    # Controls group
    controls_group = GroupBox(left_panel, text="Controls")
    controls_group.place(x=8, y=8, width=264, height=280)
    
    cp = controls_group.content
    
    # Buttons
    btn1 = Button(cp, text="Primary Button", command=lambda: app.notify.success("Success", "Button clicked!"))
    btn1.place(x=10, y=20, width=120)
    
    btn2 = Button(cp, text="Secondary", command=lambda: app.notify.info("Info", "Secondary button"))
    btn2.place(x=140, y=20, width=110)
    
    btn3 = Button(cp, text="Disabled", command=lambda: None)
    btn3.place(x=10, y=55, width=120)
    btn3.set_enabled(False)
    
    # Checkboxes
    chk1 = CheckButton(cp, text="Option 1", command=lambda v: app.console.info(f"Option 1: {v}"))
    chk1.place(x=10, y=90)
    
    chk2 = CheckButton(cp, text="Option 2", command=lambda v: app.console.info(f"Option 2: {v}"))
    chk2.place(x=10, y=115)
    
    chk3 = CheckButton(cp, text="Option 3", command=lambda v: app.console.info(f"Option 3: {v}"))
    chk3.place(x=10, y=140)
    
    # Radio buttons
    radio_label = Label(cp, text="Radio Group:", bg=cp.cget("bg"))
    radio_label.place(x=10, y=175)
    
    radio1 = RadioButton(cp, text="First", group="radio1")
    radio1.place(x=10, y=195)
    
    radio2 = RadioButton(cp, text="Second", group="radio1")
    radio2.place(x=10, y=220)
    
    radio3 = RadioButton(cp, text="Third", group="radio1")
    radio3.place(x=10, y=245)
    
    # Text entries group
    entries_group = GroupBox(left_panel, text="Text Entries")
    entries_group.place(x=8, y=295, width=264, height=140)
    
    ep = entries_group.content
    
    entry1 = TextEntry(ep, value="Standard input", width=240)
    entry1.place(x=10, y=20)
    
    entry2 = PasswordEntry(ep, value="secret", width=240)
    entry2.place(x=10, y=55)
    
    textarea_label = Label(ep, text="Multi-line:", bg=ep.cget("bg"))
    textarea_label.place(x=10, y=90)
    
    textarea = TextArea(ep, width=240, height=60)
    textarea.place(x=10, y=110)
    
    # Right panel
    right_panel = Panel(main_panel)
    right_panel.place(x=296, y=8, relwidth=1.0, relheight=1.0)
    
    # Tabs
    tabs = TabControl(right_panel)
    tabs.place(x=8, y=8, relwidth=1.0, relheight=0.6)
    
    tab1_content = Panel(tabs)
    tab1 = tabs.add_tab("General", tab1_content)
    
    tab1_label = Label(tab1_content, text="General Settings Panel")
    tab1_label.place(x=20, y=20)
    
    tab2_content = Panel(tabs)
    tab2 = tabs.add_tab("Advanced", tab2_content)
    
    tab2_label = Label(tab2_content, text="Advanced Configuration")
    tab2_label.place(x=20, y=20)
    
    tab3_content = Panel(tabs)
    tab3 = tabs.add_tab("Network", tab3_content)
    
    tab3_label = Label(tab3_content, text="Network Settings")
    tab3_label.place(x=20, y=20)
    
    # Progress and slider
    progress_group = GroupBox(right_panel, text="Progress & Slider")
    progress_group.place(x=8, y=tabs.winfo_height() + 16, relwidth=1.0, relheight=0.25)
    
    pp = progress_group.content
    
    progress = ProgressBar(pp, width=400)
    progress.place(x=10, y=20)
    
    def update_progress():
        val = progress.get_value() + 0.05
        if val > 1.0:
            val = 0.0
        progress.set_value(val)
        pp.after(500, update_progress)
    
    pp.after(500, update_progress)
    
    slider = Slider(pp, min_val=0, max_val=100, value=50, orientation="horizontal",
                    command=lambda v: app.console.info(f"Slider: {v}"))
    slider.place(x=10, y=60, width=400)
    
    # Listbox and combobox
    list_group = GroupBox(right_panel, text="Lists")
    list_group.place(x=8, y=int(right_panel.winfo_height() * 0.85), relwidth=1.0, relheight=0.15)
    
    lp = list_group.content
    
    listbox = ListBox(lp, items=["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"], width=200, height=80)
    listbox.place(x=10, y=10)
    
    combobox = ComboBox(lp, items=["Option A", "Option B", "Option C"], width=150)
    combobox.place(x=220, y=10)
    
    # Console at bottom
    console_group = GroupBox(main_panel, text="Console")
    console_group.place(x=8, y=int(main_panel.winfo_height() * 0.7), relwidth=1.0, relheight=0.3)
    
    console = Console(console_group, width=console_group.content.winfo_width(), height=120)
    console.pack(fill="both", expand=True, padx=5, pady=5)
    
    console.info("PVGUIY Console initialized")
    console.success("Framework loaded successfully")
    console.warning("Warning: This is a demo application")
    console.error("Error: Sample error message")
    
    # Theme switcher
    theme_group = GroupBox(main_panel, text="Theme Switcher")
    theme_group.place(x=8, y=int(main_panel.winfo_height() * 0.6), width=300, height=80)
    
    tp = theme_group.content
    
    def set_green():
        app.set_theme("green")
        app.notify.info("Theme Changed", "Switched to Green theme")
    
    def set_orange():
        app.set_theme("orange")
        app.notify.info("Theme Changed", "Switched to Orange theme")
    
    def set_black():
        app.set_theme("black")
        app.notify.info("Theme Changed", "Switched to Black theme")
    
    btn_green = Button(tp, text="Green", command=set_green)
    btn_green.place(x=10, y=20, width=80)
    
    btn_orange = Button(tp, text="Orange", command=set_orange)
    btn_orange.place(x=100, y=20, width=80)
    
    btn_black = Button(tp, text="Black", command=set_black)
    btn_black.place(x=190, y=20, width=80)
    
    # Status bar
    statusbar = StatusBar(window)
    statusbar.set_text("Ready - PVGUIY v1.0.0")
    
    # Tooltips
    ToolTip(btn1, "Click this button to see a success notification")
    ToolTip(btn2, "Secondary action button")
    ToolTip(entry1, "Enter your text here")
    
    # Store references to prevent garbage collection
    app._widgets = [menubar, main_panel, left_panel, right_panel, controls_group, 
                    entries_group, progress_group, list_group, console_group, theme_group,
                    btn1, btn2, btn3, chk1, chk2, chk3, radio1, radio2, radio3,
                    entry1, entry2, textarea, tabs, tab1, tab2, tab3,
                    progress, slider, listbox, combobox, console, statusbar,
                    btn_green, btn_orange, btn_black]
    
    app.run()
