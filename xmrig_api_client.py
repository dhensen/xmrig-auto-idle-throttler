import requests
from typing import Dict


class XmrigClient:
    def __init__(self, base_url, token) -> None:
        super().__init__()
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {token}',
        })
        self.base_url = base_url

    def get_config(self):
        response = self._session.get(f'{self.base_url}/2/config')
        return response.json()

    def set_config(self, config: Dict):
        response = self._session.put(f'{self.base_url}/2/config', json=config)
        print(response.status_code)
        print(response)


if __name__ == "__main__":
    client = XmrigClient('http://127.0.0.1:8810', 'foobar')
    config = client.get_config()
    print(config)
    client.set_config(config)
