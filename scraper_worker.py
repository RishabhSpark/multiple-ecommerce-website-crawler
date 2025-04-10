# # scraper_worker.py

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# import threading
# import time

# # Lock for print synchronization
# print_lock = threading.Lock()

# def create_driver():
#     """Create and configure Chrome WebDriver instance."""
#     options = webdriver.ChromeOptions()
#     options.add_argument('--disable-blink-features=AutomationControlled')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument("start-maximized")
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
#     # options.add_argument('--headless')  # Uncomment if needed
#     options.accept_insecure_certs = True

#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
#     return driver

# def scrape_website(config):
#     driver = create_driver()
#     product_links = set()

#     try:
#         for collection_url in config["collections"]:
#             with print_lock:
#                 print(f"\n[{config['name']}] Scraping: {collection_url}")

#             driver.get(collection_url)
#             time.sleep(5)
#             body = driver.find_element(By.TAG_NAME, "body")
#             no_new_product_count = 0
#             MAX_NO_NEW_COUNT = 5

#             while no_new_product_count < MAX_NO_NEW_COUNT:
#                 for _ in range(10):
#                     driver.execute_script("window.scrollBy(0, 500);")
#                     time.sleep(1)
#                 time.sleep(3)

#                 prev_count = len(product_links)

#                 if config["name"] == "NykaaFashion":
#                     try:
#                         new_links = driver.execute_script("""
#                             const links = new Set();
#                             document.querySelectorAll('a[href*="/p/"]').forEach(a => {
#                                 links.add(a.href);
#                             });
#                             document.querySelectorAll('[onclick]').forEach(el => {
#                                 const onclick = el.getAttribute('onclick');
#                                 const match = onclick && onclick.match(/location.href='(\\/p\\/[^']+)'/);
#                                 if (match) {
#                                     links.add("https://www.nykaafashion.com" + match[1]);
#                                 }
#                             });
#                             document.querySelectorAll('[data-href]').forEach(el => {
#                                 const val = el.getAttribute('data-href');
#                                 if (val && val.includes('/p/')) {
#                                     links.add("https://www.nykaafashion.com" + val);
#                                 }
#                             });
#                             return Array.from(links);
#                         """)
#                         for url in new_links:
#                             product_links.add(url)
#                     except Exception as e:
#                         with print_lock:
#                             print(f"[{config['name']}] JS extraction failed: {e}")
#                 else:
#                     try:
#                         all_links = driver.find_elements(By.TAG_NAME, "a")
#                         for link in all_links:
#                             try:
#                                 url = link.get_attribute("href")
#                                 if url and config["product_pattern"] in url:
#                                     product_links.add(url)
#                             except Exception:
#                                 continue
#                     except Exception as e:
#                         with print_lock:
#                             print(f"[{config['name']}] Warning during link extraction: {e}")

#                 with print_lock:
#                     print(f"[{config['name']}] Found {len(product_links)} product links so far...")

#                 if len(product_links) == prev_count:
#                     no_new_product_count += 1
#                 else:
#                     no_new_product_count = 0

#                 for _ in range(4):
#                     body.send_keys(Keys.PAGE_UP)
#                     time.sleep(1)

#         filename = f"{config['name'].replace(' ', '_').lower()}_product_links.csv"
#         with open(filename, "w", encoding="utf-8") as f:
#             for link in product_links:
#                 f.write(link + "\n")

#         with print_lock:
#             print(f"[{config['name']}] Saved {len(product_links)} links to {filename}")

#     except Exception as e:
#         with print_lock:
#             print(f"[{config['name']}] Error: {e}")

#     finally:
#         driver.quit()



# For max_products
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time

# Lock for print synchronization
print_lock = threading.Lock()

def create_driver():
    """Create and configure Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    # options.add_argument('--headless')  # Uncomment if needed
    options.accept_insecure_certs = True

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Required for GitHub Actions
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.binary_location = "/usr/bin/chromium-browser"  # Required for GitHub Actions
    service = Service("/usr/bin/chromedriver")             # GitHub Actions path
    return webdriver.Chrome(service=service, options=options)

def scrape_website(config):
    driver = create_driver()
    product_links = set()
    max_products = config.get("max_products", float("inf"))

    try:
        for collection_url in config["collections"]:
            with print_lock:
                print(f"\n[{config['name']}] Scraping: {collection_url}")

            driver.get(collection_url)
            time.sleep(5)
            body = driver.find_element(By.TAG_NAME, "body")
            no_new_product_count = 0
            MAX_NO_NEW_COUNT = 5

            while no_new_product_count < MAX_NO_NEW_COUNT:
                for _ in range(10):
                    driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(1)
                time.sleep(3)

                prev_count = len(product_links)

                if config["name"] == "NykaaFashion":
                    try:
                        new_links = driver.execute_script("""
                            const links = new Set();
                            document.querySelectorAll('a[href*="/p/"]').forEach(a => {
                                links.add(a.href);
                            });
                            document.querySelectorAll('[onclick]').forEach(el => {
                                const onclick = el.getAttribute('onclick');
                                const match = onclick && onclick.match(/location.href='(\\/p\\/[^']+)'/);
                                if (match) {
                                    links.add("https://www.nykaafashion.com" + match[1]);
                                }
                            });
                            document.querySelectorAll('[data-href]').forEach(el => {
                                const val = el.getAttribute('data-href');
                                if (val && val.includes('/p/')) {
                                    links.add("https://www.nykaafashion.com" + val);
                                }
                            });
                            return Array.from(links);
                        """)
                        for url in new_links:
                            product_links.add(url)
                            if len(product_links) >= max_products:
                                with print_lock:
                                    print(f"[{config['name']}] Reached max limit of {max_products} products.")
                                break
                        if len(product_links) >= max_products:
                            break
                    except Exception as e:
                        with print_lock:
                            print(f"[{config['name']}] JS extraction failed: {e}")
                else:
                    try:
                        all_links = driver.find_elements(By.TAG_NAME, "a")
                        for link in all_links:
                            try:
                                url = link.get_attribute("href")
                                if url and config["product_pattern"] in url:
                                    product_links.add(url)
                                    if len(product_links) >= max_products:
                                        with print_lock:
                                            print(f"[{config['name']}] Reached max limit of {max_products} products.")
                                        break
                            except Exception:
                                continue
                        if len(product_links) >= max_products:
                            break
                    except Exception as e:
                        with print_lock:
                            print(f"[{config['name']}] Warning during link extraction: {e}")

                with print_lock:
                    print(f"[{config['name']}] Found {len(product_links)} product links so far...")

                if len(product_links) == prev_count:
                    no_new_product_count += 1
                else:
                    no_new_product_count = 0

                for _ in range(4):
                    body.send_keys(Keys.PAGE_UP)
                    time.sleep(1)

        filename = f"{config['name'].replace(' ', '_').lower()}_product_links.csv"
        with open(filename, "w", encoding="utf-8") as f:
            for link in product_links:
                f.write(link + "\n")

        with print_lock:
            print(f"[{config['name']}] Saved {len(product_links)} links to {filename}")

    except Exception as e:
        with print_lock:
            print(f"[{config['name']}] Error: {e}")

    finally:
        driver.quit()
