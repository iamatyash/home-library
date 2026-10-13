from model.ProtoItem import ProtoItem


class Journal(ProtoItem):
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
