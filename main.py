# app.py
from google.cloud import storage
from PIL import Image
import io
import os

# GCP setup
SOURCE_BUCKET = 'source-bucket-cc-assignment'
DEST_BUCKET = 'destination-bucket-cc-assignment'
THUMBNAIL_SIZE = (128, 128)

def generate_thumbnail(image_data):
    img = Image.open(io.BytesIO(image_data))
    img.thumbnail(THUMBNAIL_SIZE)
    thumb_io = io.BytesIO()
    img.save(thumb_io, format='JPEG')
    thumb_io.seek(0)
    return thumb_io

def process_images():
    client = storage.Client.from_service_account_json("service-account.json")
    source_bucket = client.get_bucket(SOURCE_BUCKET)
    dest_bucket = client.get_bucket(DEST_BUCKET)

    blobs = source_bucket.list_blobs()

    for blob in blobs:
        if blob.content_type.startswith('image/'):
            # Download image
            image_data = blob.download_as_bytes()

            # Generate thumbnail
            thumbnail_data = generate_thumbnail(image_data)

            # Upload thumbnail to destination bucket
            thumbnail_blob = dest_bucket.blob(f'thumbnails/{blob.name}')
            thumbnail_blob.upload_from_file(thumbnail_data, content_type='image/jpeg')
            print(f"Thumbnail for {blob.name} created and uploaded.")

if __name__ == '__main__':
    process_images()
