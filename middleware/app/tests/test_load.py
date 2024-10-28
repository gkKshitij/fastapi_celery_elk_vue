# tests/test_load.py
from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(1, 5)  # Simulate a delay between user actions

    @task
    def get_items(self):
        self.client.get("/items/1")