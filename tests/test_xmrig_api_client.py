from xmrig_auto_throttler.xmrig_api_client import XmrigClient


def test_xmrig_api_client():
    client = XmrigClient("http://127.0.0.1:8810", "foobar")
    config = client.get_config()
    client.set_config(config)
