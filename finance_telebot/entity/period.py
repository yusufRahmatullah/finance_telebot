from datetime import date

_month_names = [
    '',
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des'
]


class Period:
    def __init__(self, year: int, month: int):
        self.begin = date(year, month, 27)
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        self.end = date(next_year, next_month, 26)

    def __str__(self):
        lp = f'27 {_month_names[self.begin.month]} {self.begin.year}'
        rp = f'26 {_month_names[self.end.month]} {self.end.year}'
        return f'{lp} - {rp}'

    @classmethod
    def now(cls) -> 'Period':
        now = date.today()
        if now.day >= 27:
            month = now.month
        else:
            month = now.month - 1
        if month == 0:
            year = now.year - 1
            month = 12
        else:
            year = now.year
        return cls(year, month)

    @classmethod
    def parse(cls, value: str) -> 'Period':
        if not value:
            return cls.now()
        begin = value.partition(' - ')[0]
        _, month, year = begin.split()
        monthnum = _month_names.index(month)

        return cls(int(year), monthnum)
