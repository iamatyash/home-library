import flet as ft
from models import Book, Journal, MyMap, Session

C_ORANGE = "#FF9D50"
C_MILK = "#FFF9D8"
C_CYAN = "#1DCED8"
C_GREEN = "#55E07E"
C_DARK = "#2B2625"
C_CARD = "#FFFFFF"


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
            bgcolor=C_CARD,
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
            bgcolor=C_CARD,
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
        )


class AppProgressBar(ft.ProgressBar):
    def __init__(self, val=0.0):
        super().__init__(value=val, width=250, color=C_GREEN, bgcolor="#E2DEC8")


class AppDivider(ft.Divider):
    def __init__(self):
        super().__init__(height=1, color=C_CYAN)


class App:
    current = None

    def __init__(self, page):
        self.page = page
        self.session = Session("UserName")

        self.types = ("Все", "Книга", "Журнал")
        self.authors = set()
        self.stats = MyMap()

        self.items = [
            Book("Если все кошки в мире исчезнут", "Гэнки Кавамура", 224, "Фэнтези", True),
            Book("Кафе на краю земли", "Джон Стрелеки", 176, "Психология", True),
            Book("1984", "Джордж Оруэлл", 320, "Антиутопия", True),
            Book("Бабушка сказала сидеть тихо", "Настасья Реньжина", 256, "Драма", False),
            Book("Спеши любить", "Николас Спаркс", 288, "Роман", False),
            Book("Летний лагерь", "Влад Райбер", 384, "Мистика", True),
            Book("Проект Аве Мария", "Энди Вейер", 512, "Фантастика", True),
            Book("Десять негритят", "Агата Кристи", 224, "Детектив", False),
            Journal("За рулем", "Редакция", 112, "№10", True),
            Journal("Домашний", "Редакция", 64, "№19", False),
        ]

        self.setup_window()
        self.build_ui()
        self.refresh()

    def setup_window(self):
        self.page.title = "Домашняя библиотека"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = C_MILK
        self.page.padding = 20
        self.page.spacing = 12
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.window.width = 920
        self.page.window.height = 720
        self.page.window.min_width = 750
        self.page.window.min_height = 550
        self.page.window.resizable = True
        self.page.window.on_event = self.on_win_event

    def build_ui(self):
        self.title_lbl = AppTitle("Домашняя библиотека")
        self.login_inp = InputField("Логин", 180, "UserName", self.on_login_change)

        self.type_drop = SelectDropdown("Тип", ("Книга", "Журнал"), "Книга")
        self.name_inp = InputField("Название", 200)
        self.author_inp = InputField("Автор", 160)
        self.pages_inp = InputField("Страниц", 100, "300")
        self.extra_inp = InputField("Жанр / Номер", 150, "Роман")
        self.done_chk = StatusCheckbox("Прочитано", False)
        self.add_btn = ActionButton("Добавить", self.add_item, bg=C_ORANGE, fg="#FFFFFF")

        self.filter_drop = SelectDropdown("Фильтр", self.types, "Все", self.refresh)
        self.sort_btn = ActionButton("Сортировать по стр.", self.sort_items, bg=C_CYAN, fg="#2B2625")
        self.cmp_btn = ActionButton("Сравнить 2 первых", self.compare_items, bg=C_GREEN, fg="#2B2625")
        self.info_lbl = BodyText("", color=C_ORANGE)

        self.list_col = FlexColumn([])
        self.stats_lbl = BodyText("", color=C_DARK)
        self.prog_bar = AppProgressBar(0)

        top_row = FlexRow([self.title_lbl, self.login_inp])
        add_row1 = FlexRow([self.type_drop, self.name_inp, self.author_inp, self.pages_inp])
        add_row2 = FlexRow([self.extra_inp, self.done_chk, self.add_btn])
        ctrl_row = FlexRow([self.filter_drop, self.sort_btn, self.cmp_btn, self.info_lbl])
        bot_row = FlexRow([self.stats_lbl, self.prog_bar])

        self.page.add(
            top_row,
            CardContainer(FlexColumn([add_row1, add_row2])),
            ctrl_row,
            AppDivider(),
            self.list_col,
            AppDivider(),
            bot_row,
        )

    def on_login_change(self, e):
        self.session.login = self.login_inp.value

    def add_item(self, e):
        name = self.name_inp.value.strip()
        author = self.author_inp.value.strip()
        pages_str = self.pages_inp.value.strip()
        extra = self.extra_inp.value.strip()

        if not name or not author or not Book.check_pages(pages_str):
            self.info_lbl.value = "Заполните поля корректно (число страниц > 0)"
            self.page.update()
            return

        pages = int(pages_str)
        if self.type_drop.value == "Журнал":
            obj = Journal(name, author, pages, extra or "№1", self.done_chk.value)
        else:
            obj = Book(name, author, pages, extra or "Роман", self.done_chk.value)

        self.items.append(obj)
        self.name_inp.value = ""
        self.author_inp.value = ""
        self.info_lbl.value = ""
        self.refresh()

    def sort_items(self, e):
        self.items.sort()
        self.refresh()

    def compare_items(self, e):
        if len(self.items) < 2:
            self.info_lbl.value = "Нужно минимум 2 объекта для сравнения"
        else:
            a = self.items[0]
            b = self.items[1]
            sign = "==" if a == b else ("<" if a < b else ">")
            total = a + b
            self.info_lbl.value = f"{a.name} ({len(a)} стр.) {sign} {b.name} ({len(b)} стр.) | Сумма: {total} стр."
        self.page.update()

    def toggle_item(self, e):
        item = e.control.data
        item.done = e.control.value
        self.refresh()

    def delete_item(self, e):
        item = e.control.data
        if item in self.items:
            self.items.remove(item)
            self.refresh()

    def refresh(self, e=None):
        self.list_col.controls.clear()
        self.authors = {x.author for x in self.items}

        flt = self.filter_drop.value
        for item in self.items:
            if flt == "Книга" and not isinstance(item, Book):
                continue
            if flt == "Журнал" and not isinstance(item, Journal):
                continue

            chk = StatusCheckbox("", item.done, self.toggle_item, item)
            txt = BodyText(item.get_info(), 520, color=C_DARK)
            del_btn = ActionButton("Удалить", self.delete_item, item, bg="#FFF0E6", fg=C_ORANGE)
            row = CardContainer(FlexRow([chk, txt, del_btn]))
            self.list_col.controls.append(row)

        total = len(self.items)
        done_cnt = sum(1 for x in self.items if bool(x))
        pages_sum = sum(len(x) for x in self.items)

        self.stats.put("total", total)
        self.stats.put("done", done_cnt)
        self.stats.put("pages", pages_sum)

        self.stats_lbl.value = (
            f"Всего: {self.stats['total']} | "
            f"Прочитано: {self.stats['done']} | "
            f"Страниц: {self.stats['pages']} | "
            f"Авторов: {len(self.authors)}"
        )
        self.prog_bar.value = (done_cnt / total) if total > 0 else 0
        self.page.update()

    def save_report(self):
        self.session.login = self.login_inp.value
        self.session.save("report.txt")

    def on_win_event(self, e):
        if "close" in str(e.data).lower() or "close" in str(getattr(e, "type", "")).lower():
            self.save_report()

    @staticmethod
    def main(page):
        App.current = App(page)

    @staticmethod
    def start():
        ft.run(App.main)
        if App.current is not None:
            App.current.save_report()


if __name__ == "__main__":
    App.start()
