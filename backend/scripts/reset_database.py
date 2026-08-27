import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv


def main():
    # Load environment variables from the .env file located at the project root
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    if not os.path.exists(env_path):
        print(f"Error: Environment file not found at {env_path}")
        sys.exit(1)

    load_dotenv(dotenv_path=env_path)

    uri = os.getenv("COGNODB_URI")
    username = os.getenv("COGNODB_USERNAME")
    password = os.getenv("COGNODB_PASSWORD")

    if not all([uri, username, password]):
        print("Error: Missing database credentials in environment variables.")
        sys.exit(1)

    print(f"Connecting to database at {uri}...")
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            print("\nWiping the entire graph database... This operation is destructive and cannot be undone.")
            session.run("MATCH (n) DETACH DELETE n")
            print("Database wiped successfully.")
    except Exception as e:
        print(f"\nReset script failed: {e}")
        sys.exit(1)
    finally:
        if driver:
            driver.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()
