import psycopg
from elasticsearch_dsl import Document, Keyword, Text, connections
import os


class Product(Document):
    id = Keyword()
    title = Text()

    class Index:
        name = "product"

    def save(self, **kwargs):
        return super().save(**kwargs)


def store_elastic_search():
    try:
        with psycopg.connect(
            "host=localhost port=5430 connect_timeout=10 user=postgres password=1234"
        ) as conn:
            connections.create_connection(
                hosts="http://localhost:9200",
                basic_auth=(
                    os.environ.get("ES_LOCAL_USER"),
                    os.environ.get("ES_LOCAL_PASSWORD"),
                ),
            )

            # Create the mappings in Elasticsearch
            Product.init()

            # Store the products from PostgreSQL in Elasticsearch
            with conn.cursor() as cur:
                for record in cur.execute(
                    """
                SELECT id, title FROM products;
            """
                ):
                    Product(id=record[0], title=record[1]).save()

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


def main():
    try:
        store_elastic_search()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    main()
