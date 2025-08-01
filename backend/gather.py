import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app
cred = credentials.Certificate(r"E:\Qloo_Project\backend\firebase-key.json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Fetch all feedback documents
feedback_docs = db.collection('userFeedback').stream()

# Structure to store data
user_sessions = {}

# Process each feedback entry
for doc in feedback_docs:
    data = doc.to_dict()
    user_id = data.get('userId')
    session_id = data.get('sessionId')
    preference = data.get('preference')
    feedback = data.get('feedback')

    if not user_id or not session_id:
        continue  # skip invalid data

    if user_id not in user_sessions:
        user_sessions[user_id] = {}

    if session_id not in user_sessions[user_id]:
        user_sessions[user_id][session_id] = []

    user_sessions[user_id][session_id].append({
        'preference': preference,
        'feedback': feedback
    })

# Print extracted info
for user_id, sessions in user_sessions.items():
    print(f"\nUser ID: {user_id}")
    for session_id, feedbacks in sessions.items():
        print(f"  Session ID: {session_id}")
        for fb in feedbacks:
            print(f"    Preference: {fb['preference']}, Feedback: {fb['feedback']}")
