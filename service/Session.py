from datetime import datetime


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
        return f"{self._login} | {self._time_in} | {self._time_out}"

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
