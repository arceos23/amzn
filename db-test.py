# Note: the module name is psycopg, not psycopg3
import psycopg

# Connect to an existing database
with psycopg.connect(
    "host=localhost port=5430 connect_timeout=10 user=postgres password=1234"
) as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # # Execute a command: this creates a new table
        # cur.execute(
        #     """
        #     CREATE TABLE test (
        #         id serial PRIMARY KEY,
        #         num integer,
        #         data text)
        #     """
        # )

        # # Pass data to fill a query placeholders and let Psycopg perform
        # # the correct conversion (no SQL injections!)
        # cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM test")
        print("here")
        print(cur.execute("SELECT * FROM test").fetchone())
        # will return (1, 100, "abc'def")

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        print("here")
        for record in cur.execute("SELECT * FROM test"):
            print(record)

        # Make the changes to the database persistent
        conn.commit()
        print("here")
