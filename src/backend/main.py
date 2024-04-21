from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
PORT = 5000

# Database connection setup
connection = pymysql.connect(
    host='mysql-svc',
    user='root',
    password='root',
    database='mysql'
)

# Routes
@app.route('/api/message', methods=['GET'])
def get_message():
    global message
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT message FROM messages')
            result = cursor.fetchone()
            if result:
                message = result[0]
        return jsonify({'message': message})
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve message from database', 'mysqlError': str(e)}), 500

@app.route('/api/message', methods=['POST'])
def update_message():
    global message
    new_message = request.json.get('newMessage')
    message = new_message
    try:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE messages SET message = %s', (new_message,))
            connection.commit()
        return jsonify({'message': message})
    except Exception as e:
        return jsonify({'error': 'Failed to update message in database', 'mysqlError': str(e)}), 500

@app.route('/api/store-message', methods=['POST'])
def store_message():
    new_message = request.json.get('newMessage')
    try:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO messages (message) VALUES (%s)', (new_message,))
            connection.commit()
        return jsonify({'message': new_message})
    except Exception as e:
        return jsonify({'error': 'Failed to store message in database', 'mysqlError': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
