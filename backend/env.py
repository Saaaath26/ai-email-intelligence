import requests

BASE_URL = "https://ai-email-backend-novs.onrender.com"

class EmailEnv:
    def __init__(self):
        self.emails = []
        self.index = 0

    def reset(self):
        res = requests.get(BASE_URL + "/emails")
        data = res.json()

        if "error" in data:
            raise Exception("Login required")

        self.emails = data["emails"]
        self.index = 0

        return {"email": self.emails[self.index]["text"]}

    def step(self, action):
        email = self.emails[self.index]

        correct = email["category"].lower()
        predicted = action.lower()

        reward = 1.0 if predicted == correct else 0.3

        self.index += 1
        done = self.index >= len(self.emails) or self.index >= 5

        next_obs = {}
        if not done:
            next_obs = {"email": self.emails[self.index]["text"]}

        return {
            "observation": next_obs,
            "reward": reward,
            "done": done,
            "error": None
        }

    def state(self):
        return {"index": self.index}