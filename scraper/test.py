import requests
from bs4 import BeautifulSoup as bs
import json
import re


all_review_count = False
test_count = 32

if all_review_count:
    print("all_review_count")

if test_count:
    print("test_count")

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# }
# url = "https://apigw.trendyol.com/discovery-web-websfxsocialreviewrating-santral/product-reviews-detailed?&sellerId=341266&contentId=820032774&page=0&order=DESC&orderBy=Score&channelId=1"
#
# response = requests.get(url, headers=headers)
#
# json_data = json.loads(response.text)
#
# comments = json_data['result']


# with open("products_urls.json", "r", encoding="utf-8") as f:
#     data = json.load(f)
#     print(data)
#


comments = [1, 2, 3, 4]
print(comments[:100])

def get_product_id(url: str) -> str:
    """
    Extracts product_id from a Trendyol product URL using regex.

    :param url: Reviews page URL address
    :return: product_id as string
    """
    match = re.search(r"-p-(\d+)/yorumlar", url)
    if match:
        return match.group(1)
    raise ValueError("Product ID not found in the URL.")


print(get_product_id("https://www.trendyol.com/old-spice/sprey-deodorant-150-ml-wolfthornx2-p-36490546/yorumlar?boutiqueId=61&merchantId=341266"))
