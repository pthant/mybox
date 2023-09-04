from dropbox import Dropbox, DropboxOAuth2FlowNoRedirect
from dropbox.files import ListFolderResult, FolderMetadata, CommitInfo, WriteMode
from dropbox.files import GetTemporaryLinkResult, GetTemporaryLinkResult

from settings import Config

class DropboxClient:
    def __init__(self, config: Config) -> None:
        self.__config = config
        self.__access_token = config.DB_INIT_ACCESS_TOKEN or self.login()
        self.__client = Dropbox(oauth2_access_token=self.__access_token)
    
    def get_upload_presigned_url(self, key: str) -> str:
        commit_info = CommitInfo(path=f"/{key}", mode=WriteMode.overwrite)
        res: GetTemporaryLinkResult = self.__client.files_get_temporary_upload_link(commit_info)
        # print(f"{res=}")
        return res.link
    
    def get_view_presigned_url(self, key: str) -> str:
        res: GetTemporaryLinkResult = self.__client.files_get_temporary_link(f"/{key}")
        # print(f"{res=}")
        return res.link

    def login(self) -> str:
        config = self.__config
        auth_flow = DropboxOAuth2FlowNoRedirect(
            config.DB_APP_KEY,
            config.DB_APP_SECRET,
        )

        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()

        try:
            oauth_result = auth_flow.finish(auth_code)
            # with open("token.txt", "a") as f:
                # f.write(oauth_result.access_token)
            print(f"{oauth_result.access_token=}")
            return oauth_result.access_token
        except Exception as e:
            print('Error: %s' % (e,))
            exit(1)
