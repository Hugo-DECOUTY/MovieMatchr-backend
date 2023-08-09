import os
import base64
import io
from minio import Minio

from dotenv import load_dotenv

load_dotenv()

# Récupérez les informations de configuration à partir des variables d'environnement
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

client = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)


def post_a_base64_file_in_storage(file: str, filename: str) -> bool:
    try:
        upload_file_bytes: bytes = base64.b64decode(file.encode("utf-8"))
        upload_file = io.BytesIO(upload_file_bytes)

        client.put_object(
            MINIO_BUCKET_NAME, filename, upload_file, length=len(upload_file_bytes)
        )
        return True

    except Exception as error:
        print(f"Upload error : {error}")
        return False
