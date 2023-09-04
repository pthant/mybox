import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from settings import Config
from providers import R2Client, DropboxClient
from utils import FileMetadata, save_metadata, gen_key

config = Config()
r2 = R2Client(config)
dbx = DropboxClient(config)

app = FastAPI()

@app.post("/file/upload")
def get_upload_presigned_url():
    key = gen_key()
    r2_url = r2.get_upload_presigned_url(key)
    dbx_url = dbx.get_upload_presigned_url(key)

    return {"id": key, "r2_upload_url": r2_url, "db_upload_url": dbx_url}

@app.post("/file/upload:ack")
def upload_ack(metadata: FileMetadata):
    save_metadata(metadata)
    return {"success": True}


app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
