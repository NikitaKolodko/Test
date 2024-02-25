from flask import Flask, request, jsonify
import sqlite3
import requests
import time
app = Flask(__name__)
DATABASE = '/users.db'
def initialize_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, balance REAL)''')
    users_data = [
        ('user1', 5000),
        ('user2', 7000),
        ('user3', 9000),
        ('user4', 11000),
        ('user5', 15000)
    ]
    c.executemany('INSERT INTO users (username, balance) VALUES (?, ?)', users_data)
    conn.commit()
    conn.close()
initialize_database()
class User:
    def __init__(self, user_id, username, balance):
        self.id = user_id
        self.username = username
        self.balance = balance

    @staticmethod
    def get_user_by_id(user_id):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user_data = c.fetchone()
        conn.close()
        if user_data:
            return User(*user_data)
        else:
            return None

    @staticmethod
    def get_user_by_username(username):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user_data = c.fetchone()
        conn.close()
        if user_data:
            return User(*user_data)
        else:
            return None

    def update_balance(self, new_balance):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, self.id))
        conn.commit()  # Фиксация изменений
        conn.close()
        
def fetch_weather(city):
    api_key = 'ad01378a74f742abeb7eb5284539a7ef'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        return temperature
    else:
        return None
@app.route('/update_balance', methods=['POST'])
def update_balance():
    data = request.get_json()
    user_id = data.get('userId')
    city = data.get('city')
    user = User.get_user_by_id(user_id)
    if user:
        temperature = fetch_weather(city)
        if temperature is not None:
            new_balance = user.balance + temperature
            if new_balance >= 0:
                user.update_balance(new_balance)
                return jsonify({'message': 'Balance updated successfully'}), 200
            else:
                return jsonify({'error': 'Insufficient balance'}), 400
        else:
            return jsonify({'error': 'Failed to fetch weather data'}), 500
    else:
        return jsonify({'error': 'User not found'}), 404
if __name__ == '__main__':
    app.run(debug=True)
