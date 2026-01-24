from locust import HttpUser, task, between
import random


class LaboralSaludUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        """Called when a simulated user starts"""
        # Login or initial setup if needed
        pass

    @task(3)
    def view_ausentismos(self):
        """Most common action - weight 3"""
        self.client.get("/ausentismos/")

    @task(2)
    def view_entidades(self):
        """Second most common - weight 2"""
        self.client.get("/entidades/")

    @task(1)
    def view_home(self):
        """Less common - weight 1"""
        self.client.get("/")

    @task(1)
    def view_reports(self):
        """Less common - weight 1"""
        self.client.get("/reportes/")