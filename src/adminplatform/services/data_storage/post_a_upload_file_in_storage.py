import os
from minio import Minio
from fastapi import UploadFile

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


def post_a_upload_file_in_storage(file: UploadFile, filename: str) -> bool:
    try:
        # Upload du fichier vers le bucket
        file.file.seek(0, os.SEEK_END)
        length = file.file.tell()
        file.file.seek(0)

        client.put_object(MINIO_BUCKET_NAME, filename, file.file, length=length)
        return True

    except Exception as error:
        print(f"Upload error : {error}")
        return False
