from locust import HttpUser, task, between
import random

class AuthServiceUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8000"  # URL base de tu API

    @task
    def register(self):
        random_id = random.randint(1000, 9999)
        register_data = {
            "nombre": "testuser",
            "email": f"testuser{random_id}@example.com",
            "password": "password123"
        }
        response = self.client.post("/auth/register", json=register_data)
        if response.status_code == 200:
            print("Registro exitoso")
        else:
            print("Error en el registro:", response.json())
