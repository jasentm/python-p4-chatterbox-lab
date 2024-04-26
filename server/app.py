from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        q = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
        return make_response(q)
    elif request.method == 'POST':
        new_message = Message(
            body = request.json.get('body'),
            username = request.json.get('username')
        )
        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()
        return make_response(message_dict, 201)

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    q = Message.query.filter(Message.id == id).first()
    
    if request.method == 'GET':
        return make_response(q.to_dict())
    elif request.method == 'PATCH':
        for attr in request.json:
            setattr(q, attr, request.json.get(attr))
        
        db.session.add(q)
        db.session.commit()

        return make_response(q.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(q)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."
        }

        return make_response(response_body)

if __name__ == '__main__':
    app.run(port=5555)
