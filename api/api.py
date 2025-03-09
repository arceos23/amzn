from fastapi import FastAPI
import psycopg
from elasticsearch_dsl import connections
import os
from elasticsearch_dsl import Search

app = FastAPI()


@app.get("/products")
async def root(title=""):
    try:
        if not title:
            with psycopg.connect(
                "host=localhost port=5430 connect_timeout=10 user=postgres password=1234"
            ) as conn:
                with conn.cursor() as cur:
                    return {
                        record
                        for record in cur.execute(
                            """
                        SELECT id, main_category, title, average_rating, rating_number, features, description, price, store, parent_asin
                        FROM products;
                    """
                        )
                    }

        connections.create_connection(
            hosts="http://localhost:9200",
            basic_auth=(
                os.environ.get("ES_LOCAL_USER"),
                os.environ.get("ES_LOCAL_PASSWORD"),
            ),
        )
        s = Search(index="product").query("match", title=title)
        response = s.execute()
        return [hit for hit in response]

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


@app.get("/reviews")
async def root():
    # Connect to an existing database
    with psycopg.connect(
        "host=localhost port=5430 connect_timeout=10 user=postgres password=1234"
    ) as conn:
        with conn.cursor() as cur:
            return {
                record
                for record in cur.execute(
                    """
                SELECT id, rating, title, text, asin, parent_asin, user_id, created_at, verified_purchase, helpful_vote
                FROM reviews;
            """
                )
            }
