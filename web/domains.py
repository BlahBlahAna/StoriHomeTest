import re


class SummaryObj:
    def __init__(self):
        self.total_balance = 0
        self.historical_credit_average = 0
        self.historical_debit_average = 0
        self.monthly_detail = {}

    def create_summary(
        self, total_balance, historical_credit_avg, historical_debit_avg, monthly_detail
    ):
        self.total_balance = total_balance
        self.historical_credit_average = historical_credit_avg
        self.historical_debit_average = historical_debit_avg
        self.monthly_detail = monthly_detail

        return self.get_summary()

    def get_summary(self):
        return {
            "total_balance": self.total_balance,
            "historical_credit_average": self.historical_credit_average,
            "historical_debit_average": self.historical_debit_average,
            "monthly_detail": self.monthly_detail,
        }


class Transaction:
    def __init__(self):
        self.id = ""
        self.full_date = ""
        self.month = 0
        self.day = 0
        self.amount = ""
        self.type = ""

    def create_transaction(self, data):
        self.id = data[0]
        self.full_date = data[1]

        split_date = data[1].split("/")
        self.month = int(split_date[0])
        self.day = int(split_date[1])

        self.amount = data[2]
        self.type = self.__classify_credit_or_debit()

        if self.__validate_record():
            return {
                "identifier": self.id,
                "month": self.month,
                "day": self.day,
                "amount": self.amount,
                "type": self.type,
            }
        else:
            raise Exception("Invalid Record")

    def __validate_record(self):
        self.__validate_date()
        self.__validate_amount()
        return self.__validate_date() and self.__validate_amount()

    def __validate_date(self):
        date_pattern = r"^([1-9]|1[012])[\/]([1-9]|[12][0-9]|3[01])$"
        return bool(re.match(date_pattern, self.full_date))

    def __validate_amount(self):
        amount_pattern = r"^([-\+]{1})([0-9]+)(\.{1})([0-9]{2})$"
        return bool(re.match(amount_pattern, self.amount))

    def __classify_credit_or_debit(self):
        return "debit" if self.amount[0] == "-" else "credit"
