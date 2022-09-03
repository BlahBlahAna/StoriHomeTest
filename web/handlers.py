import csv

from decimal import Decimal
from flask import render_template
from flask_mail import Message

from config import app, mail
from helpers import MONTH_MAPPER, PREDEFINED_USER
from mongo_repositories import TransactionRepository


class FileHandler:
    def __init__(self, transaction_checker):
        self.transaction_checker = transaction_checker

    def read_file_content(self):
        with open("transactions.csv", mode="r") as input:
            reader = csv.reader(input)
            for row in reader:
                try:
                    transaction = self.transaction_checker.create_transaction(row)
                    TransactionRepository.add_to_credit(transaction) if transaction[
                        "type"
                    ] == "credit" else TransactionRepository.add_to_debit(transaction)
                except Exception:
                    continue


class SummaryHandler:
    def __init__(self, summary_obj):
        self.summary_obj = summary_obj
        self.account_credit_historical_data = []
        self.account_debit_historical_data = []

    def make_summary(self):
        self.__retrieve_account_data()

        monthly_detail = self.__create_monthly_detail()
        historical_credit_balance = self.__calculate_historical_credit_balance()
        historical_debit_balance = self.__calculate_historical_debit_balance()
        total_balance = round((historical_credit_balance + historical_debit_balance), 2)

        historical_credit_average = round(
            (historical_credit_balance / len(self.account_credit_historical_data)), 2
        )
        historical_debit_average = round(
            (historical_debit_balance / len(self.account_debit_historical_data)), 2
        )

        return self.summary_obj.create_summary(
            total_balance,
            historical_credit_average,
            historical_debit_average,
            monthly_detail,
        )

    def __calculate_historical_credit_balance(self):
        credit_balance = 0
        for record in self.account_credit_historical_data:
            credit_balance += Decimal(record["amount"])
        return credit_balance

    def __calculate_historical_debit_balance(self):
        debit_balance = 0
        for record in self.account_debit_historical_data:
            debit_balance += Decimal(record["amount"])
        return debit_balance

    def __create_monthly_detail(self):
        monthly_detail = {
            num: {
                "total_number_of_transactions": 0,
                "credit_number_of_transactions": 0,
                "debit_number_of_transactions": 0,
                "credit_total_amount": 0,
                "debit_total_amount": 0,
                "credit_average_amount": 0,
                "debit_average_amount": 0,
            }
            for num in range(1, 13)
        }

        for record in self.account_credit_historical_data:
            month = record["month"]
            monthly_detail[month]["credit_number_of_transactions"] += 1
            monthly_detail[month]["credit_total_amount"] += Decimal(record["amount"])

        for record in self.account_debit_historical_data:
            month = record["month"]
            monthly_detail[month]["debit_number_of_transactions"] += 1
            monthly_detail[month]["debit_total_amount"] += Decimal(record["amount"])

        for key in monthly_detail.keys():
            monthly_detail[key]["total_number_of_transactions"] = (
                monthly_detail[key]["credit_number_of_transactions"]
                + monthly_detail[key]["debit_number_of_transactions"]
            )

            if monthly_detail[key]["credit_number_of_transactions"]:
                avg = (
                    monthly_detail[key]["credit_total_amount"]
                    / monthly_detail[key]["credit_number_of_transactions"]
                )
                monthly_detail[key]["credit_average_amount"] = round(avg, 2)

            if monthly_detail[key]["debit_number_of_transactions"]:
                avg = (
                    monthly_detail[key]["debit_total_amount"]
                    / monthly_detail[key]["debit_number_of_transactions"]
                )
                monthly_detail[key]["debit_average_amount"] = round(avg, 2)

        return monthly_detail

    def __retrieve_account_data(self):
        self.account_credit_historical_data = TransactionRepository.get_all_credit()
        self.account_debit_historical_data = TransactionRepository.get_all_debit()


class EmailHandler:
    def __init__(self, full_summary):
        self.full_summary = full_summary

    def send_email(self):
        msg = Message(
            "Your Transaction Summary from Stori",
            sender=app.config.get("MAIL_USERNAME"),
            recipients=[PREDEFINED_USER["email"]],
        )

        msg.html = render_template(
            "transaction_summary.html",
            username=PREDEFINED_USER["first_name"],
            summary=self.full_summary,
            month_mapper=MONTH_MAPPER,
        )
        mail.send(msg)
