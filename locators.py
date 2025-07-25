from selenium.webdriver.common.by import By

all_locators = {
    "thumbnail": (By.CLASS_NAME, "thumbnail"),
    "title_link": (By.CLASS_NAME, "title"),
    "pagination_links": (By.CSS_SELECTOR, ".pagination li a"),
    "detail_title": (By.CSS_SELECTOR, "h1"),
    "detail_price": (By.CLASS_NAME, "price"),
    "detail_rating_star": (By.CSS_SELECTOR, ".ratings .glyphicon-star"),
    "detail_reviews": (By.CSS_SELECTOR, ".ratings > .pull-right"),
    "detail_description": (By.CLASS_NAME, "description"),
} 