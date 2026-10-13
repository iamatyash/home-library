import flet as ft
from util.Constants import C_BG, C_CARD, C_BORDER, C_ACCENT, C_TEXT


class AppTitle(ft.Text):
    def __init__(self, text):
        super().__init__(value=text, size=22, weight=ft.FontWeight.BOLD, color=C_ACCENT)


class BodyText(ft.Text):
    def __init__(self, text="", w=None, color=C_TEXT, size=14, weight=None):
        super().__init__(value=text, size=size, width=w, color=color, weight=weight)


class InputField(ft.TextField):
    def __init__(self, hint="", w=180, val="", change=None):
        super().__init__(
            hint_text=hint,
            width=w,
            value=val,
            on_change=change,
            bgcolor=C_CARD,
            border_color=C_BORDER,
            focused_border_color=C_ACCENT,
            cursor_color=C_ACCENT,
            color=C_TEXT,
            hint_style=ft.TextStyle(color="#8E8E8E", size=13),
            border_radius=6,
        )


class ActionButton(ft.Button):
    def __init__(self, text, click, data=None, bg=C_ACCENT, fg="#FFFFFF"):
        super().__init__(content=text, on_click=click, data=data, bgcolor=bg, color=fg)


class StatusCheckbox(ft.Checkbox):
    def __init__(self, label, val=False, change=None, data=None):
        super().__init__(
            label=label,
            value=val,
            on_change=change,
            data=data,
            active_color=C_ACCENT,
            check_color="#FFFFFF",
            label_style=ft.TextStyle(color=C_TEXT),
        )


class SelectDropdown(ft.Dropdown):
    def __init__(self, items, val, w=150, change=None):
        opts = [ft.DropdownOption(x) for x in items]
        super().__init__(
            width=w,
            value=val,
            options=opts,
            on_select=change,
            bgcolor=C_CARD,
            border_color=C_BORDER,
            focused_border_color=C_ACCENT,
            color=C_TEXT,
            border_radius=6,
        )


class FlexRow(ft.Row):
    def __init__(self, controls, vertical_alignment=ft.CrossAxisAlignment.CENTER):
        super().__init__(
            controls=controls,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=vertical_alignment,
            spacing=10,
        )


class FlexColumn(ft.Column):
    def __init__(self, controls, spacing=10):
        super().__init__(
            controls=controls,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=spacing,
        )


class CardContainer(ft.Container):
    def __init__(self, content):
        super().__init__(
            content=content,
            padding=10,
            bgcolor=C_CARD,
            border_radius=8,
            border=ft.Border.all(width=1, color=C_BORDER),
        )


class AppProgressBar(ft.ProgressBar):
    def __init__(self, val=0.0):
        super().__init__(value=val, width=250, color=C_ACCENT, bgcolor=C_BORDER)


class AppDivider(ft.Divider):
    def __init__(self):
        super().__init__(height=1, color=C_BORDER)
