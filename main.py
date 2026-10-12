# //вообще я джавист поэтому на пайтоне не получилось сделать круто
import flet as ft
from models import Book, Journal, MyMap, Session


class MyTitle(ft.Text):
    def __init__(self, text):
        super().__init__(value=text, size=22, weight=ft.FontWeight.BOLD)


class MyText(ft.Text):
    def __init__(self, text="", w=None):
        super().__init__(value=text, size=14, width=w)


class MyInput(ft.TextField):
    def __init__(self, label, w=180, val="", change=None):
        super().__init__(label=label, width=w, value=val, on_change=change)


class MyBtn(ft.Button):
    def __init__(self, text, click, data=None):
        super().__init__(content=text, on_click=click, data=data)


class MyCheck(ft.Checkbox):
    def __init__(self, label, val=False, change=None, data=None):
        super().__init__(label=label, value=val, on_change=change, data=data)


class MyDrop(ft.Dropdown):
    def __init__(self, label, items, val, change=None):
        opts = [ft.DropdownOption(x) for x in items]
        super().__init__(label=label, width=150, value=val, options=opts, on_select=change)


class MyRow(ft.Row):
    def __init__(self, controls):
        super().__init__(
            controls=controls,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )


class MyCol(ft.Column):
    def __init__(self, controls):
        super().__init__(
            controls=controls,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
        )


class MyBox(ft.Container):
    def __init__(self, content):
        super().__init__(
            content=content,
            padding=10,
            bgcolor="#1A1A1A",
            border_radius=6,
        )


class MyBar(ft.ProgressBar):
    def __init__(self, val=0.0):
        super().__init__(value=val, width=250)


class App:
    current = None

    def __init__(self, page):
        self.page = page
        self.session = Session("UserName")
        self.types = ("Все", "Книга", "Журнал")
        self.authors = set()
        self.stats = MyMap()

        self.items = [
            Book("Мастер и Маргарита", "Булгаков", 480, "Роман", True),
            Book("Преступление и наказание", "Достоевский", 608, "Классика", True),
            Book("1984", "Оруэлл", 320, "Антиутопия", True),
            Book("Три товарища", "Ремарк", 480, "Роман", False),
            Book("Мартин Иден", "Лондон", 448, "Драма", True),
            Book("Портрет Дориана Грея", "Уайльд", 320, "Классика", False),
            Book("Пикник на обочине", "Стругацкие", 256, "Фантастика", True),
            Book("451 градус по Фаренгейту", "Брэдбери", 288, "Фантастика", False),
            Journal("Вокруг света", "Редакция", 112, "№10", True),
            Journal("Наука и жизнь", "Редакция", 128, "№8", False),
        ]

        self.setup_window()
        self.build_ui()
        self.refresh()

    def setup_window(self):
        self.page.title = "Домашняя библиотека"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#121212"
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
        self.title_lbl = MyTitle("Домашняя библиотека")
        self.login_inp = MyInput("Логин", 180, "UserName", self.on_login_change)

        self.type_drop = MyDrop("Тип", ("Книга", "Журнал"), "Книга")
        self.name_inp = MyInput("Название", 200)
        self.author_inp = MyInput("Автор", 160)
        self.pages_inp = MyInput("Страниц", 100, "300")
        self.extra_inp = MyInput("Жанр / Номер", 150, "Роман")
        self.done_chk = MyCheck("Прочитано", False)
        self.add_btn = MyBtn("Добавить", self.add_item)

        self.filter_drop = MyDrop("Фильтр", self.types, "Все", self.refresh)
        self.sort_btn = MyBtn("Сортировать по стр.", self.sort_items)
        self.cmp_btn = MyBtn("Сравнить 2 первых", self.compare_items)
        self.info_lbl = MyText("")

        self.list_col = MyCol([])
        self.stats_lbl = MyText("")
        self.prog_bar = MyBar(0)

        top_row = MyRow([self.title_lbl, self.login_inp])
        add_row1 = MyRow([self.type_drop, self.name_inp, self.author_inp, self.pages_inp])
        add_row2 = MyRow([self.extra_inp, self.done_chk, self.add_btn])
        ctrl_row = MyRow([self.filter_drop, self.sort_btn, self.cmp_btn, self.info_lbl])
        bot_row = MyRow([self.stats_lbl, self.prog_bar])

        self.page.add(
            top_row,
            MyBox(MyCol([add_row1, add_row2])),
            ctrl_row,
            self.list_col,
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
            self.info_lbl.value = "Заполните поля корректно"
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
            self.info_lbl.value = "Нужно минимум 2 объекта"
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

            chk = MyCheck("", item.done, self.toggle_item, item)
            txt = MyText(item.get_info(), 520)
            del_btn = MyBtn("Удалить", self.delete_item, item)
            row = MyBox(MyRow([chk, txt, del_btn]))
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
