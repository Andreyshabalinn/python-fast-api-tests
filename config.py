class Server:
    def __init__(self, env):
        self.service = {
            "dev": "",
            "beta": "",
            "rc": "http://localhost:8000/api/",
        }[env]