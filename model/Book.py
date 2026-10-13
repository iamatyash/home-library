from model.BaseItem import BaseItem


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
