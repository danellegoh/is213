from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
CORS(app)

# comment out when using docker
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/transaction'

# uncomment when using docker 
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Transaction(db.Model):
    __tablename__ = 'transaction'
    transaction_id = db.Column(db.String(64), primary_key=True)
    transaction_value = db.Column(db.Integer, nullable=False)
    userEmail = db.Column(db.String(300), nullable=False)

    def __init__(self, transaction_id, transaction_value, userEmail):
        self.transaction_id = transaction_id
        self.transaction_value = transaction_value
        self.userEmail = userEmail

    def json(self):
        return {
            "transaction_id": self.transaction_id, 
            "transaction_value": self.transaction_value, 
            "userEmail": self.userEmail
            }

# connected to database and works
# returns all transaction value


@app.route("/transaction")
def get_all():
    transaction_data = Transaction.query.all()
    if len(transaction_data):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transaction": [transaction.json() for transaction in transaction_data]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no transaction."
        }
    ), 404

# updates transaction database with new transaction record


@app.route("/transaction/<string:transaction_id>", methods=['POST'])
def create_transaction(transaction_id):
    data = request.get_json()
    transaction = Transaction(transaction_id, data["transaction_value"], data["userEmail"])
    try:
        db.session.add(transaction)
        db.session.commit()
    except:
        return jsonify(
            {
                'code': 404,
                'message': 'An error has occured when adding transaction'
            }
        ), 404

    return jsonify( 
        {
            'code': 200,
            'data': transaction.json()
        }
    ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
