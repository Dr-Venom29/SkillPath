import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

def print_section(title):
    print("=" * 60)
    print(f" {title}")
    print("=" * 60)

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
            # Step 8.1 — Verify node counts
            print_section("Step 8.1 — Node Counts")
            q81 = """
            MATCH (n)
            RETURN labels(n) AS labels, count(n) AS count
            ORDER BY labels
            """
            res81 = session.run(q81)
            print(f"{'Node Labels':<25} | {'Count':<10}")
            print("-" * 40)
            for record in res81:
                labels_str = ", ".join(record['labels']) if record['labels'] else "Unlabelled (None)"
                print(f"{labels_str:<25} | {record['count']:<10}")
                
            # Step 8.2 — Verify relationship counts
            print_section("Step 8.2 — Relationship Counts")
            q82 = """
            MATCH ()-[r]->()
            RETURN type(r) AS relationship, count(r) AS count
            ORDER BY relationship
            """
            res82 = session.run(q82)
            print(f"{'Relationship Type':<25} | {'Count':<10}")
            print("-" * 40)
            for record in res82:
                print(f"{record['relationship']:<25} | {record['count']:<10}")
                
            # Step 8.3 — Verify relationships connect the correct node types
            print_section("Step 8.3 — Relationship Schema Validation")
            q83 = """
            MATCH (a)-[r]->(b)
            RETURN
                labels(a) AS from_type,
                type(r) AS relationship,
                labels(b) AS to_type,
                count(*) AS count
            ORDER BY relationship, from_type, to_type
            """
            res83 = session.run(q83)
            print(f"{'From Label':<12} -> {'Relationship':<18} -> {'To Label':<12} | {'Count':<10}")
            print("-" * 65)
            for record in res83:
                from_str = ", ".join(record['from_type'])
                to_str = ", ".join(record['to_type'])
                print(f"{from_str:<12} -> {record['relationship']:<18} -> {to_str:<12} | {record['count']:<10}")
                
            # Step 8.4 — Verify non-random edges (Sample check)
            print_section("Step 8.4 — Sample Semantic Edges (Limit 20)")
            q84 = """
            MATCH (a)-[r]->(b)
            RETURN
                a.name AS from,
                type(r) AS relationship,
                b.name AS to
            ORDER BY relationship, from, to
            LIMIT 20
            """
            res84 = session.run(q84)
            print(f"{'From Entity':<30} | {'Relationship':<16} | {'To Entity':<30}")
            print("-" * 80)
            for record in res84:
                print(f"{record['from']:<30} | {record['relationship']:<16} | {record['to']:<30}")
                
            # Step 8.5 — Verify real multi-hop prerequisite chain
            print_section("Step 8.5 — Multi-Hop Prerequisite Chains (Sample Paths)")
            q85 = """
            MATCH path = (s:Skill)-[:PREREQUISITE_OF*2..5]->(p:Skill)
            RETURN [n in nodes(path) | n.name] AS skill_chain
            LIMIT 10
            """
            res85 = session.run(q85)
            for idx, record in enumerate(res85, 1):
                chain = record['skill_chain']
                print(f"Path {idx}: " + " -> ".join(chain))
                
            # Step 8.6 — Measure graph depth
            print_section("Step 8.6 — Prerequisite Path Depth Distribution")
            q86 = """
            MATCH path = (s:Skill)-[:PREREQUISITE_OF*1..5]->(p:Skill)
            RETURN
                length(path) AS depth,
                count(*) AS paths
            ORDER BY depth
            """
            res86 = session.run(q86)
            print(f"{'Prerequisite Depth':<20} | {'Number of Traversal Paths':<25}")
            print("-" * 50)
            for record in res86:
                print(f"{record['depth']:<20} | {record['paths']:<25}")
                
    except Exception as e:
        print(f"\nVerification failed: {e}")
        sys.exit(1)
    finally:
        if driver:
            driver.close()
            
    print("\nGraph verification completed successfully!")

if __name__ == "__main__":
    main()
