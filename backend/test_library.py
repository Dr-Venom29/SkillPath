import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

def run_query_file(session, file_path, params):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    statements = []
    # Split by semicolon for files with multiple statements
    for stmt in content.split(";"):
        cleaned = []
        for line in stmt.split("\n"):
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                cleaned.append(line)
        cleaned_stmt = "\n".join(cleaned).strip()
        if cleaned_stmt:
            statements.append(cleaned_stmt)
            
    print(f"\n============================================================")
    print(f" Executing: {os.path.basename(file_path)}")
    print(f"============================================================")
    for idx, stmt in enumerate(statements, 1):
        print(f"\n[Query Statement {idx}]")
        print(f"Params: {params}")
        res = session.run(stmt, parameters=params)
        records = list(res)
        print(f"Returned {len(records)} records:")
        for r in records[:3]:
            # Pretty print dict keys and sample values
            print("  - ", {k: (str(v)[:70] + "..." if len(str(v)) > 70 else v) for k, v in dict(r).items()})
        if len(records) > 3:
            print("    ...")

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
        
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            # 1. Test search_skills.cypher
            run_query_file(session, "cypher/search_skills.cypher", {"query": "python", "limit": 2})
            
            # 2. Test skill_details.cypher
            run_query_file(session, "cypher/skill_details.cypher", {"skill_id": "rest-apis"})
            
            # 3. Test prerequisites.cypher
            run_query_file(session, "cypher/prerequisites.cypher", {"skill_id": "rest-apis"})
            
            # 4. Test role_requirements.cypher
            run_query_file(session, "cypher/role_requirements.cypher", {"role_id": "backend-developer"})
            
            # 5. Test related_skills.cypher
            run_query_file(session, "cypher/related_skills.cypher", {"skill_id": "rest-apis"})
            
            # 6. Test learning_path.cypher
            run_query_file(session, "cypher/learning_path.cypher", {"from_id": "prog-fundamentals", "to_id": "next-js"})
            
    except Exception as e:
        print(f"\nVerification failed: {e}")
        sys.exit(1)
    finally:
        if driver:
            driver.close()
            
    print("\nAll Cypher library query files tested successfully!")

if __name__ == "__main__":
    main()
