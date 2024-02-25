import requests
import json
from app import User

def update_balance_by_username(username, city):
    url = 'http://127.0.0.1:5000/update_balance'
    user = User.get_user_by_username(username)
    if user:
        data = {'userId': user.id, 'city': city}
        response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            print(f"Balance for user {username} updated successfully.")
        else:
            print("Failed to update balance.")
    else:
        print(f"User {username} not found.")

# Пример использования:
