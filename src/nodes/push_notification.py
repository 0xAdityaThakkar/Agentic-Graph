import os
import requests

def send_push_notification(message: str):

    PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
    PUSHOVER_APP_KEY = os.getenv("PUSHOVER_APP_KEY")
    if not PUSHOVER_USER_KEY or not PUSHOVER_APP_KEY:
        print("PUSHOVER_USER_KEY or PUSHOVER_APP_KEY not set in environment variables.")
        return

    payload = {
        "token": PUSHOVER_APP_KEY,
        "user": PUSHOVER_USER_KEY,  # Replace with your user key
        "message": message,
    }

    response = requests.post("https://api.pushover.net/1/messages.json", data=payload)

    if response.status_code == 200:
        print("Push notification sent successfully.")
    else:
        print(f"Failed to send push notification. Status code: {response.status_code}")
        print(f"Response: {response.text}")
