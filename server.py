import os
import json

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_session import Session
from flask_migrate import Migrate
from langchain.schema import messages_from_dict

from ai import AI

SESSION_TYPE = 'memcache'

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://mybot:TITsDXDtrfspEByvLsNx2WPZ1qsceh3N@dpg-cihslbtgkuvojjb72m60-a.oregon-postgres.render.com/mybot_e8fh"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

CORS(app, origins=["127.0.0.1:3000"])
db = SQLAlchemy(app)
admin = Admin(app, name='MyBots', template_mode='bootstrap3')
sess = Session()
sess.init_app(app)
migrate = Migrate(app, db)

ai = AI()

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    prompt = db.Column(db.Text)
    notes = db.relationship('Note', backref='bot', lazy='dynamic')
    history = db.Column(db.Text)

    def __repr__(self):
        return f'<Bot {self.name}>'
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    #bot_id = db.relationship("Bot", backref="note", lazy='dynamic', primaryjoin="Note.id == Bot.id")
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.id'))

    def __repr__(self):
        return f'<Note {self.id}>'
    
# Add administrative views here
admin.add_view(ModelView(Bot, db.session))
admin.add_view(ModelView(Note, db.session))

with app.app_context():
    db.create_all()
    
@app.route('/bot', methods=['POST'])
@cross_origin()
def create_bot():
    data = request.get_json()  # Get the JSON data from the request
    # Perform any necessary processing on the data

    bot_name = data.get("bot_name", "")
    # reply = ai.get_reply(message)

    bot = Bot(name=bot_name, prompt="this is a prompt")
    db.session.add(bot)
    db.session.commit()
    print(bot.id)

    # Create a JSON response
    response = {
        'message': 'Success',
        'data': bot.id
    }

    return jsonify(response)  # Return the JSON response

# @app.route('/bot/history/<bot_id>', methods=['GET'])
# def get_bot_history(bot_id):
#     matched_bots = Bot.query.filter_by(id=bot_id).all()
#     if matched_bots is None or len(matched_bots) == 0:
#         return jsonify({ "error": "Cannot find bot" }), 500

#     bot = matched_bots[0]

#     response = {
#         'data': bot.history,
#         'status': 'Success'
#     }

#     return jsonify(response)

@app.route('/<bot_id>', methods=['POST'])
@cross_origin()
def process_request(bot_id):
    data = request.get_json()  # Get the JSON data from the request

    if bot_id is None:
        bot_id = 1

    matched_bots = Bot.query.filter_by(id=bot_id).all()
    if matched_bots is None or len(matched_bots) == 0:
        return jsonify({ "error": "Cannot find bot" }), 500

    bot = matched_bots[0]
    message = data.get("message", "")
    reply, info, history = ai.get_reply(message, bot.history, bot.prompt)

    if history is not None:
        bot.history = json.dumps(history)
        db.session.add(bot)
        db.session.commit()

    record_info = None
    if info is not None and len(info) > 0:
        record_info = ",".join(info)
        note = Note(content=record_info, bot_id=bot.id)
        db.session.add(note)
        db.session.commit()
        print("Recorded info: {0}".format(record_info))

    # Create a JSON response
    response = {
        'message': 'Success',
        'data': reply,
        'recorded_info': record_info
    }

    # final_response = jsonify(response).headers.add('Access-Control-Allow-Origin', '*')
    return jsonify(response)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:3000')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

if __name__ == '__main__':
    app.run()