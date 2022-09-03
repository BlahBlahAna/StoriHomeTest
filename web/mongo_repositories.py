from pymongo import MongoClient

client = MongoClient("mongodb://db:27017")
db = client.UserTransactions
credit_transactions = db["credit_transactions"]
debit_transactions = db["debit_transactions"]


class TransactionRepository:
    def add_to_credit(transaction):
        credit_transactions.insert_one(transaction)

    def add_to_debit(transaction):
        debit_transactions.insert_one(transaction)

    def get_all_credit():
        return list(credit_transactions.find({}, {"_id": 0}))

    def get_all_debit():
        return list(debit_transactions.find({}, {"_id": 0}))
