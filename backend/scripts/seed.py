import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Define the complete controlled dataset (~90 skills, 14 roles, 20 courses, 15 projects)
SKILLS = [
    # Core Programming
    {"id": "prog-fundamentals", "name": "Programming Fundamentals", "description": "Basic concepts of programming including variables, loops, conditions, and basic logic.", "level": "Beginner"},
    {"id": "python", "name": "Python", "description": "General-purpose high-level programming language known for readability and clean syntax.", "level": "Beginner"},
    {"id": "python-oop", "name": "Python OOP", "description": "Object-oriented programming in Python covering classes, inheritance, polymorphism, and magic methods.", "level": "Intermediate"},
    {"id": "javascript", "name": "JavaScript", "description": "Dynamic scripting language for web pages, enabling client-side interactivity.", "level": "Beginner"},
    {"id": "typescript", "name": "TypeScript", "description": "Typed superset of JavaScript that compiles to plain JavaScript for larger-scale applications.", "level": "Intermediate"},
    {"id": "data-structures", "name": "Data Structures", "description": "Organizing and storing data in computer memory (Arrays, Lists, Trees, Graphs).", "level": "Intermediate"},
    {"id": "algorithms", "name": "Algorithms", "description": "Step-by-step logic procedures for sorting, searching, and optimization tasks.", "level": "Intermediate"},
    {"id": "clean-code", "name": "Clean Code Practices", "description": "Writing readable, maintainable, modular, and well-tested code bases.", "level": "Intermediate"},
    {"id": "software-engineering", "name": "Software Engineering", "description": "Core principles of software development, architecture patterns, and design principles.", "level": "Intermediate"},

    # Frontend
    {"id": "html", "name": "HTML", "description": "HyperText Markup Language, the standard document format for web browsers.", "level": "Beginner"},
    {"id": "css", "name": "CSS", "description": "Cascading Style Sheets, used for describing the presentation of web pages.", "level": "Beginner"},
    {"id": "responsive-design", "name": "Responsive Design", "description": "CSS styling techniques for rendering across varied device viewports.", "level": "Beginner"},
    {"id": "css-animations", "name": "CSS Animations", "description": "Transitions, keyframes, and animations defining rich visual motion.", "level": "Intermediate"},
    {"id": "tailwind-css", "name": "Tailwind CSS", "description": "Utility-first CSS framework for rapid and highly customizable UI design.", "level": "Beginner"},
    {"id": "dom-manipulation", "name": "DOM Manipulation", "description": "Interacting with the browser Document Object Model dynamically via script.", "level": "Beginner"},
    {"id": "react", "name": "React", "description": "A popular front-end JavaScript library for building component-based user interfaces.", "level": "Intermediate"},
    {"id": "state-management", "name": "State Management", "description": "Managing data state across complex component trees (Redux, Zustand, Context API).", "level": "Intermediate"},
    {"id": "next-js", "name": "Next.js", "description": "React meta-framework enabling server-side rendering, routing, and optimization.", "level": "Advanced"},
    {"id": "frontend-architecture", "name": "Frontend Architecture", "description": "Designing scalable front-end systems, state flows, modular component design, and asset pipelines.", "level": "Advanced"},

    # Backend & Web APIs
    {"id": "networking-basics", "name": "Networking Basics", "description": "Foundational concepts of networks, connections, routing, and communication protocols.", "level": "Beginner"},
    {"id": "tcp-ip", "name": "TCP/IP", "description": "Transmission Control Protocol/Internet Protocol, basic communication protocol stack.", "level": "Beginner"},
    {"id": "http-https", "name": "HTTP/HTTPS", "description": "Web transfer protocols enabling data transfer and secure end-to-end connections.", "level": "Beginner"},
    {"id": "dns", "name": "DNS", "description": "Domain Name System, translating human-readable hostnames to IP addresses.", "level": "Beginner"},
    {"id": "json", "name": "JSON", "description": "JavaScript Object Notation, standard lightweight data interchange format.", "level": "Beginner"},
    {"id": "rest-apis", "name": "REST APIs", "description": "Representational State Transfer APIs, standard architectural style for web services.", "level": "Intermediate"},
    {"id": "api-design", "name": "API Design", "description": "Synthesizing clean, standardized backend endpoints (routes, requests, responses).", "level": "Intermediate"},
    {"id": "graphql", "name": "GraphQL", "description": "Query language for APIs and runtime for executing queries with existing data.", "level": "Intermediate"},
    {"id": "graphql-schemas", "name": "GraphQL Schemas", "description": "Defining query fields, mutation routes, and strict type schemas for APIs.", "level": "Intermediate"},
    {"id": "authentication", "name": "Authentication", "description": "Proving identity via tokens, passwords, OAuth, session management, or cookies.", "level": "Intermediate"},
    {"id": "authorization", "name": "Authorization", "description": "Controlling user permissions, Role-Based Access Control (RBAC), and API scopes.", "level": "Intermediate"},
    {"id": "node-js", "name": "Node.js", "description": "V8-powered asynchronous JavaScript runtime for server-side execution.", "level": "Intermediate"},
    {"id": "web-sockets", "name": "WebSockets", "description": "Full-duplex persistent communication channel over a single TCP connection.", "level": "Intermediate"},
    {"id": "message-queues", "name": "Message Queues", "description": "Asynchronous task workers and brokers (RabbitMQ, Kafka, Redis PubSub).", "level": "Advanced"},
    {"id": "backend-architecture", "name": "Backend Architecture", "description": "Architecting server infrastructure, request lifecycles, middleware chains, and fault tolerance.", "level": "Advanced"},
    {"id": "microservices", "name": "Microservices", "description": "Decomposing applications into independent, networked functional modules.", "level": "Advanced"},
    {"id": "system-design", "name": "System Design", "description": "Planning scale architectures, load balancing, caching, and data partitions.", "level": "Advanced"},

    # Databases
    {"id": "sql", "name": "SQL", "description": "Structured Query Language for querying and managing relational databases.", "level": "Beginner"},
    {"id": "databases-relational", "name": "Relational Databases", "description": "Tabular database engines ensuring ACID guarantees (PostgreSQL, MySQL).", "level": "Intermediate"},
    {"id": "database-design", "name": "Database Design", "description": "Schema normalization, indexing strategies, entity-relationship modeling, and query tuning.", "level": "Intermediate"},
    {"id": "orm-concepts", "name": "ORM Concepts", "description": "Object-Relational Mapping (Prisma, SQLAlchemy) translating code queries to SQL.", "level": "Intermediate"},
    {"id": "databases-nosql", "name": "NoSQL Databases", "description": "Non-tabular database engines (Document, Key-Value, Columnar) like MongoDB.", "level": "Intermediate"},
    {"id": "redis-caching", "name": "Redis & Caching", "description": "In-memory database structure store used for caching and session stores.", "level": "Intermediate"},
    {"id": "databases-graph", "name": "Graph Databases", "description": "Highly-connected database engines optimized for network relations (Neo4j).", "level": "Advanced"},

    # DevOps & Infrastructure
    {"id": "git", "name": "Git", "description": "Distributed version control system for tracking changes in source code.", "level": "Beginner"},
    {"id": "linux-cli", "name": "Linux Command Line", "description": "Operating system shell interface for file manipulation and process execution.", "level": "Beginner"},
    {"id": "bash-scripting", "name": "Bash Scripting", "description": "Shell scripting languages for OS-level task automation.", "level": "Intermediate"},
    {"id": "docker", "name": "Docker", "description": "Standard containerization platform for packaging applications and dependencies.", "level": "Intermediate"},
    {"id": "ci-cd", "name": "CI/CD", "description": "Continuous Integration & Deployment pipelines for automated software release.", "level": "Intermediate"},
    {"id": "kubernetes", "name": "Kubernetes", "description": "Container orchestration engine for automated scaling, updates, and load balancing.", "level": "Advanced"},
    {"id": "container-orchestration", "name": "Container Orchestration", "description": "Managing cluster deployments, service discovery, and rolling upgrades.", "level": "Advanced"},
    {"id": "cloud-basics", "name": "Cloud Basics", "description": "Fundamental cloud architecture and services (EC2, S3, IAM, Serverless).", "level": "Intermediate"},
    {"id": "infrastructure-as-code", "name": "Infrastructure as Code", "description": "Provisioning cloud resources using declarative scripts (Terraform, CloudFormation).", "level": "Advanced"},
    {"id": "cloud-deployment", "name": "Cloud Deployment", "description": "Deploying web services to AWS, GCP, or Azure with auto-scaling and security.", "level": "Advanced"},
    {"id": "cloud-architecture", "name": "Cloud Architecture", "description": "Designing high-availability multi-region cloud infrastructures.", "level": "Advanced"},
    {"id": "nginx", "name": "Nginx", "description": "High-performance reverse proxy server, load balancer, and HTTP cache.", "level": "Intermediate"},
    {"id": "monitoring-logging", "name": "Monitoring & Logging", "description": "Tracking software health metrics and debug logs (Prometheus, Grafana, ELK).", "level": "Intermediate"},

    # Security
    {"id": "cybersecurity-basics", "name": "Cybersecurity Basics", "description": "Foundational threat modeling, vulnerability detection, and secure practice.", "level": "Beginner"},
    {"id": "web-security", "name": "Web Security", "description": "Vulnerability protection covering CORS, CSRF, XSS, and security headers.", "level": "Intermediate"},
    {"id": "ssl-tls", "name": "SSL/TLS", "description": "Secure transport layer encryption protecting data transit.", "level": "Intermediate"},
    {"id": "cryptography", "name": "Cryptography", "description": "Encryption, decryption, hashing algorithms, and public-key infrastructure.", "level": "Advanced"},
    {"id": "cloud-security", "name": "Cloud Security", "description": "Securing cloud IAM roles, VPC networks, and infrastructure policies.", "level": "Advanced"},

    # Data Science & AI/ML
    {"id": "statistics", "name": "Statistics & Probability", "description": "Foundational statistical distribution, hypothesis testing, and probability modeling.", "level": "Intermediate"},
    {"id": "python-ds", "name": "Python for Data Science", "description": "Using Python's scientific libraries for descriptive and predictive data research.", "level": "Intermediate"},
    {"id": "pandas-numpy", "name": "Pandas & NumPy", "description": "Libraries for structured data analysis, manipulation, and array computation.", "level": "Intermediate"},
    {"id": "data-visualization", "name": "Data Visualization", "description": "Representing dataset trends visually (Matplotlib, Seaborn, D3.js).", "level": "Intermediate"},
    {"id": "machine-learning", "name": "Machine Learning Basics", "description": "Standard algorithms for classification, regression, and clustering.", "level": "Advanced"},
    {"id": "ai-engineering", "name": "AI Engineering", "description": "Building LLM applications, RAG pipelines, prompt engineering, and vector search.", "level": "Advanced"},
    {"id": "data-warehousing", "name": "Data Warehousing", "description": "Consolidating transactional datasets for analytical intelligence.", "level": "Advanced"},
    {"id": "etl-pipelines", "name": "ETL Pipelines", "description": "Extract, Transform, Load script workflows for backend data engineering.", "level": "Intermediate"},
    {"id": "apache-spark", "name": "Apache Spark", "description": "Unified analytical engine for large-scale distributed data processing.", "level": "Advanced"},

    # Testing & Process
    {"id": "testing-unit", "name": "Unit Testing", "description": "Testing small, isolated parts of software (functions, methods) for correctness.", "level": "Intermediate"},
    {"id": "testing-integration", "name": "Integration Testing", "description": "Testing groups of software modules together to verify collaborative behavior.", "level": "Intermediate"},
    {"id": "agile-scrum", "name": "Agile & Scrum", "description": "Modern software team project planning methodology and sprint processes.", "level": "Beginner"}
]

ROLES = [
    {"id": "frontend-developer", "name": "Frontend Developer", "description": "Builds responsive, high-performance web user interfaces using modern front-end frameworks."},
    {"id": "backend-developer", "name": "Backend Developer", "description": "Builds and secures scalable backend server APIs, databases, and microservices."},
    {"id": "fullstack-developer", "name": "Fullstack Developer", "description": "Possesses competency across the complete web stack, spanning database, server logic, and client UI."},
    {"id": "devops-engineer", "name": "DevOps Engineer", "description": "Automates development deployments, CI/CD pipelines, container orchestration, and server monitoring."},
    {"id": "data-engineer", "name": "Data Engineer", "description": "Processes and pipelines large datasets, engineering database engines, ETL networks, and analytical stores."},
    {"id": "security-engineer", "name": "Security Engineer", "description": "Protects systems and networks from threats, configuring cryptography, firewalls, and security policies."},
    {"id": "qa-engineer", "name": "QA Engineer", "description": "Assures software releases through automated unit, integration, end-to-end, and manual tests."},
    {"id": "software-engineer", "name": "Software Engineer", "description": "Designs, develops, and maintains software applications using core computer science principles and patterns."},
    {"id": "cloud-engineer", "name": "Cloud Engineer", "description": "Architects, provisions, and manages cloud infrastructure environments and deployment pipelines."},
    {"id": "ml-engineer", "name": "Machine Learning Engineer", "description": "Designs and deploys machine learning models and data processing pipelines into production environments."},
    {"id": "data-scientist", "name": "Data Scientist", "description": "Extracts insights from complex data through statistical research, predictive modeling, and data visualization."},
    {"id": "cybersecurity-analyst", "name": "Cybersecurity Analyst", "description": "Monitors networks, identifies vulnerabilities, and enforces web security policies and threat prevention."},
    {"id": "devsecops-engineer", "name": "DevSecOps Engineer", "description": "Integrates security practices into DevOps pipelines, container images, and cloud deployment infrastructure."},
    {"id": "ai-engineer", "name": "AI Engineer", "description": "Engineers applications leveraging generative AI, large language models, RAG pipelines, and vector databases."}
]

COURSES = [
    {"id": "intro-programming", "name": "Introduction to Programming", "description": "Foundational programming logic covering basic syntax, variables, loop structures, and conditionals."},
    {"id": "python-fundamentals", "name": "Python Fundamentals", "description": "Master core Python syntax, OOP concepts, data structures, and script execution."},
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
    {"id": "typescript-react", "name": "TypeScript with React", "description": "Type components, map interfaces, static typing state, and configure compilation options."},
    {"id": "system-design-masterclass", "name": "System Design Masterclass", "description": "Design distributed microservices, load balancing strategies, Redis caching, and fault tolerance."},
    {"id": "ml-engineering-course", "name": "Machine Learning Engineering", "description": "Train, evaluate, and deploy machine learning models with Python, Scikit-Learn, and Docker."},
    {"id": "ai-app-development", "name": "Generative AI & LLM App Development", "description": "Build LLM applications using LangChain, RAG architecture, vector search, and prompt engineering."},
    {"id": "cloud-architecture-aws", "name": "Cloud Architecture on AWS", "description": "Provision AWS cloud environments, Terraform IaC, IAM roles, VPC networks, and serverless APIs."}
]

PROJECTS = [
    {"id": "portfolio-website", "name": "Personal Portfolio Website", "description": "Static HTML/CSS responsive portfolio landing page showcasing work projects."},
    {"id": "weather-dashboard", "name": "JavaScript Weather Dashboard", "description": "Fetch live API data dynamically via browser DOM manipulation."},
    {"id": "task-manager-react", "name": "React Task Manager", "description": "Build interactive tasks boards, configuring complex local state and component styling."},
    {"id": "fastapi-blog-api", "name": "FastAPI Blog API", "description": "Backend database service providing full REST query routes for article entities."},
    {"id": "network-packet-sniffer", "name": "Python Packet Sniffer", "description": "Build a raw socket parser analyzing TCP header values in real-time."},
    {"id": "ecommerce-backend", "name": "E-commerce Backend Service", "description": "Microservice handling order checkout, JWT authentication, and relational DB tables."},
    {"id": "dockerized-app", "name": "Dockerized Multi-Container Application", "description": "Package frontend, backend, PostgreSQL DB, and Nginx reverse proxy into Compose."},
    {"id": "cicd-pipeline-project", "name": "Automated CI/CD Pipeline", "description": "Configure GitHub Actions workflows to build, test, and release Docker containers."},
    {"id": "data-analysis-report", "name": "Data Analysis & Visualization Report", "description": "Process CSV datasets with Pandas/NumPy and generate visual insight charts."},
    {"id": "chat-app-websockets", "name": "Realtime Chat App with WebSockets", "description": "Build persistent WebSocket servers with Node.js enabling instant multi-user messaging."},
    {"id": "system-design-simulator", "name": "Distributed Rate Limiter Simulator", "description": "Implement token-bucket rate limiting with Redis caching and system design principles."},
    {"id": "rag-knowledge-bot", "name": "RAG Knowledge Base Bot", "description": "Engineered AI document assistant using vector embeddings, Python, and OpenAI/Gemini APIs."},
    {"id": "terraform-aws-cluster", "name": "Terraform AWS Kubernetes Infrastructure", "description": "Provision infrastructure as code for EKS clusters, VPC networks, and security groups."},
    {"id": "devsecops-pipeline", "name": "DevSecOps Security Pipeline", "description": "Automate SAST security vulnerability scanning in Docker image CI/CD pipelines."},
    {"id": "ml-prediction-service", "name": "ML Model Microservice", "description": "Train predictive machine learning model and serve predictions via REST API endpoints."}
]

# Strict PREREQUISITE_OF edges (A must be learned before B)
PREREQUISITES = [
    # Core Programming & CS
    ("prog-fundamentals", "python"),
    ("prog-fundamentals", "javascript"),
    ("prog-fundamentals", "html"),
    ("prog-fundamentals", "git"),
    ("prog-fundamentals", "networking-basics"),
    ("prog-fundamentals", "sql"),
    ("prog-fundamentals", "data-structures"),
    ("data-structures", "algorithms"),
    ("prog-fundamentals", "clean-code"),
    ("clean-code", "software-engineering"),

    # Python Dependency Chain
    ("python", "python-oop"),
    ("python-oop", "python-backend"),
    ("python", "python-ds"),

    # Frontend Dependency Chain
    ("javascript", "dom-manipulation"),
    ("html", "css"),
    ("css", "responsive-design"),
    ("responsive-design", "css-animations"),
    ("css", "tailwind-css"),
    ("dom-manipulation", "react"),
    ("react", "state-management"),
    ("javascript", "typescript"),
    ("typescript", "next-js"),
    ("state-management", "frontend-architecture"),
    ("next-js", "frontend-architecture"),

    # Web Networking & API Chain
    ("networking-basics", "tcp-ip"),
    ("tcp-ip", "http-https"),
    ("networking-basics", "dns"),
    ("http-https", "json"),
    ("http-https", "rest-apis"),
    ("rest-apis", "api-design"),
    ("http-https", "authentication"),
    ("authentication", "authorization"),
    ("api-design", "backend-architecture"),
    ("authorization", "backend-architecture"),
    ("backend-architecture", "microservices"),
    ("microservices", "system-design"),
    ("graphql", "graphql-schemas"),

    # Database Dependency Chain
    ("sql", "databases-relational"),
    ("databases-relational", "database-design"),
    ("database-design", "orm-concepts"),

    # DevOps & Infrastructure Chain
    ("linux-cli", "bash-scripting"),
    ("bash-scripting", "docker"),
    ("docker", "ci-cd"),
    ("docker", "kubernetes"),
    ("kubernetes", "container-orchestration"),
    ("cloud-basics", "infrastructure-as-code"),
    ("infrastructure-as-code", "cloud-deployment"),
    ("cloud-deployment", "cloud-architecture"),
    ("docker", "monitoring-logging"),

    # Security Dependency Chain
    ("cybersecurity-basics", "web-security"),
    ("networking-basics", "ssl-tls"),
    ("cybersecurity-basics", "cryptography"),
    ("cloud-basics", "cloud-security"),

    # Data & AI/ML Chain
    ("python", "statistics"),
    ("python-ds", "pandas-numpy"),
    ("pandas-numpy", "data-visualization"),
    ("pandas-numpy", "machine-learning"),
    ("machine-learning", "ai-engineering"),
    ("sql", "etl-pipelines"),
    ("etl-pipelines", "data-warehousing"),
    ("data-warehousing", "apache-spark"),

    # Testing & Process
    ("prog-fundamentals", "testing-unit"),
    ("testing-unit", "testing-integration")
]

# Role requirements (REQUIRES)
REQUIRES = [
    # Frontend Developer
    ("frontend-developer", "html"),
    ("frontend-developer", "css"),
    ("frontend-developer", "javascript"),
    ("frontend-developer", "dom-manipulation"),
    ("frontend-developer", "react"),
    ("frontend-developer", "state-management"),
    ("frontend-developer", "typescript"),
    ("frontend-developer", "git"),

    # Backend Developer
    ("backend-developer", "python"),
    ("backend-developer", "http-https"),
    ("backend-developer", "rest-apis"),
    ("backend-developer", "authentication"),
    ("backend-developer", "sql"),
    ("backend-developer", "databases-relational"),
    ("backend-developer", "git"),
    ("backend-developer", "docker"),
    ("backend-developer", "testing-unit"),

    # Fullstack Developer
    ("fullstack-developer", "javascript"),
    ("fullstack-developer", "react"),
    ("fullstack-developer", "node-js"),
    ("fullstack-developer", "rest-apis"),
    ("fullstack-developer", "sql"),
    ("fullstack-developer", "databases-relational"),
    ("fullstack-developer", "docker"),
    ("fullstack-developer", "git"),

    # DevOps Engineer
    ("devops-engineer", "linux-cli"),
    ("devops-engineer", "bash-scripting"),
    ("devops-engineer", "docker"),
    ("devops-engineer", "kubernetes"),
    ("devops-engineer", "ci-cd"),
    ("devops-engineer", "cloud-basics"),
    ("devops-engineer", "monitoring-logging"),

    # Data Engineer
    ("data-engineer", "python"),
    ("data-engineer", "sql"),
    ("data-engineer", "databases-relational"),
    ("data-engineer", "databases-nosql"),
    ("data-engineer", "etl-pipelines"),
    ("data-engineer", "data-warehousing"),
    ("data-engineer", "docker"),

    # Security Engineer
    ("security-engineer", "networking-basics"),
    ("security-engineer", "web-security"),
    ("security-engineer", "ssl-tls"),
    ("security-engineer", "cryptography"),
    ("security-engineer", "cybersecurity-basics"),
    ("security-engineer", "cloud-security"),

    # QA Engineer
    ("qa-engineer", "testing-unit"),
    ("qa-engineer", "testing-integration"),
    ("qa-engineer", "python"),
    ("qa-engineer", "git"),
    ("qa-engineer", "rest-apis"),

    # Software Engineer
    ("software-engineer", "prog-fundamentals"),
    ("software-engineer", "data-structures"),
    ("software-engineer", "algorithms"),
    ("software-engineer", "clean-code"),
    ("software-engineer", "git"),
    ("software-engineer", "testing-unit"),

    # Cloud Engineer
    ("cloud-engineer", "cloud-basics"),
    ("cloud-engineer", "infrastructure-as-code"),
    ("cloud-engineer", "cloud-deployment"),
    ("cloud-engineer", "docker"),
    ("cloud-engineer", "networking-basics"),
    ("cloud-engineer", "linux-cli"),

    # Machine Learning Engineer
    ("ml-engineer", "python"),
    ("ml-engineer", "data-structures"),
    ("ml-engineer", "statistics"),
    ("ml-engineer", "pandas-numpy"),
    ("ml-engineer", "machine-learning"),
    ("ml-engineer", "docker"),
    ("ml-engineer", "git"),

    # Data Scientist
    ("data-scientist", "python"),
    ("data-scientist", "statistics"),
    ("data-scientist", "python-ds"),
    ("data-scientist", "pandas-numpy"),
    ("data-scientist", "data-visualization"),
    ("data-scientist", "sql"),

    # Cybersecurity Analyst
    ("cybersecurity-analyst", "cybersecurity-basics"),
    ("cybersecurity-analyst", "networking-basics"),
    ("cybersecurity-analyst", "web-security"),
    ("cybersecurity-analyst", "linux-cli"),

    # DevSecOps Engineer
    ("devsecops-engineer", "docker"),
    ("devsecops-engineer", "ci-cd"),
    ("devsecops-engineer", "web-security"),
    ("devsecops-engineer", "cloud-security"),
    ("devsecops-engineer", "linux-cli"),

    # AI Engineer
    ("ai-engineer", "python"),
    ("ai-engineer", "pandas-numpy"),
    ("ai-engineer", "machine-learning"),
    ("ai-engineer", "ai-engineering"),
    ("ai-engineer", "rest-apis"),
    ("ai-engineer", "docker")
]

# TEACHES relationships (Courses -> Skill)
TEACHES = [
    ("intro-programming", "prog-fundamentals"),
    ("python-fundamentals", "python"),
    ("python-fundamentals", "python-oop"),
    ("git-github", "git"),
    ("html-css-basics", "html"),
    ("html-css-basics", "css"),
    ("js-deep-dive", "javascript"),
    ("js-deep-dive", "dom-manipulation"),
    ("modern-react", "react"),
    ("modern-react", "state-management"),
    ("python-backend", "python"),
    ("python-backend", "rest-apis"),
    ("python-backend", "api-design"),
    ("sql-databases", "sql"),
    ("sql-databases", "databases-relational"),
    ("sql-databases", "database-design"),
    ("docker-containers", "docker"),
    ("web-networking", "networking-basics"),
    ("web-networking", "tcp-ip"),
    ("web-networking", "http-https"),
    ("web-security-guide", "web-security"),
    ("web-security-guide", "authentication"),
    ("web-security-guide", "authorization"),
    ("ds-algo-python", "data-structures"),
    ("ds-algo-python", "algorithms"),
    ("devops-bootcamp", "ci-cd"),
    ("devops-bootcamp", "kubernetes"),
    ("devops-bootcamp", "monitoring-logging"),
    ("data-science-intro", "python-ds"),
    ("data-science-intro", "statistics"),
    ("data-science-intro", "pandas-numpy"),
    ("node-express", "node-js"),
    ("node-express", "rest-apis"),
    ("typescript-react", "typescript"),
    ("typescript-react", "react"),
    ("system-design-masterclass", "system-design"),
    ("system-design-masterclass", "backend-architecture"),
    ("system-design-masterclass", "microservices"),
    ("ml-engineering-course", "machine-learning"),
    ("ai-app-development", "ai-engineering"),
    ("cloud-architecture-aws", "cloud-basics"),
    ("cloud-architecture-aws", "infrastructure-as-code"),
    ("cloud-architecture-aws", "cloud-deployment")
]

# BUILDS relationships (Project -> Skill)
BUILDS = [
    ("portfolio-website", "html"),
    ("portfolio-website", "css"),
    ("portfolio-website", "responsive-design"),
    ("weather-dashboard", "javascript"),
    ("weather-dashboard", "dom-manipulation"),
    ("weather-dashboard", "http-https"),
    ("task-manager-react", "react"),
    ("task-manager-react", "state-management"),
    ("fastapi-blog-api", "python"),
    ("fastapi-blog-api", "rest-apis"),
    ("fastapi-blog-api", "api-design"),
    ("fastapi-blog-api", "sql"),
    ("network-packet-sniffer", "python"),
    ("network-packet-sniffer", "tcp-ip"),
    ("network-packet-sniffer", "networking-basics"),
    ("ecommerce-backend", "node-js"),
    ("ecommerce-backend", "rest-apis"),
    ("ecommerce-backend", "authentication"),
    ("ecommerce-backend", "authorization"),
    ("ecommerce-backend", "databases-relational"),
    ("dockerized-app", "docker"),
    ("dockerized-app", "nginx"),
    ("dockerized-app", "databases-relational"),
    ("cicd-pipeline-project", "ci-cd"),
    ("cicd-pipeline-project", "docker"),
    ("cicd-pipeline-project", "git"),
    ("data-analysis-report", "pandas-numpy"),
    ("data-analysis-report", "data-visualization"),
    ("data-analysis-report", "statistics"),
    ("chat-app-websockets", "node-js"),
    ("chat-app-websockets", "web-sockets"),
    ("system-design-simulator", "system-design"),
    ("system-design-simulator", "redis-caching"),
    ("rag-knowledge-bot", "python"),
    ("rag-knowledge-bot", "ai-engineering"),
    ("terraform-aws-cluster", "infrastructure-as-code"),
    ("terraform-aws-cluster", "kubernetes"),
    ("devsecops-pipeline", "ci-cd"),
    ("devsecops-pipeline", "web-security"),
    ("ml-prediction-service", "machine-learning"),
    ("ml-prediction-service", "rest-apis")
]

# Strictly RELATED_TO (Complementary / alternative / adjacent skills)
RELATED_TO = [
    ("rest-apis", "graphql"),
    ("databases-relational", "databases-nosql"),
    ("databases-relational", "databases-graph"),
    ("databases-relational", "redis-caching"),
    ("databases-nosql", "databases-graph"),
    ("react", "tailwind-css"),
    ("docker", "nginx"),
    ("authentication", "cryptography"),
    ("data-structures", "pandas-numpy"),
    ("agile-scrum", "clean-code"),
    ("css-animations", "responsive-design"),
    ("python-ds", "statistics"),
    ("microservices", "message-queues")
]


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
        
    print(f"Connecting to database at {uri}...")
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        print("\nBatch Seeding Nodes...")
        with driver.session() as session:
            # Batch seed Skills
            print(f" - Seeding {len(SKILLS)} Skills...")
            session.run("""
                UNWIND $batch AS row
                MERGE (s:Skill {id: row.id})
                SET s.name = row.name, s.description = row.description, s.level = row.level
            """, batch=SKILLS)

            # Batch seed Roles
            print(f" - Seeding {len(ROLES)} Roles...")
            session.run("""
                UNWIND $batch AS row
                MERGE (r:Role {id: row.id})
                SET r.name = row.name, r.description = row.description
            """, batch=ROLES)

            # Batch seed Courses
            print(f" - Seeding {len(COURSES)} Courses...")
            session.run("""
                UNWIND $batch AS row
                MERGE (c:Course {id: row.id})
                SET c.name = row.name, c.description = row.description
            """, batch=COURSES)

            # Batch seed Projects
            print(f" - Seeding {len(PROJECTS)} Projects...")
            session.run("""
                UNWIND $batch AS row
                MERGE (p:Project {id: row.id})
                SET p.name = row.name, p.description = row.description
            """, batch=PROJECTS)

        print("\nBatch Seeding Relationships...")
        with driver.session() as session:
            # Batch PREREQUISITE_OF
            print(f" - Seeding {len(PREREQUISITES)} PREREQUISITE_OF relationships...")
            session.run("""
                UNWIND $batch AS row
                MATCH (a:Skill {id: row[0]})
                MATCH (b:Skill {id: row[1]})
                MERGE (a)-[:PREREQUISITE_OF]->(b)
            """, batch=PREREQUISITES)

            # Batch REQUIRES
            print(f" - Seeding {len(REQUIRES)} REQUIRES relationships...")
            session.run("""
                UNWIND $batch AS row
                MATCH (a:Role {id: row[0]})
                MATCH (b:Skill {id: row[1]})
                MERGE (a)-[:REQUIRES]->(b)
            """, batch=REQUIRES)

            # Batch TEACHES
            print(f" - Seeding {len(TEACHES)} TEACHES relationships...")
            session.run("""
                UNWIND $batch AS row
                MATCH (a:Course {id: row[0]})
                MATCH (b:Skill {id: row[1]})
                MERGE (a)-[:TEACHES]->(b)
            """, batch=TEACHES)

            # Batch BUILDS
            print(f" - Seeding {len(BUILDS)} BUILDS relationships...")
            session.run("""
                UNWIND $batch AS row
                MATCH (a:Project {id: row[0]})
                MATCH (b:Skill {id: row[1]})
                MERGE (a)-[:BUILDS]->(b)
            """, batch=BUILDS)

            # Batch RELATED_TO
            print(f" - Seeding {len(RELATED_TO)} RELATED_TO relationships...")
            session.run("""
                UNWIND $batch AS row
                MATCH (a:Skill {id: row[0]})
                MATCH (b:Skill {id: row[1]})
                MERGE (a)-[:RELATED_TO]->(b)
            """, batch=RELATED_TO)

        # Verification
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
