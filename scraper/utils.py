import re

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

