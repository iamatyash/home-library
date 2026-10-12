from abc import ABC, abstractmethod
from datetime import datetime


class BaseItem(ABC):
    def __init__(self, name, author, pages, done=False):
        self._name = str(name)
        self._author = str(author)
        self._pages = int(pages)
        self._done = bool(done)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = str(val)

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, val):
        self._author = str(val)

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, val):
        self._pages = max(1, int(val))

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, val):
        self._done = bool(val)

    @abstractmethod
    def get_info(self):
        pass

    @staticmethod
    def check_pages(val):
        return str(val).isdigit() and int(val) > 0

    def __eq__(self, other):
        if not isinstance(other, BaseItem):
            return False
        return self._name == other._name and self._pages == other._pages

    def __repr__(self):
        return f"{self.__class__.__name__}({self._name}, {self._pages})"

    def __str__(self):
        status = "Прочитано" if self._done else "Не прочитано"
        return f"{self._name} - {self._author} ({self._pages} стр.) [{status}]"

    def __lt__(self, other):
        return self._pages < other._pages

    def __le__(self, other):
        return self._pages <= other._pages

    def __gt__(self, other):
        return self._pages > other._pages

    def __ge__(self, other):
        return self._pages >= other._pages

    def __len__(self):
        return self._pages

    def __add__(self, other):
        return self._pages + other._pages

    def __bool__(self):
        return self._done

    def __hash__(self):
        return hash((self._name, self._author))


class Book(BaseItem):
    def __init__(self, name, author, pages, genre="Роман", done=False):
        super().__init__(name, author, pages, done)
        self._genre = str(genre)

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, val):
        self._genre = str(val)

    def get_info(self):
        return f"Книга | {self._name} — {self._author} | {self._genre} | {self._pages} стр."


class Journal(BaseItem):
    def __init__(self, name, author, pages, num="№1", done=False):
        super().__init__(name, author, pages, done)
        self._num = str(num)

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, val):
        self._num = str(val)

    def get_info(self):
        return f"Журнал | {self._name} ({self._num}) — {self._author} | {self._pages} стр."


class MyMap(BaseItem):
    def __init__(self):
        super().__init__("map", "system", 1, True)
        self._keys = []
        self._vals = []

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, val):
        self._keys = list(val)

    @property
    def vals(self):
        return self._vals

    @vals.setter
    def vals(self, val):
        self._vals = list(val)

    def get_info(self):
        return f"Записей: {len(self._keys)}"

    def put(self, k, v):
        if k in self._keys:
            idx = self._keys.index(k)
            self._vals[idx] = v
        else:
            self._keys.append(k)
            self._vals.append(v)

    def get(self, k, default=None):
        if k in self._keys:
            idx = self._keys.index(k)
            return self._vals[idx]
        return default

    def __getitem__(self, k):
        return self.get(k)

    def __setitem__(self, k, v):
        self.put(k, v)

    def __len__(self):
        return len(self._keys)


class Session(BaseItem):
    FMT = "%d.%m.%Y %H:%M:%S"

    def __init__(self, login="UserName"):
        super().__init__(login, "user", 1, True)
        self._login = login
        self._time_in = datetime.now().strftime(self.FMT)
        self._time_out = datetime.now().strftime(self.FMT)

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, val):
        self._login = str(val).strip() or "UserName"

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, val):
        self._time_in = str(val)

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, val):
        self._time_out = str(val)

    def get_info(self):
        return f"{self._login}: {self._time_in} - {self._time_out}"

    def save(self, filename="report.txt"):
        self._time_out = datetime.now().strftime(self.FMT)
        line = "+------------------------------------------------------+"
        head = f"| {'login':<9}| {'time_in':<20}| {'time_out':<20}|"
        sep = "|----------|---------------------|---------------------|"
        row = f"|{self._login:<10}| {self._time_in:<20}| {self._time_out:<20}|"
        text = "\n".join([line, head, sep, row, line]) + "\n"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
