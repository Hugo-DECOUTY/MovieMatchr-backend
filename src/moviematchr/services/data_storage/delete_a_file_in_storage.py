import os
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


def delete_a_file_in_storage(filename: str):
    try:
        client.remove_object(MINIO_BUCKET_NAME, filename)
        return True

    except FileNotFoundError as error:
        print(f"File not found: {error}")
        return False
