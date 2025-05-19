from google.cloud import storage
import os
import datetime

class Bucket:
    def __init__(self):
        gs = storage.Client.from_service_account_json(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        self.bucket = gs.get_bucket(os.getenv('BUCKET_NAME'))

    def upload_file(self, file_name: str) -> str:
        blob = self.bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        return blob.public_url

