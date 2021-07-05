class BaseApiResponse:
    def __init__(self):
        self.errors = []
        self.data = None

    def add_error(self, err):
        self.errors.append(err)

    def make(self):
        payload = {
            "errors": self.errors,
        }

        if self.data:
            payload["data"] = self.data

        return payload


class VpnAccessApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.config = None

    def make(self):
        return {
            "errors": self.errors,
            "config": self.config
        }
