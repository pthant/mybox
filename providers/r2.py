import boto3
import botocore

from settings import Config

class R2Client:
    def __init__(self, config: Config) -> None:
        self.__config = config
        self.ENDPOINT = f"https://{config.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
        self.__client = self.__make_r2_client()

    def __make_r2_client(self):
        return boto3.client(
            "s3",
            endpoint_url=self.ENDPOINT,
            aws_access_key_id=self.__config.R2_APP_KEY,
            aws_secret_access_key=self.__config.R2_APP_SECRET,
            config=botocore.client.Config(signature_version="s3v4")
        )

    def get_upload_presigned_url(self, key: str) -> str:
        return self.__client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.__config.R2_BUCKET,
                "Key": key,
            },
            ExpiresIn=3600
        )