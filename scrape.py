import os
import time
import requests
from bs4 import BeautifulSoup

AMAZON_REVIEWS_URL = "https://amazon-reviews-2023.github.io/"
TIMEOUT_SECONDS = "5"
TABLE_ID = "grouped-by-category"
ANCHOR_TAG = "a"
DOWNLOAD_ATTRIBUTE = "download"
HREF = "href"
FOLDER_NAME = "downloads"
TARGET_PRODUCT_CATEGORIES = ["Subscription_Boxes", "Magazine_Subscriptions"]


def main():
    try:
        # Get HTML from URL
        r = requests.get(AMAZON_REVIEWS_URL, TIMEOUT_SECONDS)
        r.raise_for_status()  # Raises an error for a 4XX or 5XX status code

        # Retrieve the reviews and metadata download links for each product category
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find(id=TABLE_ID)
        links = table.find_all(ANCHOR_TAG)
        download_links = [
            link
            for link in links
            if link.get(DOWNLOAD_ATTRIBUTE) == "" and link.get(HREF) is not None
        ]

        # Save review and metadata files for the target download category
        for link in download_links:
            for target_product_category in TARGET_PRODUCT_CATEGORIES:
                if target_product_category in link[HREF]:
                    url = link[HREF]
                    tokens = url.strip().split("/")

                    # Make folder to store downloaded file
                    category = tokens[-2]
                    folder_path = os.path.join(os.getcwd(), f"{FOLDER_NAME}/{category}")
                    os.makedirs(folder_path, exist_ok=True)

                    # Store file
                    filename = tokens[-1]
                    file_path = os.path.join(folder_path, filename)
                    start_time = time.perf_counter()
                    download_response = requests.get(url, TIMEOUT_SECONDS)
                    with open(file_path, "wb") as file:
                        file.write(download_response.content)
                    end_time = time.perf_counter()
                    print(
                        f"Successfully saved file from {url} to {file_path} in {end_time - start_time} seconds.\n"
                    )
                    break
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    main()
