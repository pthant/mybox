import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from settings import Config
from providers import R2Client
from utils import FileMetadata, save_metadata, gen_key

config = Config()
r2 = R2Client(config)

app = FastAPI()

@app.post("/file/upload")
def get_upload_presigned_url():
    key = gen_key()
    url = r2.get_upload_presigned_url(key)
    t_url = r2.get_upload_presigned_url("thumb" + key)
    return {"id": key, "r2_upload_url": url, "db_upload_url": t_url}

@app.post("/file/upload:ack")
def upload_ack(metadata: FileMetadata):
    save_metadata(metadata)
    return {"success": True}


app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
