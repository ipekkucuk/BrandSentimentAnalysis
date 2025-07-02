import json
import sqlite3
import requests
import math
from utils import get_product_id
from db_connector import DROP_TABLE_QUERY, INSERT_COMMENT_QUERY, CREATE_TABLE_QUERY
import time

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.128 Safari/537.36 Edg/122.0.2365.66",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.159 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/110.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Android 13; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0",
    "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.128 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.193 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",  # Do Not Track
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

comments_base_url = "https://apigw.trendyol.com/discovery-web-websfxsocialreviewrating-santral/product-reviews-detailed?&sellerId=341266&contentId={product_id}&page={page_number}&order=DESC&orderBy=Score&rates={rate}&channelId=1"

with open("products_urls.json", "r", encoding="utf-8") as f:
    products_data = json.load(f)

MAX_COMMENT_COUNT_IN_ONE_PAGE = 30

db_name = "reviews.db"
db_connection = sqlite3.connect(db_name)
cursor = db_connection.cursor()

cursor.execute(DROP_TABLE_QUERY)
cursor.execute(CREATE_TABLE_QUERY)

#for brand in products_data:
   # brand_products = products_data[brand]

for key in products_data:
    brand, category_name, parent_company = [x.strip() for x in key.split(",")]

    brand_products = products_data[key]
    counter = 0
    for product in brand_products:
        product_id = get_product_id(product["url"])

        for star_count, comment_count in enumerate(product["rates_count"], start=1):

            if product["all_review_count"]:
                page_count = math.ceil(product["all_review_count"] / MAX_COMMENT_COUNT_IN_ONE_PAGE)
            else:
                page_count = math.ceil(comment_count / MAX_COMMENT_COUNT_IN_ONE_PAGE)

            #page_count = math.ceil(product["all_review_count"] / max_comment_count_in_page) if product[
               ## "all_review_count"] else math.ceil(comment_count / max_comment_count_in_page)

            comments = []

            for page_number in range(0,page_count):
                complete_url = comments_base_url.format(product_id=product_id, page_number=page_number, rate=star_count)
                response = requests.get(complete_url, headers=headers)

                try:
                    json_data = json.loads(response.text)
                    comments += json_data['result']["productReviews"]["content"]
                except json.JSONDecodeError as e:
                    print("JSON parse error:", e)
                    print(response.text)  # İçeriği görsel olarak kontrol etmek istersen
                    breakpoint()


            if product["all_review_count"]:
                # Tüm yorumları al
                comments = comments
            else:
                # Sadece gerekli kadar yorumu al
                comments = comments[0:comment_count]

            counter += 1
            for comment in comments:
                comment_date = comment["commentDateISOtype"]
                comment_text = comment["comment"]
                comment_rate = comment["rate"]

                cursor.execute(INSERT_COMMENT_QUERY, (brand, comment_text, comment_date, comment_rate,))
                db_connection.commit()
