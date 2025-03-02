import os
import time
import psycopg
import json

DESTINATION_FOLDER_NAME = "test-decompressed"
META_FOLDER = "meta"
REVIEW_FOLDER = "review"


def store_data():
    # Store data from files into normalized PostgreSQL database
    try:
        # Get all files in the destination folder
        destination_path = os.path.join(os.getcwd(), DESTINATION_FOLDER_NAME)
        category_folders = os.listdir(destination_path)

        # Store the decompressed files in the database
        with psycopg.connect(
            "host=localhost port=5430 connect_timeout=10 user=postgres password=1234"
        ) as conn:  # Connect to an existing database

            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                for category_folder in sorted(
                    category_folders
                ):  # Process products before reviews due to foreign key constraints
                    if category_folder[0] != ".":  # Skip hidden folders
                        category_path = os.path.join(destination_path, category_folder)
                        files = os.listdir(category_path)
                        for file in files:
                            start_time = time.perf_counter()
                            file_path = os.path.join(category_path, file)
                            # Store content into database
                            with open(file_path, "r") as f:
                                for line in f.readlines():
                                    data = json.loads(line)
                                    if META_FOLDER in category_folder:
                                        cur.execute(
                                            "INSERT INTO products (main_category, average_rating, title, parent_asin, price, store) VALUES (%s, %s, %s, %s, %s, %s)",
                                            (
                                                data["main_category"],
                                                data["average_rating"],
                                                data["title"],
                                                data["parent_asin"],
                                                data["price"],
                                                data["store"],
                                            ),
                                        )
                                    elif REVIEW_FOLDER in category_folder:
                                        print(data)
                                        cur.execute(
                                            "INSERT INTO reviews (rating, title, text, asin, parent_asin, user_id, created_at, verified_purchase, helpful_vote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                            (
                                                data["rating"],
                                                data["title"],
                                                data["text"],
                                                data["asin"],
                                                data["parent_asin"],
                                                data["user_id"],
                                                data["timestamp"],
                                                data["verified_purchase"],
                                                data["helpful_vote"],
                                            ),
                                        )
                                conn.commit()
                                end_time = time.perf_counter()
                                print(
                                    f"Successfully saved file {file_path} to database in {end_time - start_time} seconds.\n"
                                )
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


def main():
    try:
        store_data()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    main()
