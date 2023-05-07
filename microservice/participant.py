from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from os import environ

app = Flask(__name__)
CORS(app)

# comment out when using docker 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/participant'

# uncomment when using docker 
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Participant(db.Model):
    __tablename__ = 'participant'
    
    userEmail = db.Column(db.String(64), nullable= False, primary_key=True)
    eventid = db.Column(db.Integer, nullable= False, primary_key = True)
    
    def __init__(self, userEmail, eventid):
        self.userEmail = userEmail
        self.eventid = eventid
        
    def json(self):
        return {
            'userEmail': self.userEmail,
            'eventid': self.eventid
        }

# get all participanting list 
@app.route('/participants', methods=['GET'])
def get_all():
    ParticipantsList = Participant.query.all()
    if ParticipantsList:
        return {
            'code': 200,
            'data': 
                {
                    'participants': [participant.json() for participant in ParticipantsList]
                }
        }
    return {
        'code': 400,
        'message': 'There are no participants'
    }

# get all participant's events
@app.route('/participants/<string:userEmail>', methods=['GET'])
def get_participant_events(userEmail):
    EventsList = Participant.query.filter_by(userEmail=userEmail)
    if EventsList:
        return {
            'code': 200,
            'data':
                {
                    'events': [event.json() for event in EventsList]
                }
        }
    return {
        'code': 400,
        'message': 'This participant did not sign up for any events.'
    }

# get all event's participants
@app.route('/participants/event<string:eventid>', methods=['GET'])
def get_events_participants(eventid):
    Event = Participant.query.filter_by(eventid=eventid).all()
    if not Event:
        return {
            'code': 400,
            'message': 'This event does not exist.'
        }
    else:
        ParticipantsList = Participant.query.filter_by(eventid=eventid).all()
        if ParticipantsList:
            return {
                'code': 200,
                'data':
                    {
                        'participants': [participant.json() for participant in ParticipantsList]
                    }
            }
        else: 
            return {
                'code': 400,
                'message': 'This event does not have any sign ups yet.'
            }

# add participant to event
@app.route('/participants/<string:userEmail>/<string:eventid>', methods=['POST'])
def add_participants(userEmail, eventid):
    Participated = Participant.query.filter_by(eventid=eventid, userEmail=userEmail).first()
    if Participated:

        return {
            'code': 404,
            'message': 'Participant has already signed up for this event'
        }
        
    participating = Participant(userEmail, eventid)

    try: 
        db.session.add(participating)
        db.session.commit()
    except:
        print(404)
        return jsonify(
            {
                'code': 404,
                'message': 'An error has occured when adding participant to event'
            }
        ), 404
    return jsonify(
        {
            'code': 200,
            'data': participating.json()
        }
    ), 201
    
# remove participant from event   
@app.route('/participants', methods=['DELETE'])
def delete_participant():
    data = request.get_json()
    eventid = data["eventid"]
    userEmail = data["userEmail"]
    RemoveParticipant = Participant.query.filter_by(eventid=eventid, userEmail=userEmail).first()
    if RemoveParticipant:
        try: 
            db.session.delete(RemoveParticipant)
            db.session.commit()
        except:
            return jsonify(
                {
                    'code': 404,
                    'message': 'An error has occured when removing participant to event'
                }
            ), 404
        return jsonify(
            {
                'code': 200,
                'message': 'Participant removed from event successfully'
            }
        )
    return jsonify(
        {
            'code': 404,
            'message': 'Participant did not sign up for this event.'
        }
    ), 404

# remove all participants from event
@app.route('/participants/<string:eventid>', methods=['DELETE'])
def delete_event_participant(eventid):
    RemoveEvent = Participant.query.filter_by(eventid=eventid).all()
    if RemoveEvent:
        try: 
            for participant in RemoveEvent:
                db.session.delete(participant)
                db.session.commit()
            
        except:
            return jsonify(
                {
                    'code': 404,
                    'message': 'An error has occured when removing all participants from events'
                }
            ), 404
            
        return jsonify(
                {
                    'code': 200,
                    'message': 'All participants removed from this event successfully'
                }
            ), 200
        
    return jsonify(
        {
            'code': 404,
            'message': 'There are no participants to remove from this event. This event do not have any sign ups'
        }
    ), 404
    
if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage participants ...")
    app.run(host='0.0.0.0', port=3334, debug=True)