import firebase_admin
from firebase_admin import credentials, auth, firestore

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def create_user(email, password):
    user = auth.create_user(
        email=email,
        password=password
    )
    return user.uid
    
def verify_token(id_token):
    decoded_token = auth.verify_id_token(id_token)
    return decoded_token