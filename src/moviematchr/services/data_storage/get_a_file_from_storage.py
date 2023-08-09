import os
import io
from minio import Minio
from fastapi.responses import StreamingResponse

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


def get_a_file_from_storage(
        filename: str,
        media_type: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
):
    try:
        response = client.get_object(MINIO_BUCKET_NAME, filename)

        file_data = io.BytesIO()

        for data in response.stream(32 * 1024):
            file_data.write(data)

        file_data.seek(0)

        return StreamingResponse(file_data, media_type=media_type)

    except FileNotFoundError as error:
        print(f"File not found: {error}")
        return None
