import os
from typing import Protocol


class StorageProvider(Protocol):
    def upload_file(self, filename: str, content: bytes) -> str:
        pass

    def delete_file(self, url: str) -> None:
        pass


class LocalStorageProvider:
    def upload_file(self, filename: str, content: bytes) -> str:
        os.makedirs("uploads", exist_ok=True)

        path = f"uploads/{filename}"

        with open(path, "wb") as file:
            file.write(content)

        return path

    def delete_file(self, url: str) -> None:
        if os.path.exists(url):
            os.remove(url)


class R2StorageProvider:
    def upload_file(self, filename: str, content: bytes) -> str:
        # upload here
        return f"https://r2.cloudflare.com/{filename}"

    def delete_file(self, url: str) -> None:
        # delete here
        pass
