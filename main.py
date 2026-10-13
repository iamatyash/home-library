"""
Приложение «Домашняя библиотека» на Flet.
Учебный проект для зачета по ООП.
"""

import flet as ft
from models import Book, Journal, MyMap, Session


# =====================================================================
# Пользовательские UI-компоненты (требование: переопределить >= 10 компонентов окна)
# =====================================================================

class AppTitle(ft.Text):
    def __init__(self, text):
        super().__init__(value=text, size=22, weight=ft.FontWeight.BOLD)


class BodyText(ft.Text):
    def __init__(self, text="", w=None):
        super().__init__(value=text, size=14, width=w)


class InputField(ft.TextField):
    def __init__(self, label, w=180, val="", change=None):
        super().__init__(label=label, width=w, value=val, on_change=change)


class ActionButton(ft.Button):
    def __init__(self, text, click, data=None):
        super().__init__(content=text, on_click=click, data=data)


class StatusCheckbox(ft.Checkbox):
    def __init__(self, label, val=False, change=None, data=None):
        super().__init__(label=label, value=val, on_change=change, data=data)


class SelectDropdown(ft.Dropdown):
    def __init__(self, label, items, val, change=None):
        opts = [ft.DropdownOption(x) for x in items]
        super().__init__(label=label, width=150, value=val, options=opts, on_select=change)


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
            bgcolor="#1A1A1A",
            border_radius=8,
        )


class AppProgressBar(ft.ProgressBar):
    def __init__(self, val=0.0):
        super().__init__(value=val, width=250)


class AppDivider(ft.Divider):
    def __init__(self):
        super().__init__(height=1, color="#2E2E2E")


# =====================================================================
# Основной класс приложения
# =====================================================================

class App:
    current = None

    def __init__(self, page):
        self.page = page
        self.session = Session("UserName")

        # Коллекции по ТЗ (tuple, set, list, кастомный маппинг)
        self.types = ("Все", "Книга", "Журнал")  # tuple
        self.authors = set()                     # set
        self.stats = MyMap()                     # кастомный класс вместо dict

        # Начальный список объектов (требование: не менее 10 объектов)
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
        """Настройка параметров окна приложения."""
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
        """Инициализация и размещение элементов интерфейса."""
        self.title_lbl = AppTitle("Домашняя библиотека")
        self.login_inp = InputField("Логин", 180, "UserName", self.on_login_change)

        self.type_drop = SelectDropdown("Тип", ("Книга", "Журнал"), "Книга")
        self.name_inp = InputField("Название", 200)
        self.author_inp = InputField("Автор", 160)
        self.pages_inp = InputField("Страниц", 100, "300")
        self.extra_inp = InputField("Жанр / Номер", 150, "Роман")
        self.done_chk = StatusCheckbox("Прочитано", False)
        self.add_btn = ActionButton("Добавить", self.add_item)

        self.filter_drop = SelectDropdown("Фильтр", self.types, "Все", self.refresh)
        self.sort_btn = ActionButton("Сортировать по стр.", self.sort_items)
        self.cmp_btn = ActionButton("Сравнить 2 первых", self.compare_items)
        self.info_lbl = BodyText("")

        self.list_col = FlexColumn([])
        self.stats_lbl = BodyText("")
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
        """Обновление логина активной сессии."""
        self.session.login = self.login_inp.value

    def add_item(self, e):
        """Добавление нового элемента библиотеки."""
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
        """Сортировка списка элементов (используется __lt__)."""
        self.items.sort()
        self.refresh()

    def compare_items(self, e):
        """Сравнение первых двух элементов списка (демонстрация __eq__, __lt__, __add__, __len__)."""
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
        """Переключение статуса прочтения."""
        item = e.control.data
        item.done = e.control.value
        self.refresh()

    def delete_item(self, e):
        """Удаление элемента из коллекции."""
        item = e.control.data
        if item in self.items:
            self.items.remove(item)
            self.refresh()

    def refresh(self, e=None):
        """Фильтрация, расчет статистики и обновление отображения."""
        self.list_col.controls.clear()
        self.authors = {x.author for x in self.items}

        flt = self.filter_drop.value
        for item in self.items:
            if flt == "Книга" and not isinstance(item, Book):
                continue
            if flt == "Журнал" and not isinstance(item, Journal):
                continue

            chk = StatusCheckbox("", item.done, self.toggle_item, item)
            txt = BodyText(item.get_info(), 520)
            del_btn = ActionButton("Удалить", self.delete_item, item)
            row = CardContainer(FlexRow([chk, txt, del_btn]))
            self.list_col.controls.append(row)

        total = len(self.items)
        done_cnt = sum(1 for x in self.items if bool(x))
        pages_sum = sum(len(x) for x in self.items)

        # Сохранение агрегатов в кастомный маппинг MyMap
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
        """Сохранение отчета сессии в файл report.txt по ТЗ."""
        self.session.login = self.login_inp.value
        self.session.save("report.txt")

    def on_win_event(self, e):
        """Обработка системных событий окна (сохранение при закрытии)."""
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
