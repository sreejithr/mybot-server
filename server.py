from flask import Flask, request, jsonify
from flask_cors import CORS
from ai import AI

app = Flask(__name__)
CORS(app)

ai = AI()

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