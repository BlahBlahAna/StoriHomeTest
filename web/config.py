from flask import Flask
from flask_mail import Mail
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient("mongodb://db:27017")
db = client.UserTransactions
transactions = db["transactions"]

mail_settings = {
    "MAIL_SERVER": "smtp.mailtrap.io",
    "MAIL_PORT": 2525,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": "29640223c6963f",
    "MAIL_PASSWORD": "5394d7340b0ac1",
}

app.config.update(mail_settings)

mail = Mail(app)
