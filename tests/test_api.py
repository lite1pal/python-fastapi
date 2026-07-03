import unittest

from fastapi.testclient import TestClient

from main import app


class CustomerApiTests(unittest.TestCase):
    def setUp(self) -> None:
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
