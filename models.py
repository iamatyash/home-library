from abc import ABC, abstractmethod
from datetime import datetime


class BaseItem(ABC):
    def __init__(self, name, author, pages, done=False):
        self._name = str(name)
        self._author = str(author)
        self._pages = max(1, int(pages))
        self._done = bool(done)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = str(val).strip()

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, val):
        self._author = str(val).strip()

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
        try:
            return int(val) > 0
        except (ValueError, TypeError):
            return False

    def __eq__(self, other):
        if not isinstance(other, BaseItem):
            return False
        return self._name == other._name and self._pages == other._pages

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self._name}', author='{self._author}', pages={self._pages})"

    def __str__(self):
        status = "Прочитано" if self._done else "Не прочитано"
        return f"{self._name} — {self._author} ({self._pages} стр.) [{status}]"

    def __lt__(self, other):
        if not isinstance(other, BaseItem):
            return NotImplemented
        return self._pages < other._pages

    def __le__(self, other):
        if not isinstance(other, BaseItem):
            return NotImplemented
        return self._pages <= other._pages

    def __gt__(self, other):
        if not isinstance(other, BaseItem):
            return NotImplemented
        return self._pages > other._pages

    def __ge__(self, other):
        if not isinstance(other, BaseItem):
            return NotImplemented
        return self._pages >= other._pages

    def __len__(self):
        return self._pages

    def __add__(self, other):
        if isinstance(other, BaseItem):
            return self._pages + other._pages
        if isinstance(other, int):
            return self._pages + other
        return NotImplemented

    def __bool__(self):
        return self._done

    def __hash__(self):
        return hash((self._name, self._author, self._pages))


class Book(BaseItem):
    def __init__(self, name, author, pages, genre="Роман", done=False):
        super().__init__(name, author, pages, done)
        self._genre = str(genre)

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, val):
        self._genre = str(val).strip()

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
        self._num = str(val).strip()

    def get_info(self):
        return f"Журнал | {self._name} ({self._num}) — {self._author} | {self._pages} стр."


class MyMap:
    def __init__(self):
        self._keys = []
        self._vals = []

    @property
    def keys(self):
        return list(self._keys)

    @property
    def values(self):
        return list(self._vals)

    def put(self, key, value):
        if key in self._keys:
            idx = self._keys.index(key)
            self._vals[idx] = value
        else:
            self._keys.append(key)
            self._vals.append(value)

    def get(self, key, default=None):
        if key in self._keys:
            idx = self._keys.index(key)
            return self._vals[idx]
        return default

    def remove(self, key):
        if key in self._keys:
            idx = self._keys.index(key)
            self._keys.pop(idx)
            self._vals.pop(idx)

    def __getitem__(self, key):
        if key in self._keys:
            return self.get(key)
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __len__(self):
        return len(self._keys)

    def __contains__(self, key):
        return key in self._keys

    def __repr__(self):
        items_str = ", ".join(f"{k!r}: {v!r}" for k, v in zip(self._keys, self._vals))
        return f"MyMap({{{items_str}}})"

    def __str__(self):
        return self.__repr__()


class Session:
    DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"

    def __init__(self, login="UserName"):
        self._login = str(login).strip() or "UserName"
        self._time_in = self.now_formatted()
        self._time_out = self.now_formatted()

    @staticmethod
    def now_formatted():
        return datetime.now().strftime(Session.DATETIME_FORMAT)

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
        self._time_out = self.now_formatted()
        line = "+------------------------------------------------------+"
        head = f"| {'login':<10}| {'time_in':<20}| {'time_out':<20}|"
        sep = "|-----------|---------------------|---------------------|"
        row = f"| {self._login:<10}| {self._time_in:<20}| {self._time_out:<20}|"
        text = "\n".join([line, head, sep, row, line]) + "\n"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

    def __repr__(self):
        return f"Session(login='{self._login}', time_in='{self._time_in}', time_out='{self._time_out}')"

    def __str__(self):
        return self.get_info()
