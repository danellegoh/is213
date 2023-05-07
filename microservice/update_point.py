# Upon Receiving New Transaction > create new transaction record and upload in transaction database
# After new transaction is logged > updates user database to increase points + update tier
# Updated tier + month to call for rewards available

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

import os
import sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# ensure that port number is changed accordingly
# ensure that reward database and user database and transaction database is in phpmyadmin

# URL for routing
transactionURL = os.environ.get('transactionURL')
userURL = os.environ.get('userURL')
rewardURL = os.environ.get('rewardURL')


@app.route("/update_point", methods=['POST'])
def receive_transaction():
    # Simple check of input format and data of the request are JSON
    # Receive json transaction input, json file must look like this
    # {
    #     "transaction_id": 8,
    #     "transaction_value": 20,
    #     "userEmail": "koo@gmail.com"
    # }
    if request.is_json:
        try:
            transaction = request.get_json()

            result = update_user(transaction)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "Error updating point internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def update_user(order):
    transaction_id = order['transaction_id']
    
    new_order_detail = {
        "transaction_value": order['transaction_value'], "userEmail": order['userEmail']}
    transaction_result = invoke_http(transactionURL + "/" + transaction_id, method='POST', json=new_order_detail)
    
    if transaction_result['code'] == 404:
        return transaction_result

# Update user database to log new transaction + update total point + update tier
    print('\n-----Invoking user microservice-----')
    print("this is the user email", transaction_result['data']['userEmail'])
    userEmail = transaction_result['data']['userEmail']
    user_result = invoke_http(
        userURL + "/" + userEmail, method='PUT') # , json=new_order_detail
    if user_result['code'] == 500:
        return {"message": "error at user"}
    print('Updated user total point and tier:', user_result)
    user_name = user_result['data']['name']
    print(user_name)
    user_total_points = user_result['data']['total_points']

# Using the user result > retrieve tier to check for available rewards
    print('\n-----Invoking reward microservice-----')
    print("this is the user email", transaction_result['data']['userEmail'])
    print(transaction_result)
    tier = user_result['data']['tier']
    month = str(datetime.now().month)
    special = '0'
    reward_result = invoke_http(
        rewardURL + "/" + month + '/' + tier + '/' + special, method='GET')
    print('Updated user total point and tier:', reward_result)
    if reward_result['code'] == 500:
        return {"message": "error at reward"}

    ## need to take into account the scenario that all rewards have been claimed
    ## error is because you're pulling on reward from the reward_result but there's only code and data being returned
        
    reward_result['reward']['name'] = user_name
    reward_result['reward']['email'] = userEmail
    reward_result['reward']['total_points'] = user_total_points
    return reward_result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)