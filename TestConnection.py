import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv('.env')

uri = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

driver = GraphDatabase.driver(uri, auth=(username, password))

# Try to connect to the database
try:
    with driver.session() as session:
        result = session.run("RETURN 1")
        print("Connection successful!")
except Exception as e:
    print("Failed to connect to the database:", e)
finally:
    # Close the driver when done
    driver.close()
