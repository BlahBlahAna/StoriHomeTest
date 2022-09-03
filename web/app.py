from flask import jsonify
from flask_restful import Api, Resource

from config import app
from controllers import EmailController, FileController, SummaryController


api = Api(app)


class LoadTransactions(Resource):
    def get(self):
        file_controller = FileController()
        response = file_controller.read_file_content()
        return jsonify(response)


class Summary(Resource):
    def get(self):
        summary_controller = SummaryController()
        response = summary_controller.make_summary()
        return jsonify(response)


class Email(Resource):
    def get(self):
        email_controller = EmailController()
        response = email_controller.send_email()
        return jsonify(response)


api.add_resource(LoadTransactions, "/load_transactions")
api.add_resource(Summary, "/view_summary")
api.add_resource(Email, "/send_email")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
