from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ

app = Flask(__name__)
CORS(app)

# comment out when using docker
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/rewards'

# uncomment when doing docker 
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Reward(db.Model):
    __tablename__ = 'rewards'
    
    tier = db.Column(db.String(10), nullable = False, primary_key = True)
    month = db.Column(db.String(10), nullable = False, primary_key = True)
    rewardid = db.Column(db.String(100), nullable = False, primary_key = True)
    rewardname = db.Column(db.String(100), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    discount = db.Column(db.Float(precision = 2), nullable = False)
    special = db.Column(db.Boolean, nullable = False)

    
    def __init__(self, tier, month, rewardid, rewardname, discount, quantity, special):
        self.tier = tier
        self.month = month
        self.rewardid = rewardid
        self.rewardname = rewardname
        self.discount = discount
        self.quantity = quantity
        self.special = special
    
    def json(self):
        return {
            'tier': self.tier,
            'month': self.month,
            'rewardid': self.rewardid,
            'rewardname': self.rewardname,
            'discount': self.discount,
            'quantity': self.quantity,
            'special': self.special
        }
        
@app.route('/rewards')
def get_all():
    RewardList = Reward.query.all()
    if RewardList:
        return jsonify( {
            'code': 200,
            'data': {
                'rewards': [reward.json() for reward in RewardList]
                }
            }
        )
    return {
        'code': 400,
        'message': 'There are no available rewards'
    }
    
@app.route('/rewards/<string:month>/<string:tier>/<string:special>')
def get_reward(month, tier, special):
    reward = Reward.query.filter_by(month=month,tier=tier, special=special).first()
    if reward:
        if reward.quantity != 0:
            return jsonify( {
                    'code': 200,
                    'reward': reward.json()
                } 
            )
        else:
            return jsonify( {
                    'code': 200,
                    'message': 'Rewards have been all claimed.',
                    "reward": reward.json()
                } 
            )
    return jsonify( 
        {
            'code': 404,
            'message': 'Reward not found'
        }), 404

@app.route('/rewards/<string:tier>/<string:month>', methods=['POST'])
def create_reward(tier, month):
    # collect data from input
    data = request.get_json()
    # filter the potential reward out from database using month and tier
    reward = Reward.query.filter_by(month=month,tier=tier).first()
    
    # if a reward is returned for that month and tier, need to check if it is a duplicate reward
    if reward:
        # check if the reward name extracted out from the database is the same as the reward name in the input
        if['rewardname'] == data["rewardname"]:
         # if the same then display error
            return jsonify( {
                'code': 404,
                'data': {
                    'rewardid': reward.rewardid
                },
                'message': 'Reward already exists'
            })
    
    rewardid = Reward.query.count() + 1
    reward = Reward(tier, month, rewardid, data["rewardname"], data["discount"], data["quantity"], data["special"])
    try:
        db.session.add(reward)
        db.session.commit()
    except:
        return jsonify(
            {
                'code': 404,
                'message': 'An error has occured when adding reward'
            }
        )
    return jsonify( 
            {
                'code': 200,
                'data': {
                    'rewardid': reward.json()
                },
            }
        ), 200
    
# @app.route('/rewards/<string:tier>', methods=['PUT'])
# def edit_reward(tier):
#     month = datetime.now().month
#     reward = Reward.query.filter_by(month=month,tier=tier).first()
#     if reward.quantity > 0:
#         reward.quantity -= 1
        
#         try:
#             db.session.commit()
#         except:
#             return jsonify(
#                 {
#                     'code': 404,
#                     'message': 'An error has occurred when updating reward'
#                 }
#             )
            
#         return jsonify( {
#             'code': 200,
#             'data': {
#                 "reward": reward.json()
#             },
#             'message': 'Reward claimed successfully'
#         })
    
#     else:
#         return jsonify( {
#             'code': 404,
#             'message': 'Reward all claimed'
#         })

@app.route('/rewards/<string:rewardid>', methods=['PUT'])
def edit_reward(rewardid):
    reward = Reward.query.filter_by(rewardid=rewardid).first()
    if reward.quantity > 0:
        reward.quantity -= 1
        # return str(reward.quantity)
        
        try:
            db.session.commit()
        except:
            return jsonify(
                {
                    'code': 404,
                    'message': 'An error has occurred when updating reward'
                }
            )
            
        return jsonify( {
            'code': 200,
            'data': {
                "reward": reward.json()
            },
            'message': 'Reward claimed successfully'
        })
    
    else:
        return jsonify( {
            'code': 404,
            'message': 'Reward all claimed'
        })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5002, debug= True)