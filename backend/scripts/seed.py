import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Define the complete controlled dataset
SKILLS = [
    {"id": "prog-fundamentals", "name": "Programming Fundamentals", "description": "Basic concepts of programming including variables, loops, conditions, and basic logic.", "level": "Beginner"},
    {"id": "python", "name": "Python", "description": "General-purpose high-level programming language known for readability and clean syntax.", "level": "Beginner"},
    {"id": "javascript", "name": "JavaScript", "description": "Dynamic scripting language for web pages, enabling client-side interactivity.", "level": "Beginner"},
    {"id": "typescript", "name": "TypeScript", "description": "Typed superset of JavaScript that compiles to plain JavaScript for larger-scale applications.", "level": "Intermediate"},
    {"id": "html", "name": "HTML", "description": "HyperText Markup Language, the standard document format for web browsers.", "level": "Beginner"},
    {"id": "css", "name": "CSS", "description": "Cascading Style Sheets, used for describing the presentation of web pages.", "level": "Beginner"},
    {"id": "dom-manipulation", "name": "DOM Manipulation", "description": "Interacting with the browser Document Object Model dynamically via script.", "level": "Beginner"},
    {"id": "react", "name": "React", "description": "A popular front-end JavaScript library for building component-based user interfaces.", "level": "Intermediate"},
    {"id": "state-management", "name": "State Management", "description": "Managing data state across complex component trees (Redux, Zustand, Context API).", "level": "Intermediate"},
    {"id": "tailwind-css", "name": "Tailwind CSS", "description": "Utility-first CSS framework for rapid and highly customizable UI design.", "level": "Beginner"},
    {"id": "git", "name": "Git", "description": "Distributed version control system for tracking changes in source code.", "level": "Beginner"},
    {"id": "linux-cli", "name": "Linux Command Line", "description": "Operating system shell interface for file manipulation and process execution.", "level": "Beginner"},
    {"id": "networking-basics", "name": "Networking Basics", "description": "Foundational concepts of networks, connections, routing, and communication protocols.", "level": "Beginner"},
    {"id": "tcp-ip", "name": "TCP/IP", "description": "Transmission Control Protocol/Internet Protocol, basic communication protocol stack.", "level": "Beginner"},
    {"id": "http-https", "name": "HTTP/HTTPS", "description": "Web transfer protocols enabling data transfer and secure end-to-end connections.", "level": "Beginner"},
    {"id": "dns", "name": "DNS", "description": "Domain Name System, translating human-readable hostnames to IP addresses.", "level": "Beginner"},
    {"id": "json", "name": "JSON", "description": "JavaScript Object Notation, standard lightweight data interchange format.", "level": "Beginner"},
    {"id": "rest-apis", "name": "REST APIs", "description": "Representational State Transfer APIs, standard architectural style for web services.", "level": "Intermediate"},
    {"id": "graphql", "name": "GraphQL", "description": "Query language for APIs and runtime for executing queries with existing data.", "level": "Intermediate"},
    {"id": "authentication", "name": "Authentication", "description": "Proving identity via tokens, passwords, OAuth, session management, or cookies.", "level": "Intermediate"},
    {"id": "sql", "name": "SQL", "description": "Structured Query Language for querying and managing relational databases.", "level": "Beginner"},
    {"id": "databases-relational", "name": "Relational Databases", "description": "Tabular database engines ensuring ACID guarantees (PostgreSQL, MySQL).", "level": "Intermediate"},
    {"id": "databases-nosql", "name": "NoSQL Databases", "description": "Non-tabular database engines (Document, Key-Value, Columnar) like MongoDB.", "level": "Intermediate"},
    {"id": "databases-graph", "name": "Graph Databases", "description": "Highly-connected database engines optimized for network relations (Neo4j).", "level": "Advanced"},
    {"id": "data-structures", "name": "Data Structures", "description": "Organizing and storing data in computer memory (Arrays, Lists, Trees, Graphs).", "level": "Intermediate"},
    {"id": "algorithms", "name": "Algorithms", "description": "Step-by-step logic procedures for sorting, searching, and optimization tasks.", "level": "Intermediate"},
    {"id": "testing-unit", "name": "Unit Testing", "description": "Testing small, isolated parts of software (functions, methods) for correctness.", "level": "Intermediate"},
    {"id": "testing-integration", "name": "Integration Testing", "description": "Testing groups of software modules together to verify collaborative behavior.", "level": "Intermediate"},
    {"id": "docker", "name": "Docker", "description": "Standard containerization platform for packaging applications and dependencies.", "level": "Intermediate"},
    {"id": "ci-cd", "name": "CI/CD", "description": "Continuous Integration & Deployment pipelines for automated software release.", "level": "Intermediate"},
    {"id": "cloud-basics", "name": "Cloud Basics", "description": "Fundamental cloud architecture and services (EC2, S3, IAM, Serverless).", "level": "Intermediate"},
    {"id": "kubernetes", "name": "Kubernetes", "description": "Container orchestration engine for automated scaling, updates, and load balancing.", "level": "Advanced"},
    {"id": "monitoring-logging", "name": "Monitoring & Logging", "description": "Tracking software health metrics and debug logs (Prometheus, Grafana, ELK).", "level": "Intermediate"},
    {"id": "web-security", "name": "Web Security", "description": "Vulnerability protection covering CORS, CSRF, XSS, and security headers.", "level": "Intermediate"},
    {"id": "ssl-tls", "name": "SSL/TLS", "description": "Secure transport layer encryption protecting data transit.", "level": "Intermediate"},
    {"id": "python-ds", "name": "Python for Data Science", "description": "Using Python's scientific libraries for descriptive and predictive data research.", "level": "Intermediate"},
    {"id": "pandas-numpy", "name": "Pandas & NumPy", "description": "Libraries for structured data analysis, manipulation, and array computation.", "level": "Intermediate"},
    {"id": "data-visualization", "name": "Data Visualization", "description": "Representing dataset trends visually (Matplotlib, Seaborn, D3.js).", "level": "Intermediate"},
    {"id": "machine-learning", "name": "Machine Learning Basics", "description": "Standard algorithms for classification, regression, and clustering.", "level": "Advanced"},
    {"id": "message-queues", "name": "Message Queues", "description": "Asynchronous task workers and brokers (RabbitMQ, Kafka, Redis PubSub).", "level": "Advanced"},
    {"id": "node-js", "name": "Node.js", "description": "V8-powered asynchronous JavaScript runtime for server-side execution.", "level": "Intermediate"},
    {"id": "web-sockets", "name": "WebSockets", "description": "Full-duplex persistent communication channel over a single TCP connection.", "level": "Intermediate"},
    {"id": "nginx", "name": "Nginx", "description": "High-performance reverse proxy server, load balancer, and HTTP cache.", "level": "Intermediate"},
    {"id": "bash-scripting", "name": "Bash Scripting", "description": "Shell scripting languages for OS-level task automation.", "level": "Intermediate"},
    {"id": "api-design", "name": "API Design", "description": "Synthesizing clean, standardized backend endpoints (routes, requests, responses).", "level": "Intermediate"},
    {"id": "microservices", "name": "Microservices", "description": "Decomposing applications into independent, networked functional modules.", "level": "Advanced"},
    {"id": "system-design", "name": "System Design", "description": "Planning scale architectures, load balancing, caching, and data partitions.", "level": "Advanced"},
    {"id": "redis-caching", "name": "Redis & Caching", "description": "In-memory database structure store used for caching and session stores.", "level": "Intermediate"},
    {"id": "orm-concepts", "name": "ORM Concepts", "description": "Object-Relational Mapping (Prisma, SQLAlchemy) translating code queries to SQL.", "level": "Intermediate"},
    {"id": "cybersecurity-basics", "name": "Cybersecurity Basics", "description": "Foundational threat modeling, vulnerability detection, and secure practice.", "level": "Beginner"},
    {"id": "cryptography", "name": "Cryptography", "description": "Encryption, decryption, hashing algorithms, and public-key infrastructure.", "level": "Advanced"},
    {"id": "data-warehousing", "name": "Data Warehousing", "description": "Consolidating transactional datasets for analytical intelligence.", "level": "Advanced"},
    {"id": "etl-pipelines", "name": "ETL Pipelines", "description": "Extract, Transform, Load script workflows for backend data engineering.", "level": "Intermediate"},
    {"id": "apache-spark", "name": "Apache Spark", "description": "Unified analytical engine for large-scale distributed data processing.", "level": "Advanced"},
    {"id": "clean-code", "name": "Clean Code Practices", "description": "Writing readable, maintainable, modular, and well-tested code code bases.", "level": "Intermediate"},
    {"id": "agile-scrum", "name": "Agile & Scrum", "description": "Modern software team project planning methodology and sprint processes.", "level": "Beginner"},
    {"id": "responsive-design", "name": "Responsive Design", "description": "CSS styling techniques for rendering across varied device viewports.", "level": "Beginner"},
    {"id": "css-animations", "name": "CSS Animations", "description": "Transitions, keyframes, and animations defining rich visual motion.", "level": "Intermediate"},
    {"id": "next-js", "name": "Next.js", "description": "React meta-framework enabling server-side rendering, routing, and optimization.", "level": "Advanced"},
    {"id": "graphql-schemas", "name": "GraphQL Schemas", "description": "Defining query fields, mutation routes, and strict type schemas for APIs.", "level": "Intermediate"}
]

ROLES = [
    {"id": "frontend-developer", "name": "Frontend Developer", "description": "Builds responsive, high-performance web user interfaces using modern front-end frameworks."},
    {"id": "backend-developer", "name": "Backend Developer", "description": "Builds and secures scalable backend server APIs, databases, and microservices."},
    {"id": "fullstack-developer", "name": "Fullstack Developer", "description": "Possesses competency across the complete web stack, spanning database, server logic, and client UI."},
    {"id": "devops-engineer", "name": "DevOps Engineer", "description": "Automates development deployments, CI/CD pipelines, container orchestration, and server monitoring."},
    {"id": "data-engineer", "name": "Data Engineer", "description": "Processes and pipelines large datasets, engineering database engines, ETL networks, and analytical stores."},
    {"id": "security-engineer", "name": "Security Engineer", "description": "Protects systems and networks from threats, configuring cryptography, firewalls, and security policies."},
    {"id": "qa-engineer", "name": "QA Engineer", "description": "Assures software releases through automated unit, integration, end-to-end, and manual tests."}
]

COURSES = [
    {"id": "intro-programming", "name": "Introduction to Programming", "description": "Foundational programming logic covering basic syntax, variables, loop structures, and conditionals."},
    {"id": "git-github", "name": "Git & GitHub Version Control", "description": "Master version tracking, pull requests, merges, conflict resolution, and branching."},
    {"id": "html-css-basics", "name": "HTML & CSS for Beginners", "description": "Learn layout engines, selectors, responsive structure, and web style practices."},
    {"id": "js-deep-dive", "name": "JavaScript Deep Dive", "description": "Core asynchronous patterns, callbacks, promises, closures, dynamic execution, and browser API."},
    {"id": "modern-react", "name": "Modern React & State Management", "description": "JSX syntax, components, rendering lifecycles, hooks, and dynamic data state providers."},
    {"id": "python-backend", "name": "Python Backend Development with FastAPI", "description": "API services, routing, validation, Pydantic, parameters, and unit testing integration."},
    {"id": "sql-databases", "name": "SQL & Relational Databases", "description": "Query construction, table normalization, primary/foreign keys, joins, indexes, and ACID rules."},
    {"id": "docker-containers", "name": "Docker & Containerization", "description": "Create images, write Dockerfiles, configure volumes, networks, and compose multi-container systems."},
    {"id": "web-networking", "name": "Web Networking Fundamentals", "description": "Understand HTTP protocols, DNS servers, TCP/IP handshakes, network routing, and IP addressing."},
    {"id": "web-security-guide", "name": "Practical Web Security", "description": "Vulnerability analysis, security headers, token auth, JWT, cookies, and CORS configuration."},
    {"id": "ds-algo-python", "name": "Data Structures & Algorithms in Python", "description": "Implement binary trees, graphs, sorting lists, hash tables, big-O analysis, and algorithms."},
    {"id": "devops-bootcamp", "name": "DevOps Bootcamp", "description": "Automated pipelines, Kubernetes configurations, cloud compute setup, and log dashboards."},
    {"id": "data-science-intro", "name": "Introduction to Data Science", "description": "Analyze mathematical distributions, manipulate matrices, clean datasets, and draw insights."},
    {"id": "node-express", "name": "Node.js & Express API Development", "description": "Write server endpoints, construct middle-wares, handle exceptions, and route JSON operations."},
    {"id": "typescript-react", "name": "TypeScript with React", "description": "Type components, map interfaces, static typing state, and configure compilation options."}
]

PROJECTS = [
    {"id": "portfolio-website", "name": "Personal Portfolio Website", "description": "Static HTML/CSS responsive portfolio landing page showcasing work projects."},
    {"id": "task-manager-react", "name": "React Task Manager", "description": "Build interactive tasks boards, configuring complex local state and component styling."},
    {"id": "weather-dashboard-js", "name": "JavaScript Weather Dashboard", "description": "Dynamic browser application querying external weather services using fetch APIs."},
    {"id": "blog-api-fastapi", "name": "FastAPI Blog API", "description": "Backend database service providing full REST query routes for article entities."},
    {"id": "e-commerce-backend", "name": "E-commerce Backend Service", "description": "Scale relational database engine, handle authentication profiles, and query transactions."},
    {"id": "containerized-app", "name": "Dockerized Multi-Container Application", "description": "Bundle web app servers and SQL databases inside compose networks."},
    {"id": "ci-cd-pipeline-deploy", "name": "Automated CI/CD Pipeline", "description": "Create Git actions scripts mapping deployment pipelines to cloud environments."},
    {"id": "network-packet-sniffer", "name": "Python Packet Sniffer", "description": "Build a raw socket parser analyzing TCP header values in real-time."},
    {"id": "data-analysis-report", "name": "Sales Data Analysis Report", "description": "Write Jupyter scripts aggregating multi-year customer data outputs."},
    {"id": "chat-app-websockets", "name": "Real-Time Chat Application", "description": "Build full WebSocket pipelines pushing instant messages to connected users."}
]

# Define relationship matrices
PREREQUISITES = [
    ("prog-fundamentals", "python"), ("prog-fundamentals", "javascript"),
    ("javascript", "dom-manipulation"), ("dom-manipulation", "react"), ("react", "next-js"),
    ("javascript", "typescript"), ("typescript", "next-js"), ("react", "state-management"),
    ("html", "dom-manipulation"), ("css", "responsive-design"), ("responsive-design", "tailwind-css"),
    ("css", "css-animations"), ("networking-basics", "tcp-ip"), ("tcp-ip", "http-https"),
    ("http-https", "dns"), ("http-https", "rest-apis"), ("json", "rest-apis"),
    ("rest-apis", "authentication"), ("rest-apis", "graphql"), ("graphql", "graphql-schemas"),
    ("sql", "databases-relational"), ("databases-relational", "orm-concepts"),
    ("databases-relational", "redis-caching"), ("databases-nosql", "redis-caching"),
    ("databases-relational", "databases-graph"), ("data-structures", "algorithms"),
    ("prog-fundamentals", "data-structures"), ("linux-cli", "bash-scripting"),
    ("git", "ci-cd"), ("docker", "kubernetes"), ("docker", "ci-cd"),
    ("cloud-basics", "kubernetes"), ("ci-cd", "monitoring-logging"), ("http-https", "web-security"),
    ("web-security", "ssl-tls"), ("web-security", "authentication"), ("cybersecurity-basics", "cryptography"),
    ("python", "python-ds"), ("python-ds", "pandas-numpy"), ("pandas-numpy", "data-visualization"),
    ("pandas-numpy", "machine-learning"), ("databases-relational", "data-warehousing"),
    ("data-warehousing", "etl-pipelines"), ("etl-pipelines", "apache-spark"),
    ("rest-apis", "api-design"), ("api-design", "microservices"), ("microservices", "system-design"),
    ("testing-unit", "testing-integration"), ("clean-code", "system-design"), ("nginx", "microservices")
]

REQUIRES = [
    ("frontend-developer", "html"), ("frontend-developer", "css"), ("frontend-developer", "javascript"),
    ("frontend-developer", "react"), ("frontend-developer", "git"), ("frontend-developer", "tailwind-css"),
    ("frontend-developer", "typescript"),
    ("backend-developer", "python"), ("backend-developer", "node-js"), ("backend-developer", "sql"),
    ("backend-developer", "databases-relational"), ("backend-developer", "rest-apis"),
    ("backend-developer", "git"), ("backend-developer", "testing-unit"), ("backend-developer", "docker"),
    ("fullstack-developer", "html"), ("fullstack-developer", "javascript"), ("fullstack-developer", "react"),
    ("fullstack-developer", "node-js"), ("fullstack-developer", "databases-relational"),
    ("fullstack-developer", "rest-apis"), ("fullstack-developer", "git"),
    ("devops-engineer", "linux-cli"), ("devops-engineer", "bash-scripting"), ("devops-engineer", "git"),
    ("devops-engineer", "docker"), ("devops-engineer", "ci-cd"), ("devops-engineer", "kubernetes"),
    ("devops-engineer", "cloud-basics"),
    ("data-engineer", "python"), ("data-engineer", "sql"), ("data-engineer", "databases-relational"),
    ("data-engineer", "pandas-numpy"), ("data-engineer", "etl-pipelines"), ("data-engineer", "apache-spark"),
    ("security-engineer", "networking-basics"), ("security-engineer", "tcp-ip"), ("security-engineer", "web-security"),
    ("security-engineer", "ssl-tls"), ("security-engineer", "cybersecurity-basics"), ("security-engineer", "cryptography"),
    ("qa-engineer", "prog-fundamentals"), ("qa-engineer", "python"), ("qa-engineer", "testing-unit"),
    ("qa-engineer", "testing-integration"), ("qa-engineer", "git")
]

TEACHES = [
    ("intro-programming", "prog-fundamentals"), ("intro-programming", "python"),
    ("git-github", "git"), ("html-css-basics", "html"), ("html-css-basics", "css"),
    ("js-deep-dive", "javascript"), ("js-deep-dive", "dom-manipulation"),
    ("modern-react", "react"), ("modern-react", "state-management"),
    ("python-backend", "python"), ("python-backend", "rest-apis"), ("python-backend", "testing-unit"),
    ("sql-databases", "sql"), ("sql-databases", "databases-relational"),
    ("docker-containers", "docker"), ("web-networking", "networking-basics"),
    ("web-networking", "tcp-ip"), ("web-networking", "http-https"),
    ("web-security-guide", "web-security"), ("web-security-guide", "authentication"),
    ("ds-algo-python", "data-structures"), ("ds-algo-python", "algorithms"),
    ("devops-bootcamp", "ci-cd"), ("devops-bootcamp", "kubernetes"), ("devops-bootcamp", "cloud-basics"),
    ("data-science-intro", "python-ds"), ("data-science-intro", "pandas-numpy"),
    ("node-express", "node-js"), ("node-express", "rest-apis"),
    ("typescript-react", "typescript"), ("typescript-react", "react")
]

BUILDS = [
    ("portfolio-website", "html"), ("portfolio-website", "css"), ("portfolio-website", "responsive-design"),
    ("task-manager-react", "react"), ("task-manager-react", "state-management"),
    ("weather-dashboard-js", "javascript"), ("weather-dashboard-js", "dom-manipulation"), ("weather-dashboard-js", "http-https"),
    ("blog-api-fastapi", "python"), ("blog-api-fastapi", "rest-apis"), ("blog-api-fastapi", "sql"),
    ("e-commerce-backend", "node-js"), ("e-commerce-backend", "databases-relational"), ("e-commerce-backend", "authentication"),
    ("containerized-app", "docker"), ("containerized-app", "databases-relational"),
    ("ci-cd-pipeline-deploy", "ci-cd"), ("ci-cd-pipeline-deploy", "cloud-basics"),
    ("network-packet-sniffer", "python"), ("network-packet-sniffer", "tcp-ip"),
    ("data-analysis-report", "pandas-numpy"), ("data-analysis-report", "data-visualization"),
    ("chat-app-websockets", "node-js"), ("chat-app-websockets", "web-sockets"), ("chat-app-websockets", "web-security")
]

RELATED_TO = [
    ("rest-apis", "graphql"), ("databases-relational", "databases-nosql"),
    ("databases-relational", "databases-graph"), ("databases-nosql", "databases-graph"),
    ("react", "tailwind-css"), ("docker", "nginx"), ("authentication", "cryptography"),
    ("data-structures", "pandas-numpy"), ("agile-scrum", "clean-code"),
    ("css-animations", "responsive-design")
]

def main():
    # Load environment variables
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
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
        
        # 1. Create constraints/indexes
        print("\nCreating schema constraints and indexes...")
        with driver.session() as session:
            # We run these with safety check error logs caught
            constraints = [
                "CREATE CONSTRAINT skill_id_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE",
                "CREATE CONSTRAINT role_id_unique IF NOT EXISTS FOR (r:Role) REQUIRE r.id IS UNIQUE",
                "CREATE CONSTRAINT course_id_unique IF NOT EXISTS FOR (c:Course) REQUIRE c.id IS UNIQUE",
                "CREATE CONSTRAINT project_id_unique IF NOT EXISTS FOR (p:Project) REQUIRE p.id IS UNIQUE",
                "CREATE INDEX skill_name_idx IF NOT EXISTS FOR (s:Skill) ON (s.name)",
                "CREATE INDEX role_name_idx IF NOT EXISTS FOR (r:Role) ON (r.name)",
                "CREATE INDEX course_name_idx IF NOT EXISTS FOR (c:Course) ON (c.name)",
                "CREATE INDEX project_name_idx IF NOT EXISTS FOR (p:Project) ON (p.name)"
            ]
            for statement in constraints:
                try:
                    session.run(statement)
                except Exception as e:
                    print(f"Index/Constraint note: {e}")
                    
        # NOTE: No database wipe is performed in the production seed script to ensure safety.
        # The script only merges nodes and relationships, updating properties as needed.
        # If a full reset is required, use the separate reset_database.py utility.

        # 2. Create nodes using parameterized MERGE
        print("\nSeeding Nodes using parameterized MERGE queries...")
        with driver.session() as session:
            # Seed Skill nodes
            print(f" - Seeding {len(SKILLS)} Skills...")
            skill_query = """
            MERGE (s:Skill {id: $id})
            SET s.name = $name,
                s.description = $description,
                s.level = $level
            """
            for s in SKILLS:
                session.run(skill_query, **s)
                
            # Seed Role nodes
            print(f" - Seeding {len(ROLES)} Roles...")
            role_query = """
            MERGE (r:Role {id: $id})
            SET r.name = $name,
                r.description = $description
            """
            for r in ROLES:
                session.run(role_query, **r)
                
            # Seed Course nodes
            print(f" - Seeding {len(COURSES)} Courses...")
            course_query = """
            MERGE (c:Course {id: $id})
            SET c.name = $name,
                c.description = $description
            """
            for c in COURSES:
                session.run(course_query, **c)
                
            # Seed Project nodes
            print(f" - Seeding {len(PROJECTS)} Projects...")
            project_query = """
            MERGE (p:Project {id: $id})
            SET p.name = $name,
                p.description = $description
            """
            for p in PROJECTS:
                session.run(project_query, **p)

        # 3. Create relationships using parameterized MERGE
        print("\nSeeding Relationships using parameterized MERGE queries...")
        with driver.session() as session:
            # Seed PREREQUISITE_OF
            print(f" - Seeding {len(PREREQUISITES)} PREREQUISITE_OF relationships...")
            prereq_query = """
            MATCH (a:Skill {id: $from_id})
            MATCH (b:Skill {id: $to_id})
            MERGE (a)-[r:PREREQUISITE_OF]->(b)
            """
            for from_id, to_id in PREREQUISITES:
                session.run(prereq_query, from_id=from_id, to_id=to_id)
                
            # Seed REQUIRES
            print(f" - Seeding {len(REQUIRES)} REQUIRES relationships...")
            requires_query = """
            MATCH (a:Role {id: $from_id})
            MATCH (b:Skill {id: $to_id})
            MERGE (a)-[r:REQUIRES]->(b)
            """
            for from_id, to_id in REQUIRES:
                session.run(requires_query, from_id=from_id, to_id=to_id)
                
            # Seed TEACHES
            print(f" - Seeding {len(TEACHES)} TEACHES relationships...")
            teaches_query = """
            MATCH (a:Course {id: $from_id})
            MATCH (b:Skill {id: $to_id})
            MERGE (a)-[r:TEACHES]->(b)
            """
            for from_id, to_id in TEACHES:
                session.run(teaches_query, from_id=from_id, to_id=to_id)
                
            # Seed BUILDS
            print(f" - Seeding {len(BUILDS)} BUILDS relationships...")
            builds_query = """
            MATCH (a:Project {id: $from_id})
            MATCH (b:Skill {id: $to_id})
            MERGE (a)-[r:BUILDS]->(b)
            """
            for from_id, to_id in BUILDS:
                session.run(builds_query, from_id=from_id, to_id=to_id)
                
            # Seed RELATED_TO
            print(f" - Seeding {len(RELATED_TO)} RELATED_TO relationships...")
            related_query = """
            MATCH (a:Skill {id: $from_id})
            MATCH (b:Skill {id: $to_id})
            MERGE (a)-[r:RELATED_TO]->(b)
            """
            for from_id, to_id in RELATED_TO:
                session.run(related_query, from_id=from_id, to_id=to_id)

        # 4. Verify counts
        print("\nVerifying Node Counts...")
        with driver.session() as session:
            node_counts = session.run("""
                MATCH (n)
                RETURN labels(n)[0] AS label, count(n) AS count
                ORDER BY label
            """)
            for record in node_counts:
                print(f" - {record['label']}: {record['count']}")
                
            print("\nVerifying Relationship Counts...")
            rel_counts = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) AS rel_type, count(r) AS count
                ORDER BY rel_type
            """)
            for record in rel_counts:
                print(f" - {record['rel_type']}: {record['count']}")

    except Exception as e:
        print(f"\nSeeding script failed: {e}")
        sys.exit(1)
    finally:
        if driver:
            print("\nClosing connection...")
            driver.close()
            print("Connection closed.")
            
    print("\nDatabase seed completed successfully!")

if __name__ == "__main__":
    main()
