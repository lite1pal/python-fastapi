import os
import unittest

from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:////tmp/python-fastapi-test.db"

from db import Base, SessionLocal, engine
from main import app
from repositories.customers import seed_customers
from services import customers as customer_services


class FailingEmailProvider:
    def send_customer_created(
        self,
        *,
        to_email: str,
        customer_name: str,
        company: str | None,
    ) -> None:
        raise RuntimeError("email provider unavailable")


class FailingQueueProvider:
    def enqueue_customer_notes_summary(self, *, customer_id: int) -> None:
        raise RuntimeError("queue unavailable")


class FailingStorageProvider:
    def create_presigned_upload_url(
        self, filename: str, content_type: str
    ):
        raise RuntimeError("storage unavailable")


class CustomerApiTests(unittest.TestCase):
    def setUp(self) -> None:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            seed_customers(db)
        finally:
            db.close()
        self.client = TestClient(app)
        self.email_provider = customer_services.email_provider
        self.queue_provider = customer_services.queue_provider
        self.storage_provider = customer_services.storage_provider

    def tearDown(self) -> None:
        customer_services.email_provider = self.email_provider
        customer_services.queue_provider = self.queue_provider
        customer_services.storage_provider = self.storage_provider

    def test_root_exposes_docs_link(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "service": "customer-api",
                "docs": "/docs",
            },
        )

    def test_delete_archives_customer(self) -> None:
        response = self.client.delete("/customers/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "archived")

    def test_create_customer_succeeds_when_email_provider_fails(self) -> None:
        customer_services.email_provider = FailingEmailProvider()

        response = self.client.post(
            "/customers",
            json={
                "name": "Alex Stone",
                "email": "alex@example.com",
                "company": "Example Co",
                "status": "lead",
                "notes": "Asked for pricing details.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "alex@example.com")

    def test_summarize_notes_returns_503_when_queue_enqueue_fails(self) -> None:
        customer_services.queue_provider = FailingQueueProvider()

        response = self.client.post("/customers/1/summarize_notes")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(),
            {"detail": "Unable to queue notes summary right now"},
        )

    def test_upload_url_returns_502_when_storage_provider_fails(self) -> None:
        customer_services.storage_provider = FailingStorageProvider()

        response = self.client.post(
            "/customers/1/upload_url",
            json={
                "filename": "avatar.png",
                "content_type": "image/png",
            },
        )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.json(),
            {"detail": "Unable to create upload URL right now"},
        )


if __name__ == "__main__":
    unittest.main()
