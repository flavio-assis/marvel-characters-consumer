class MockResponse:
    def __init__(self, json_data, status_code, *args, **kwargs):
        self.json_data = json_data
        self.status_code = status_code
        super().__init__(*args, **kwargs)

    async def json(self):
        return self.json_data

    def text(self):
        return f'{self.json_data}'

    def status(self):
        return self.status_code
