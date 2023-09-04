import uuid

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

import boto3
from botocore.client import Config


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    R2_ACCOUNT_ID: str
    R2_APP_KEY: str
    R2_APP_SECRET: str
    R2_BUCKET: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

R2_ENDPOINT = f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

def get_r2_client():
    config = Config(signature_version="s3v4")
    r2 = boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=settings.R2_APP_KEY,
        aws_secret_access_key=settings.R2_APP_SECRET,
        config=config
    )
    return r2

def _get_upload_presigned_url(r2, key):
    return r2.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.R2_BUCKET,
            "Key": key,
        },
        ExpiresIn=3600
    )

r2 = get_r2_client()

class FileMetadata(BaseModel):
    id: str
    file_type: str
    display_name: str

def gen_key() -> str:
    uu = uuid.uuid4()
    return uu.hex

def save_metadata(metadata: FileMetadata):
    with open("metadata.csv", "a") as f:
        f.write(",".join([metadata.id, metadata.file_type, metadata.display_name]) + "\n")

app = FastAPI()


@app.post("/upload/ack")
def upload_ack(metadata: FileMetadata):
    save_metadata(metadata)
    return {"success": True}

@app.post("/upload")
def get_upload_presigned_url():
    key = gen_key()
    url = _get_upload_presigned_url(r2, key)
    return {"id": key, "r2_upload_url": url}

app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
