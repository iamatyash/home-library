from abc import ABC, abstractmethod


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
        return f"{self._name} | {self._author} ({self._pages} стр.) [{status}]"

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
        return f"Книга | {self._name} | {self._author} | {self._genre} | {self._pages} стр."


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
        return f"Журнал | {self._name} ({self._num}) | {self._author} | {self._pages} стр."
