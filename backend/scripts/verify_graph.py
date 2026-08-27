import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

def print_section(title):
    print("=" * 65)
    print(f" {title}")
    print("=" * 65)

def main():
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
        
    driver = None
    errors = []

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
                
            # Step 8.3 — Strict Schema Validation Rules
            print_section("Step 8.3 — Strict Relationship Schema Rules")
            EXPECTED_SCHEMAS = {
                "PREREQUISITE_OF": ("Skill", "Skill"),
                "REQUIRES": ("Role", "Skill"),
                "TEACHES": ("Course", "Skill"),
                "BUILDS": ("Project", "Skill"),
                "RELATED_TO": ("Skill", "Skill"),
            }
            q83 = """
            MATCH (a)-[r]->(b)
            RETURN
                labels(a)[0] AS from_type,
                type(r) AS relationship,
                labels(b)[0] AS to_type,
                count(*) AS count
            ORDER BY relationship, from_type, to_type
            """
            res83 = session.run(q83)
            print(f"{'From Label':<12} -> {'Relationship':<18} -> {'To Label':<12} | {'Status':<10} | {'Count':<8}")
            print("-" * 70)
            for record in res83:
                rel = record['relationship']
                f_type = record['from_type']
                t_type = record['to_type']
                expected = EXPECTED_SCHEMAS.get(rel)
                
                if expected and (f_type, t_type) == expected:
                    status = "VALID [OK]"
                else:
                    status = "INVALID [FAIL]"
                    errors.append(f"Invalid edge schema: {f_type} -[{rel}]-> {t_type} (expected {expected})")
                    
                print(f"{f_type:<12} -> {rel:<18} -> {t_type:<12} | {status:<10} | {record['count']:<8}")

            # Step 8.4 — Cycle Detection in PREREQUISITE_OF
            print_section("Step 8.4 — Cycle Detection (PREREQUISITE_OF)")
            q_cycle = """
            MATCH path = (s:Skill)-[:PREREQUISITE_OF*1..10]->(s:Skill)
            RETURN [n in nodes(path) | n.id] AS cycle_ids, [n in nodes(path) | n.name] AS cycle_names
            LIMIT 10
            """
            cycles = list(session.run(q_cycle))
            if cycles:
                print(" [FAIL] PREREQUISITE_OF cycles detected!")
                for c in cycles:
                    chain = " -> ".join(c['cycle_names'])
                    print(f"   Cycle: {chain}")
                    errors.append(f"Prerequisite cycle detected: {chain}")
            else:
                print(" [PASS] 0 cycles detected in PREREQUISITE_OF relationships.")

            # Step 8.5 — Self-Referencing Check
            print_section("Step 8.5 — Self-Referencing Prerequisites Check")
            q_self = """
            MATCH (s:Skill)-[:PREREQUISITE_OF]->(s:Skill)
            RETURN s.id AS id, s.name AS name
            """
            self_loops = list(session.run(q_self))
            if self_loops:
                print(" [FAIL] Self-referencing prerequisites detected!")
                for s in self_loops:
                    print(f"   Self loop: {s['name']} ({s['id']})")
                    errors.append(f"Self-referencing prerequisite: {s['name']}")
            else:
                print(" [PASS] 0 self-referencing prerequisites found.")

            # Step 8.6 — Orphan Detection
            print_section("Step 8.6 — Orphan Node Detection")
            orphan_queries = {
                "Orphan Skills (no relations)": "MATCH (s:Skill) WHERE NOT (s)-[]-() RETURN s.name AS name, s.id AS id",
                "Orphan Roles (no REQUIRES)": "MATCH (r:Role) WHERE NOT (r)-[:REQUIRES]->() RETURN r.name AS name, r.id AS id",
                "Orphan Courses (no TEACHES)": "MATCH (c:Course) WHERE NOT (c)-[:TEACHES]->() RETURN c.name AS name, c.id AS id",
                "Orphan Projects (no BUILDS)": "MATCH (p:Project) WHERE NOT (p)-[:BUILDS]->() RETURN p.name AS name, p.id AS id",
            }
            for title, query in orphan_queries.items():
                orphans = list(session.run(query))
                if orphans:
                    print(f" [WARN] {title}: {len(orphans)} found")
                    for o in orphans:
                        print(f"    - {o['name']} ({o['id']})")
                else:
                    print(f" [PASS] {title}: 0 found")

            # Step 8.7 — Duplicate Relationship Check
            print_section("Step 8.7 — Duplicate Relationship Check")
            q_dup = """
            MATCH (a)-[r]->(b)
            WITH a, type(r) AS rel, b, count(*) AS cnt
            WHERE cnt > 1
            RETURN labels(a)[0] AS from_type, a.id AS from_id, rel, labels(b)[0] AS to_type, b.id AS to_id, cnt
            """
            duplicates = list(session.run(q_dup))
            if duplicates:
                print(" [FAIL] Duplicate relationships detected!")
                for d in duplicates:
                    print(f"   Duplicate: {d['from_id']} -[{d['rel']}]-> {d['to_id']} (Count: {d['cnt']})")
                    errors.append(f"Duplicate edge: {d['from_id']} -[{d['rel']}]-> {d['to_id']}")
            else:
                print(" [PASS] 0 duplicate relationship edges found.")

            # Step 8.8 — Path Depth Distribution
            print_section("Step 8.8 — Prerequisite Path Depth Distribution")
            q88 = """
            MATCH path = (s:Skill)-[:PREREQUISITE_OF*1..5]->(p:Skill)
            RETURN
                length(path) AS depth,
                count(*) AS paths
            ORDER BY depth
            """
            res88 = session.run(q88)
            print(f"{'Prerequisite Depth':<20} | {'Number of Traversal Paths':<25}")
            print("-" * 50)
            for record in res88:
                print(f"{record['depth']:<20} | {record['paths']:<25}")

            # Step 8.9 — Role Required Skill Reachability & Coherence Check
            print_section("Step 8.9 — Role Required Skill Reachability & Coherence")
            q89 = """
            MATCH (r:Role)-[:REQUIRES]->(req:Skill)
            OPTIONAL MATCH path = (root:Skill)-[:PREREQUISITE_OF*0..5]->(req)
            WHERE NOT ()-[:PREREQUISITE_OF]->(root)
            RETURN
                r.id AS role_id,
                r.name AS role_name,
                req.name AS skill_name,
                collect(DISTINCT root.name) AS root_prereqs
            ORDER BY r.name, req.name
            """
            res89 = list(session.run(q89))
            incoherent = []
            for record in res89:
                roots = record['root_prereqs']
                if not roots:
                    incoherent.append(f"{record['role_name']} -> {record['skill_name']} (Disconnected prerequisite graph)")
            
            if incoherent:
                print(" [FAIL] Incoherent role prerequisites detected!")
                for inc in incoherent:
                    print(f"   Incoherent: {inc}")
                    errors.append(inc)
            else:
                print(f" [PASS] All {len(res89)} required role skills have coherent, reachable prerequisite chains!")
                
    except Exception as e:
        print(f"\nVerification failed: {e}")
        sys.exit(1)
    finally:
        if driver:
            driver.close()

    print("\n" + "=" * 65)
    if errors:
        print(f"GRAPH VALIDATION FAILED: {len(errors)} error(s) found!")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("GRAPH VALIDATION PASSED COMPLETELY (0 errors found)!")
        print("=" * 65)

if __name__ == "__main__":
    main()
