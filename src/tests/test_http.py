import unittest
from fastapi.testclient import TestClient

from web_interface import asgi_app  # assuming your FastAPI app is defined here

class TestHTTP(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(asgi_app.asgi_application)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "HoyoverseBoosting"})


    def test_get_screen_infos(self):
        response = self.client.get("/get/screen/infos")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()["infos"]) > 0)
        print(response.json()["infos"])
    def test_get_screen_monitor_numbers(self):
        response = self.client.get("/get/screen/monitorNumbers")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()["numbers"]) > 0)
        print(response.json()["numbers"])