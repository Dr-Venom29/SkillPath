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
        
    schema_path = os.path.join(os.path.dirname(__file__), "..", "cypher", "schema.cypher")
    if not os.path.exists(schema_path):
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)
        
    with open(schema_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Split queries by semicolon and strip comments/empty statements
    queries = []
    for statement in content.split(";"):
        cleaned_statement_lines = []
        for line in statement.split("\n"):
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                cleaned_statement_lines.append(line)
        cleaned_statement = "\n".join(cleaned_statement_lines).strip()
        if cleaned_statement:
            queries.append(cleaned_statement)
            
    print(f"Loaded {len(queries)} schema queries from {schema_path}")
    
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            for query in queries:
                print(f"\nExecuting query:\n{query}")
                try:
                    session.run(query)
                    print("Execution successful.")
                except Exception as e:
                    err_msg = str(e).lower()
                    if "alreadyexists" in err_msg or "already exists" in err_msg or "equivalentschemaruleviolation" in err_msg:
                        print("Constraint or index already exists. Skipping.")
                    else:
                        print(f"Error executing schema query: {e}")
                        # Check if legacy syntax is needed
                        if "require" in query.lower() and "for" in query.lower():
                            print("Attempting fallback legacy constraint syntax...")
                            # Attempt parsing to generate legacy constraint syntax:
                            # CREATE CONSTRAINT ON (s:Skill) ASSERT s.id IS UNIQUE
                            # Let's map query templates
                            legacy_query = None
                            if "Skill" in query:
                                legacy_query = "CREATE CONSTRAINT ON (s:Skill) ASSERT s.id IS UNIQUE"
                            elif "Role" in query:
                                legacy_query = "CREATE CONSTRAINT ON (r:Role) ASSERT r.id IS UNIQUE"
                            elif "Course" in query:
                                legacy_query = "CREATE CONSTRAINT ON (c:Course) ASSERT c.id IS UNIQUE"
                            elif "Project" in query:
                                legacy_query = "CREATE CONSTRAINT ON (p:Project) ASSERT p.id IS UNIQUE"
                            
                            if legacy_query:
                                try:
                                    print(f"Executing fallback query:\n{legacy_query}")
                                    session.run(legacy_query)
                                    print("Fallback execution successful.")
                                    continue
                                except Exception as fallback_err:
                                    print(f"Fallback query also failed: {fallback_err}")
                        raise e
    except Exception as e:
        print(f"\nSchema setup failed: {e}")
        sys.exit(1)
    finally:
        if driver:
            driver.close()
            
    print("\nSchema setup completed successfully!")

if __name__ == "__main__":
    main()
