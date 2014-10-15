import http.client
import urllib.request
from bs4 import BeautifulSoup

def connect(host, url):
    conn = http.client.HTTPConnection(host)
    conn.request("GET", url)
    response = conn.getresponse()

    soup = BeautifulSoup(response.read())
    conn.close()

    return soup

def download_bytes(url):
    with urllib.request.urlopen(url) as response:
        ret = []
        byte = None

        while byte != b"":
            byte = response.read(1)
            ret.append(byte)

        return b"".join(ret)
