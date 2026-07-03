from typing import Protocol
from pydantic import BaseModel


class PresignedUpload(BaseModel):
    upload_url: str
    file_url: str
    key: str


class StorageProvider(Protocol):
    def create_presigned_upload_url(
        self, filename: str, content_type: str
    ) -> PresignedUpload:
        pass

    def delete_file(self, url: str) -> None:
        pass


class FakeR2StorageProvider:
    def create_presigned_upload_url(
        self, filename: str, content_type: str
    ) -> PresignedUpload:
        key = f"customers/{filename}"

        return PresignedUpload(
            upload_url=f"https://fake-r2-upload-url.com/{key}",
            file_url=f"https://cdn.example.com/{key}",
            key=key,
        )

    def delete_file(self, url: str) -> None:
        # delete here
        pass
