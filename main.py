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

def get_working_proxies(proxy_list, limit=50, needed=3):
    working = []
    for proxy in proxy_list[:limit]:
        if test_proxy(proxy):
            working.append(proxy)
            if len(working) >= needed:
                break
    return working

print(f"Testing first 10 proxies out of {len(proxy_list)}...")

def make_request_with_rotation(url, working_proxies, max_attempts=3):
    for attempt in range(max_attempts):
        if not working_proxies:
            print("No more working proxies to try.")
            return None

        proxy = working_proxies[attempt % len(working_proxies)]
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        try:
            response = requests.get(url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                print(f"Success using proxy: {proxy}")
                return response
        except Exception:
            print(f"Proxy {proxy} failed, rotating to next one...")

    print("All attempts failed.")
    return None

working_proxies = get_working_proxies(proxy_list)
print(f"\nFound {len(working_proxies)} working proxies: {working_proxies}")

result = make_request_with_rotation("https://api.ipify.org?format=json", working_proxies)
if result:
    hidden_ip = result.json()["ip"]
    print(f"Your IP through the proxy is now: {hidden_ip}")