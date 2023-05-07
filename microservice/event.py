from flask import Flask ,request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from os import environ

app = Flask(__name__)
CORS(app)

# comment out when using docker
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/events'

# uncomment when using docker 
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Event(db.Model):
    __tablename__ = 'events'
    
    eventid = db.Column(db.Integer, nullable= False, primary_key= True)
    eventtitle = db.Column(db.String(1000), nullable= False)
    eventdescription = db.Column(db.String(1000), nullable= False)
    eventdate = db.Column(db.String(20), nullable = False)
    starttime = db.Column(db.String(20), nullable = False)
    endtime = db.Column(db.String(20), nullable = False)
    maxpax = db.Column(db.Integer)
    currentpax = db.Column(db.Integer)
    
    def __init__(self, eventid, eventtitle, eventdescription, eventdate, starttime, endtime, maxpax, currentpax):
        self.eventid = eventid
        self.eventtitle = eventtitle
        self.eventdescription = eventdescription
        self.eventdate = eventdate
        self.starttime = starttime
        self.endtime = endtime
        self.maxpax = maxpax
        self.currentpax = currentpax
        
    def json(self):
        return {
            'eventid': self.eventid,
            'eventtitle': self.eventtitle,
            'eventdescription': self.eventdescription,
            'eventdate': self.eventdate,
            'starttime': self.starttime,
            'endtime': self.endtime,
            'maxpax': self.maxpax,
            'currentpax': self.currentpax
        }

@app.route('/events', methods= ['GET'])
def get_all():
    EventsList = Event.query.all()
    if EventsList:
        return jsonify(
            {
                "code": 200,
                "data":
                    {
                        "events": [event.json() for event in EventsList]
                    }
        }
    )
    return {
        "code": 404,
        "message": "There are no events currently."
    }
    
    
@app.route('/events/<string:eventtitle>', methods= ['GET'])
def get_event(eventtitle):
    event = Event.query.filter_by(eventtitle=eventtitle).first()
    if event:
        return jsonify(
            {
                "code": 200,
                "event": event.json()
        }
    )
    return jsonify(
        {
            'code': 404,
            'message': 'Event not found.'
        }), 404
    
@app.route('/events', methods= ['POST'])
def create_event():
    eventid = Event.query.count() + 1
    
    data = request.get_json()
    
    event = Event(eventid, **data, currentpax = 0)
    try:
        db.session.add(event)
        db.session.commit()
    except:
        return jsonify(
            {
                'code': 404,
                'message': 'An error has occured when adding event'
            }
        ), 404
    return jsonify( 
        {
            'code': 200,
            'data': event.json()
        }
    ), 201
    
@app.route('/events/<string:eventtitle>', methods=['DELETE'])
def delete_event(eventtitle):
    event = Event.query.filter_by(eventtitle=eventtitle).first()
    
    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify(
                {
                    'code': 200,
                    'message': 'Event deleted successfully'
                }
            ), 200
    except:
        return jsonify(
            {
                'code': 404,
                'message': 'An error has occured when deleting event'
            }
        )
        
@app.route('/events/<string:eventtitle>', methods=['PUT'])
def add_participant_num(eventtitle):
    event = Event.query.filter_by(eventtitle=eventtitle).first()
    if event.currentpax < event.maxpax:
        event.currentpax += 1
        try:
            db.session.commit()
            return jsonify(
                {
                    'code': 200,
                    'message': 'Participant added successfully'
                }
            ), 200
        except:
            return jsonify(
                {
                    'code': 500,
                    'message': 'An error has occurred when updating event'
                }
            ), 500
    else:
        return jsonify(
            {
                'code': 400,
                'message': 'Event is full'
            }
        ), 400
    
if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage events ...")
    app.run(host='0.0.0.0', port=3333, debug=True)
    
    

    
    
    