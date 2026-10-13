import flet as ft
from constants import C_ORANGE, C_CYAN, C_GREEN, C_DARK, C_CARD, C_BORDER


class AppTitle(ft.Text):
    def __init__(self, text):
        super().__init__(value=text, size=22, weight=ft.FontWeight.BOLD, color=C_ORANGE)


class BodyText(ft.Text):
    def __init__(self, text="", w=None, color=C_DARK):
        super().__init__(value=text, size=14, width=w, color=color)


class InputField(ft.TextField):
    def __init__(self, label, w=180, val="", change=None):
        super().__init__(
            label=label,
            width=w,
            value=val,
            on_change=change,
            bgcolor="#FFFFFF",
            border_color=C_CYAN,
            focused_border_color=C_ORANGE,
            cursor_color=C_ORANGE,
            color=C_DARK,
            label_style=ft.TextStyle(color=C_DARK),
        )


class ActionButton(ft.Button):
    def __init__(self, text, click, data=None, bg=C_ORANGE, fg="#FFFFFF"):
        super().__init__(content=text, on_click=click, data=data, bgcolor=bg, color=fg)


class StatusCheckbox(ft.Checkbox):
    def __init__(self, label, val=False, change=None, data=None):
        super().__init__(
            label=label,
            value=val,
            on_change=change,
            data=data,
            active_color=C_GREEN,
            check_color="#FFFFFF",
            label_style=ft.TextStyle(color=C_DARK),
        )


class SelectDropdown(ft.Dropdown):
    def __init__(self, label, items, val, change=None):
        opts = [ft.DropdownOption(x) for x in items]
        super().__init__(
            label=label,
            width=150,
            value=val,
            options=opts,
            on_select=change,
            bgcolor="#FFFFFF",
            border_color=C_CYAN,
            focused_border_color=C_ORANGE,
            color=C_DARK,
            label_style=ft.TextStyle(color=C_DARK),
        )


class FlexRow(ft.Row):
    def __init__(self, controls):
        super().__init__(
            controls=controls,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )


class FlexColumn(ft.Column):
    def __init__(self, controls):
        super().__init__(
            controls=controls,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
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
        super().__init__(value=val, width=250, color=C_GREEN, bgcolor="#E2E8F0")


class AppDivider(ft.Divider):
    def __init__(self):
        super().__init__(height=1, color=C_CYAN)
