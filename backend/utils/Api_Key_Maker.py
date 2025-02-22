import secrets
import base64

def generate_api_key(length=48):
    token = secrets.token_bytes(length)
    return base64.b64encode(token).decode('utf-8')

api_key = generate_api_key()
print("Clé API générée :", api_key)