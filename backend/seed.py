import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

def main():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
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
        
    seed_path = os.path.join(os.path.dirname(__file__), "..", "cypher", "seed.cypher")
    if not os.path.exists(seed_path):
        print(f"Error: Seed file not found at {seed_path}")
        sys.exit(1)
        
    with open(seed_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Split queries by newline or use a basic parser. Since MERGE statements don't use semicolons,
    # we can split by newline and filter out comments. Let's make sure we execute each line or construct
    # one single transaction with all MERGE commands. Doing one multi-line statement is highly efficient in Cypher!
    # Let's filter out lines that are comments or empty.
    cleaned_lines = []
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped and not stripped.startswith("//"):
            cleaned_lines.append(stripped)
            
    query = "\n".join(cleaned_lines)
    
    if not query:
        print("No statements found to seed.")
        sys.exit(0)
        
    print(f"Connecting to database to execute seed query...")
    
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            # First, optional check: show current node counts
            print("Running seeding transaction...")
            session.run(query)
            print("Database seeded successfully.")
            
            # Let's count the nodes of each type to verify
            print("\nVerification counts:")
            counts_query = """
            MATCH (n)
            RETURN labels(n)[0] AS label, count(n) AS count
            """
            res = session.run(counts_query)
            for record in res:
                print(f" - {record['label']}: {record['count']}")
                
            # Let's count relationship types to verify
            print("\nRelationship counts:")
            rel_query = """
            MATCH ()-[r]->()
            RETURN type(r) AS rel_type, count(r) AS count
            """
            res_rel = session.run(rel_query)
            for record in res_rel:
                print(f" - {record['rel_type']}: {record['count']}")
                
    except Exception as e:
        print(f"\nDatabase seeding failed: {e}")
        sys.exit(1)
    finally:
        if driver:
            driver.close()
            
    print("\nDatabase seeding completed successfully!")

if __name__ == "__main__":
    main()
