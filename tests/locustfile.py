from locust import HttpUser, task, between


class ChatbotUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def health(self):
        self.client.get("/health")

    @task
    def chat(self):
        self.client.post(
            "/chat",
            json={
                "message": "Explain Artificial Intelligence."
            }
        )