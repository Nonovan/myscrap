import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


proxies = {
    "http": "http://USERNAME:PASSWORD@pr.oxylabs.io:7777",
    "https": "https://USERNAME:PASSWORD@pr.oxylabs.io:7777"
}

try:
    retry = Retry(
        total=5,
        backoff_factor=3,
        status_forcelist=[403, 429, 500, 502, 503, 504],
    )

    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)

    r = session.get("https://ip.oxylabs.io/", proxies=proxies, timeout=180)
    print(r.status_code)
    print(r.text)

except Exception as e:
    print(e)