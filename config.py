class Server:
    def __init__(self, env):
        self.service_1 = {
            "dev": "http://localhost:8002",
            "stage": "",
            "rc": "",
        }[env]
        self.service_2 = {
            "dev": "",
            "stage": "",
            "rc": "",
        }[env]