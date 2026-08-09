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

def get_working_proxies(proxy_list, limit=50, needed=3):
    working = []
    for proxy in proxy_list[:limit]:
        if test_proxy(proxy):
            working.append(proxy)
            if len(working) >= needed:
                break
    return working

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

working_proxies = []

while True:
    print("\n--- IP Hider Menu ---")
    print("1. Check my real IP")
    print("2. Fetch and test proxies")
    print("3. Hide my IP")
    print("4. Quit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        response = requests.get("https://api.ipify.org?format=json")
        real_ip = response.json()["ip"]
        print(f"Your real IP is: {real_ip}")
    elif choice == "2":
        proxy_list = get_proxy_list()
        working_proxies = get_working_proxies(proxy_list)
        print(f"Found {len(working_proxies)} working proxies: {working_proxies}")
    elif choice == "3":
        if not working_proxies:
            print("No working proxies yet — choose option 2 first.")
        else:
            result = make_request_with_rotation("https://api.ipify.org?format=json", working_proxies)
            if result:
                hidden_ip = result.json()["ip"]
                print(f"Your IP through the proxy is now: {hidden_ip}")
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, try again.")