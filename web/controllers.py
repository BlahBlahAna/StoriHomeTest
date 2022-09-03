import logging
from domains import Transaction, SummaryObj
from handlers import EmailHandler, FileHandler, SummaryHandler


class FileController:
    def read_file_content(self):
        try:
            transaction_checker = Transaction()
            file_handler = FileHandler(transaction_checker)
            file_handler.read_file_content()
        except Exception as ex:
            logging.error(ex)
            return {"message": "There was an error when reading file content"}

        return {"message": "File content read and loaded into database"}


class SummaryController:
    def make_summary(self):
        try:
            summary_obj = SummaryObj()
            summary_handler = SummaryHandler(summary_obj)
            summary = summary_handler.make_summary()
        except Exception as ex:
            logging.error(ex)
            return {"message": "There was an error when creating the summary"}

        return {"message": summary}


class EmailController:
    def send_email(self):
        try:
            summary = SummaryObj()
            summary_handler = SummaryHandler(summary)

            complete_summary = summary_handler.make_summary()

            email_handler = EmailHandler(complete_summary)
            email_handler.send_email()
        except Exception as ex:
            logging.error(ex)
            return {"message": "There was an error sending the email"}

        return {"message": "Email successfully sent to user"}
