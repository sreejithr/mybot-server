import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from ai import AI

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://mybot:TITsDXDtrfspEByvLsNx2WPZ1qsceh3N@dpg-cihslbtgkuvojjb72m60-a.oregon-postgres.render.com/mybot_e8fh"
# 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ai = AI()

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    prompt = db.Column(db.Text)

    def __repr__(self):
        return f'<Bot {self.name}>'
    
@app.route('/bot', methods=['POST'])
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


@app.route('/', methods=['POST'])
def process_request():
    data = request.get_json()  # Get the JSON data from the request
    # Perform any necessary processing on the data

    message = data.get("message", "")
    reply = ai.get_reply(message)

    # Create a JSON response
    response = {
        'message': 'Success',
        'data': reply
    }

    return jsonify(response)  # Return the JSON response

if __name__ == '__main__':
    app.run()