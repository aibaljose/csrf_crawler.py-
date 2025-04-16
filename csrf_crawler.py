import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

visited = set()

def is_csrf_protected(form):
    for input_tag in form.find_all("input"):
        if 'csrf' in input_tag.get("name", "").lower():
            return True
    return False

def scan_for_csrf_forms(url):
    try:
        session = requests.Session()
        response = session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        print(f"\nScanning: {url}")
        forms = soup.find_all("form")
        if not forms:
            print("No forms found on this page.")
            return

        for i, form in enumerate(forms, 1):
            action = form.get("action")
            method = form.get("method", "get").upper()
            csrf = is_csrf_protected(form)

            print(f"\nForm #{i}")
            print(f"Action: {action}")
            print(f"Method: {method}")
            print(f"CSRF Token Present: {'✅' if csrf else '❌'}")

    except Exception as e:
        print(f"[!] Error scanning {url}: {e}")

def crawl(url, depth=1):
    if url in visited or depth <= 0:
        return
    visited.add(url)

    scan_for_csrf_forms(url)

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a", href=True):
            new_url = urljoin(url, link['href'])
            if new_url.startswith(url):
                crawl(new_url, depth - 1)
    except Exception as e:
        print(f"[!] Crawler error: {e}")

if __name__ == "__main__":
    target_url = input("Enter target URL (e.g., http://localhost/dvwa): ").strip()
    crawl(target_url, depth=2)
