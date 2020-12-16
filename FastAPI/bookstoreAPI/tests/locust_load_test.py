from locust import HttpUser, task


class BookstoreLocustTasks(HttpUser):
    # @task
    # def token_test(self):
    #     self.client.post("/token", dict(username="test", password="test"))

    @task
    def test_post_user(self):
        user_dict = {
            "name": "test",
            "password": "test",
            "mail": "a@b.com",
            "role": "admin"
        }
        auth_header = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0Iiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNjA4NTEzMDQ3fQ.-Nqui1lGUbPavLTSSgLZxA6ig-U4MhxhDb9pdvkvCR8"}
        self.client.post("/v1/user", json=user_dict, headers=auth_header)

    # def on_start(self):
    #     self.client.post("/token", json=dict(username="test", password="test"))
