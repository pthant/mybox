import uuid
import csv

from pydantic import BaseModel

class FileMetadata(BaseModel):
    id: str
    file_type: str
    display_name: str

class FileMetadataWithUrl(FileMetadata):
    url: str

def gen_key() -> str:
    uu = uuid.uuid4()
    return uu.hex

def save_metadata(metadata: FileMetadata):
    with open("metadata.csv", "a") as f:
        f.write(",".join([metadata.id, metadata.file_type, metadata.display_name]) + "\n")

def load_metadata() -> list[dict]:
    with open("metadata.csv", "r") as f:
        return list(csv.DictReader(f, fieldnames=("id", "file_type", "display_name")))
