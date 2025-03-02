from fastapi import FastAPI
import psycopg

app = FastAPI()


@app.get("/products")
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
                SELECT id, main_category, title, average_rating, rating_number, features, description, price, store, parent_asin
                FROM products;
            """
                )
            }


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
