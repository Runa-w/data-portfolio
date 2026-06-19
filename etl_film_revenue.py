import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()
db_password = os.getenv('DB_PASSWORD')

# --- CONNECTIONS ---
# Source: dvdrental database
source = create_engine(f'postgresql+psycopg2://postgres:{db_password}@localhost:5432/dvdrental')

# Destination: projects database
destination = create_engine(f'postgresql+psycopg2://postgres:{db_password}@localhost:5432/projects')

# --- EXTRACT ---
# Pull raw data from deverental with a SQL query
query = """
    SELECT
        c.name AS category,
        SUM(p.amount) AS total_revenue,
        COUNT(r.rental_id) AS total_rentals
    FROM category c
    JOIN film_category fc ON c.category_id = fc.category_id
    JOIN film f ON fc.film_id = f.film_id
    JOIN inventory i ON f.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    JOIN payment p ON r.rental_id = p.rental_id
    GROUP BY c.name
    ORDER BY total_revenue DESC;
"""

print("Extracting data from dvdrental...")
df = pd.read_sql(query, source)

# --- TRANSFORM ---
# Add a revenue per rental column
print("Transforming data...")
df['revenue_per_rental'] = (df['total_revenue'] / df['total_rentals']).round(2)

# --- LOAD ---
# Write the result to the projects database as a new table
print("Loading data into projects database...")
df.to_sql('film_category_revenue', destination, if_exists='replace', index=False)

print("Done!")
print(df)