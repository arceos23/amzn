import os
import gzip
import shutil
import time

SOURCE_FOLDER_NAME = "downloads"
DESTINATION_FOLDER_NAME = "decompressed"
GZIP_MAGIC_NUMBER = b"\x1F\x8B"
GZIP_FILE_EXTENSION = ".gz"


def main():
    try:
        # Get all category folders in the source folder
        downloads_path = os.path.join(os.getcwd(), SOURCE_FOLDER_NAME)
        category_folders = os.listdir(downloads_path)

        # Store the decompressed files in each category folder
        for category_folder in category_folders:
            # Get all files in the category folder
            category_path = os.path.join(downloads_path, category_folder)
            files = os.listdir(category_path)

            # Store each file
            for file in files:
                file_path = os.path.join(category_path, file)
                try:
                    start_time = time.perf_counter()
                    with gzip.open(file_path, "rb") as f_in:
                        output_file_path = file_path[:-3].replace(
                            SOURCE_FOLDER_NAME, DESTINATION_FOLDER_NAME
                        )

                        # Make folder to store decompressed file
                        last_slash_index = output_file_path.rfind("/")
                        output_folder_path = output_file_path[:last_slash_index]
                        os.makedirs(output_folder_path, exist_ok=True)

                        # Store decompressed file
                        with open(output_file_path, "wb") as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    end_time = time.perf_counter()
                    print(
                        f"Successfully unzipped file {file_path} in {end_time - start_time} seconds.\n"
                    )
                except gzip.BadGzipFile:
                    print(f"Invalid gzip file found. {err=}, {type(err)=}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    main()
