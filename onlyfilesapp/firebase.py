import firebase_admin, os
from firebase_admin import credentials, storage


cred = credentials.Certificate("./onlyfiles-firebase.key.json")
firebase_admin.initialize_app(credential=cred, options={
    'storageBucket': os.environ.get('FIREBASE_STORAGE'),
})

FIREBASE_BUCKET = storage.bucket()

