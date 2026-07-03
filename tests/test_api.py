import os
import unittest

from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:////tmp/python-fastapi-test.db"

from db import Base, SessionLocal, engine
from main import app
from repositories.customers import seed_customers


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


if __name__ == "__main__":
    unittest.main()
