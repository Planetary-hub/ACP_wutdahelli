import tkinter as tk
from config import (
    BG_COLOR, FRAME_COLOR, SIDEBAR_COLOR, TEXT_COLOR, SUBTEXT_COLOR,
    BUTTON_COLOR, BUTTON_TEXT, BUTTON_HOVER, DANGER_COLOR, DANGER_HOVER,
    ENTRY_COLOR, LIST_COLOR, LIST_TEXT,
    FONT_MAIN, FONT_TITLE, FONT_HEADER, FONT_BUTTON
)

def show_page(page, pages, refresh_cb):
    for p in pages:
        p.pack_forget()

    page.pack(fill="both", expand=True, padx=18, pady=18)
    refresh_cb()

def make_page_title(parent, title, subtitle):
    tk.Label(
        parent,
        text=title,
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        font=FONT_TITLE
    ).pack(anchor="w", pady=(0, 5))

    tk.Label(
        parent,
        text=subtitle,
        bg=BG_COLOR,
        fg=SUBTEXT_COLOR,
        font=FONT_MAIN
    ).pack(anchor="w", pady=(0, 15))

def make_panel(parent, title):
    panel = tk.LabelFrame(
        parent,
        text=title,
        bg=FRAME_COLOR,
        fg=TEXT_COLOR,
        font=FONT_HEADER,
        padx=15,
        pady=15
    )
    panel.pack(fill="both", expand=True)
    return panel

def make_label(parent, text, row, col, columnspan=1):
    tk.Label(
        parent,
        text=text,
        bg=FRAME_COLOR,
        fg=TEXT_COLOR,
        font=FONT_MAIN
    ).grid(row=row, column=col, columnspan=columnspan, padx=5, pady=5, sticky="w")

def make_entry(parent, row, col, width=25):
    entry = tk.Entry(
        parent,
        width=width,
        bg=ENTRY_COLOR,
        fg="black",
        font=FONT_MAIN
    )
    entry.grid(row=row, column=col, padx=5, pady=5, sticky="w")
    return entry

def make_button(parent, text, command, row, col, danger=False, columnspan=1):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=DANGER_COLOR if danger else BUTTON_COLOR,
        fg=BUTTON_TEXT,
        font=FONT_BUTTON,
        activebackground=DANGER_HOVER if danger else BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        width=18
    )
    btn.grid(row=row, column=col, columnspan=columnspan, padx=5, pady=5, sticky="w")
    return btn

def make_listbox(parent, row, col, height=8, columnspan=4):
    box = tk.Listbox(
        parent,
        width=95,
        height=height,
        bg=LIST_COLOR,
        fg=LIST_TEXT,
        font=FONT_MAIN,
        selectbackground="#5b4b8a",
        selectforeground="white"
    )
    box.grid(row=row, column=col, columnspan=columnspan, padx=5, pady=10, sticky="w")
    return box

def make_sidebar_button(parent, text, command, danger=False):
    tk.Button(
        parent,
        text=text,
        command=command,
        bg=DANGER_COLOR if danger else BUTTON_COLOR,
        fg=BUTTON_TEXT,
        font=FONT_BUTTON,
        activebackground=DANGER_HOVER if danger else BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        width=18,
        height=2
    ).pack(pady=7)
