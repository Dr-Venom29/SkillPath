import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

def main():
    # Read environment variables from project root .env
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    if not os.path.exists(env_path):
        print(f"Error: {env_path} does not exist.")
        sys.exit(1)
        
    print(f"Loading environment variables from: {env_path}")
    load_dotenv(dotenv_path=env_path)
    
    uri = os.getenv("COGNODB_URI")
    username = os.getenv("COGNODB_USERNAME")
    password = os.getenv("COGNODB_PASSWORD")
    
    if not all([uri, username, password]):
        print("Error: Missing database credentials in environment variables.")
        print(f"COGNODB_URI: {uri}")
        print(f"COGNODB_USERNAME: {username}")
        print(f"COGNODB_PASSWORD: {'***' if password else None}")
        sys.exit(1)
        
    print(f"Connecting to: {uri} as user: {username}")
    
    driver = None
    try:
        # 2. Create Neo4j driver
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        # 3. Verify connectivity
        print("Verifying connectivity...")
        driver.verify_connectivity()
        print("Connection successful")
        
        # 4. Run a tiny Cypher query: RETURN 1 AS result
        print("Running initial read query...")
        with driver.session() as session:
            result = session.run("RETURN 1 AS result")
            record = result.single()
            if record:
                print(f"Result: {record['result']}")
            else:
                print("Failed to run initial query.")
                sys.exit(1)
        
        test_node_id = "test-skill-123"
        test_node_name = "Test Skill Node"
        
        # 5. Test a write: CREATE (s:Skill {id: $id, name: $name}) RETURN s
        print(f"Testing parameterized write (CREATE) for node ID '{test_node_id}'...")
        with driver.session() as session:
            write_query = """
            CREATE (s:Skill {
                id: $id,
                name: $name
            })
            RETURN s.id AS id, s.name AS name
            """
            write_result = session.run(write_query, id=test_node_id, name=test_node_name)
            record = write_result.single()
            if record:
                print(f"Successfully created node: {record['id']} ('{record['name']}')")
            else:
                print("Write query failed to return created node.")
                sys.exit(1)
                
        # 6. Test a read: MATCH (s:Skill) RETURN s
        print("Testing read (MATCH) for the created node...")
        with driver.session() as session:
            read_query = """
            MATCH (s:Skill {id: $id})
            RETURN s.id AS id, s.name AS name
            """
            read_result = session.run(read_query, id=test_node_id)
            record = read_result.single()
            if record:
                print(f"Successfully read node: {record['id']} ('{record['name']}')")
            else:
                print("Failed to read back the created node!")
                sys.exit(1)
                
        # 7. Finally delete the test node
        print("Cleaning up (DELETING) the test node...")
        with driver.session() as session:
            delete_query = """
            MATCH (s:Skill {id: $id})
            DETACH DELETE s
            """
            delete_result = session.run(delete_query, id=test_node_id)
            summary = delete_result.consume()
            print(f"Deleted test node. Nodes deleted: {summary.counters.nodes_deleted}")
            
    except Exception as e:
        print(f"An error occurred during verification: {e}")
        sys.exit(1)
    finally:
        # 8. Close the driver
        if driver:
            print("Closing driver...")
            driver.close()
            print("Driver closed.")
            
    print("\nMilestone 1 check passed successfully!")

if __name__ == "__main__":
    main()
