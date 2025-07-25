import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import all_locators

BASE_URL = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
OUTPUT_FILE = "output.json"
WAIT_TIME = 10
TARGET_PRODUCT = "Asus VivoBook X441NA-GA190"

def get_driver():
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    return driver


def extract_laptop_data_from_detail(driver):
    try:
        title = driver.find_element(*all_locators["detail_title"]).text.strip()
    except Exception:
        title = ''
    try:
        price = driver.find_element(*all_locators["detail_price"]).text.strip()
    except Exception:
        price = ''
    try:
        rating = len(driver.find_elements(*all_locators["detail_rating_star"]))
    except Exception:
        rating = 0
    try:
        reviews_text = driver.find_element(*all_locators["detail_reviews"]).text.strip()
        reviews_count = int(reviews_text)
    except Exception:
        reviews_count = 0
    try:
        description = driver.find_element(*all_locators["detail_description"]).text.strip()
    except Exception:
        description = ''
    product_url = driver.current_url
    return {
        "title": title,
        "price": price,
        "rating": rating,
        "reviews_count": reviews_count,
        "product_url": product_url,
        "description": description
    }


def main():
    driver = get_driver()
    driver.get(BASE_URL)
    found = False
    while not found:
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_all_elements_located(all_locators["thumbnail"])
        )
        cards = driver.find_elements(*all_locators["thumbnail"])
        for card in cards:
            try:
                title_elem = card.find_element(*all_locators["title_link"])
                product_title = title_elem.get_attribute("title")
                if product_title.strip() == TARGET_PRODUCT:
                    link = title_elem.get_attribute("href")
                    driver.execute_script("window.open(arguments[0], '_self')", link)
                    WebDriverWait(driver, WAIT_TIME).until(
                        EC.presence_of_element_located(all_locators["detail_description"])
                    )
                    data = extract_laptop_data_from_detail(driver)
                    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                        json.dump([data], f, indent=2, ensure_ascii=False)
                    print(f"Scraping complete. Results saved to {OUTPUT_FILE}")
                    found = True
                    break
            except Exception:
                continue
        if found:
            break
        # Pagination: look for next button
    driver.quit()
    if not found:
        print(f"Product '{TARGET_PRODUCT}' not found.")

if __name__ == "__main__":
    main() 