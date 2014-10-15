from bs4 import BeautifulSoup
import http.client

def connect(host, url):
    conn = http.client.HTTPConnection(host)
    conn.request("GET", url)
    response = conn.getresponse()
    
    soup = BeautifulSoup(response.read())
    conn.close()

    return soup
