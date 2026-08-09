import requests

def get_proxy_list():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
    response = requests.get(url)
    proxy_list = response.text.strip().split("\r\n")
    return proxy_list

def test_proxy(proxy):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
    except Exception:
        return False
    return False

proxy_list = get_proxy_list()
print(f"Testing first 10 proxies out of {len(proxy_list)}...")

for proxy in proxy_list[:50]:
    working = test_proxy(proxy)
    if working:
        print(f"{proxy} - WORKING")
    else:
        print(f"{proxy} - failed")