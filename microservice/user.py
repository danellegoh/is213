from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
CORS(app)

# comment out when using docker
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/user'

# uncomment when doing docker 
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    userEmail = db.Column(db.String(64), primary_key=True)
    total_points = db.Column(db.Integer, nullable=False)
    tier = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(64), nullable = False)

    def __init__(self, userEmail, total_points, tier, name):
        self.userEmail = userEmail
        self.total_points = total_points
        self.tier = tier
        self.name = name

    def json(self):
        return {"userEmail": self.userEmail, "total_points": self.total_points, "tier": self.tier, "name": self.name}

@app.route("/user")

#connected to database and works
def get_all():
    user_data = User.query.all()
    if len(user_data):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "user": [user.json() for user in user_data]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no books."
        }
    ), 404

#Updates tier + User points with user email as input
#Returns User email, total point, tier 
@app.route("/user/<string:userEmail>", methods=['PUT'])
def update_points(userEmail):
    user = User.query.filter_by(userEmail=userEmail).first()
    if (user):
        current_point = user.total_points

        # RMB TO CHANGE THIS BACK
        updated_point = current_point + 50
        
        if updated_point < 300:
            updated_tier = "Bronze"
        elif updated_point >= 300 and updated_point < 600:
            updated_tier = "Silver"
        elif updated_point >= 600:
            updated_tier = "Gold"

        try: 
            user.userEmail =  userEmail
            user.total_points = updated_point
            user.tier = updated_tier
            user.name = user.name
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "user": "Error receiving data from user"
                    },
                    "message": "An error occurred updating the user."
                }
            ), 500
        return jsonify(
        {
            "code": 201,
            "data": user.json(),
            "message" : "User data updated successfully!"
        }
    ), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)