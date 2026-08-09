import requests


def get_proxy_list():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
    response =requests.get(url)
    proxy_list =response.text.strip().split("\r\n")
    return proxy_list

proxies = get_proxy_list()
print(f"Found {len(proxies)} proxies")
for proxy in proxies [:5]:
    print(proxy)