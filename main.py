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

def get_working_proxies(proxy_list, limit=50, needed=3):
    working = []
    for proxy in proxy_list[:limit]:
        if test_proxy(proxy):
            working.append(proxy)
            if len(working) >= needed:
                break
    return working

working_proxies = get_working_proxies(proxy_list)
print(f"\nFound {len(working_proxies)} working proxies: {working_proxies}")

if working_proxies:
    chosen_proxy = working_proxies[0]
    proxies = {
        "http": f"http://{chosen_proxy}",
        "https": f"http://{chosen_proxy}"
    }
    response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=5)
    hidden_ip = response.json()["ip"]
    print(f"Your IP through the proxy is now: {hidden_ip}")
else:
    print("No working proxies found this time — try running again.")