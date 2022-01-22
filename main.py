import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Не стоит злоупотреблять использованием тернарного оператора
        # Eсли приходится разносить оператор на несколько строк, страдает его
        # читаемость. В данной ситуации лучше использовать стандартный блок if-else
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Имя параметра цикла не соответсвует PEP8, более того,
        # сопадает с именем существующего класса. Следует выбрать другое имя
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            # Нет необходимости в переносе ): на другую строку.
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий к функции не соответствуют требованиям PEP8.
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Стандарт PEP8 не рекомендует использовать \ для переноса
            # Корректный перенос используется вами ниже в if cash_remained > 0
            # Следует придерживаться одного стиля во всем документе
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Есть ли смысл использовать преобразование типа? Можно сразу положить
    # в константы значение типа float (60.0, 70.0)
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # По всей видимости опечатка? Следует исправить на /= 1.0
            # если есть необходимость выводить остаток типа float
            cash_remained == 1.00
            currency_type = 'руб'
        # Возможно, следует описать обработку ситуации, когда не был передан
        # параметр currency. Сейчас программа выведет некоторую сумму без
        # указания единиц измерения
        if cash_remained > 0:
            return (
                # Согласно условию задания не допускаются вызовы функций в f-строках
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Следует придерживаться одного стиля во всем документе
            # Выше использовались f строки
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # Нет необходимости в переопределнии функции, она будет унаследована
    # от класса-родителя. Все что идет ниже нужно убрать
    def get_week_stats(self):
        super().get_week_stats()

# Код не закрыт конструкцией if __name__ == ‘__main__’
