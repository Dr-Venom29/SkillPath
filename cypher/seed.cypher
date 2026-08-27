// 1. Wipe database before seeding
MATCH (n) DETACH DELETE n;

// 2. Create Skill Nodes
CREATE (s1:Skill {id: "prog-fundamentals", name: "Programming Fundamentals", description: "Basic concepts of programming including variables, loops, conditions, and basic logic.", level: "Beginner"})
CREATE (s2:Skill {id: "python", name: "Python", description: "General-purpose high-level programming language known for readability and clean syntax.", level: "Beginner"})
CREATE (s3:Skill {id: "javascript", name: "JavaScript", description: "Dynamic scripting language for web pages, enabling client-side interactivity.", level: "Beginner"})
CREATE (s4:Skill {id: "typescript", name: "TypeScript", description: "Typed superset of JavaScript that compiles to plain JavaScript for larger-scale applications.", level: "Intermediate"})
CREATE (s5:Skill {id: "html", name: "HTML", description: "HyperText Markup Language, the standard document format for web browsers.", level: "Beginner"})
CREATE (s6:Skill {id: "css", name: "CSS", description: "Cascading Style Sheets, used for describing the presentation of web pages.", level: "Beginner"})
CREATE (s7:Skill {id: "dom-manipulation", name: "DOM Manipulation", description: "Interacting with the browser Document Object Model dynamically via script.", level: "Beginner"})
CREATE (s8:Skill {id: "react", name: "React", description: "A popular front-end JavaScript library for building component-based user interfaces.", level: "Intermediate"})
CREATE (s9:Skill {id: "state-management", name: "State Management", description: "Managing data state across complex component trees (Redux, Zustand, Context API).", level: "Intermediate"})
CREATE (s10:Skill {id: "tailwind-css", name: "Tailwind CSS", description: "Utility-first CSS framework for rapid and highly customizable UI design.", level: "Beginner"})
CREATE (s11:Skill {id: "git", name: "Git", description: "Distributed version control system for tracking changes in source code.", level: "Beginner"})
CREATE (s12:Skill {id: "linux-cli", name: "Linux Command Line", description: "Operating system shell interface for file manipulation and process execution.", level: "Beginner"})
CREATE (s13:Skill {id: "networking-basics", name: "Networking Basics", description: "Foundational concepts of networks, connections, routing, and communication protocols.", level: "Beginner"})
CREATE (s14:Skill {id: "tcp-ip", name: "TCP/IP", description: "Transmission Control Protocol/Internet Protocol, basic communication protocol stack.", level: "Beginner"})
CREATE (s15:Skill {id: "http-https", name: "HTTP/HTTPS", description: "Web transfer protocols enabling data transfer and secure end-to-end connections.", level: "Beginner"})
CREATE (s16:Skill {id: "dns", name: "DNS", description: "Domain Name System, translating human-readable hostnames to IP addresses.", level: "Beginner"})
CREATE (s17:Skill {id: "json", name: "JSON", description: "JavaScript Object Notation, standard lightweight data interchange format.", level: "Beginner"})
CREATE (s18:Skill {id: "rest-apis", name: "REST APIs", description: "Representational State Transfer APIs, standard architectural style for web services.", level: "Intermediate"})
CREATE (s19:Skill {id: "graphql", name: "GraphQL", description: "Query language for APIs and runtime for executing queries with existing data.", level: "Intermediate"})
CREATE (s20:Skill {id: "authentication", name: "Authentication", description: "Proving identity via tokens, passwords, OAuth, session management, or cookies.", level: "Intermediate"})
CREATE (s21:Skill {id: "sql", name: "SQL", description: "Structured Query Language for querying and managing relational databases.", level: "Beginner"})
CREATE (s22:Skill {id: "databases-relational", name: "Relational Databases", description: "Tabular database engines ensuring ACID guarantees (PostgreSQL, MySQL).", level: "Intermediate"})
CREATE (s23:Skill {id: "databases-nosql", name: "NoSQL Databases", description: "Non-tabular database engines (Document, Key-Value, Columnar) like MongoDB.", level: "Intermediate"})
CREATE (s24:Skill {id: "databases-graph", name: "Graph Databases", description: "Highly-connected database engines optimized for network relations (Neo4j).", level: "Advanced"})
CREATE (s25:Skill {id: "data-structures", name: "Data Structures", description: "Organizing and storing data in computer memory (Arrays, Lists, Trees, Graphs).", level: "Intermediate"})
CREATE (s26:Skill {id: "algorithms", name: "Algorithms", description: "Step-by-step logic procedures for sorting, searching, and optimization tasks.", level: "Intermediate"})
CREATE (s27:Skill {id: "testing-unit", name: "Unit Testing", description: "Testing small, isolated parts of software (functions, methods) for correctness.", level: "Intermediate"})
CREATE (s28:Skill {id: "testing-integration", name: "Integration Testing", description: "Testing groups of software modules together to verify collaborative behavior.", level: "Intermediate"})
CREATE (s29:Skill {id: "docker", name: "Docker", description: "Standard containerization platform for packaging applications and dependencies.", level: "Intermediate"})
CREATE (s30:Skill {id: "ci-cd", name: "CI/CD", description: "Continuous Integration & Deployment pipelines for automated software release.", level: "Intermediate"})
CREATE (s31:Skill {id: "cloud-basics", name: "Cloud Basics", description: "Fundamental cloud architecture and services (EC2, S3, IAM, Serverless).", level: "Intermediate"})
CREATE (s32:Skill {id: "kubernetes", name: "Kubernetes", description: "Container orchestration engine for automated scaling, updates, and load balancing.", level: "Advanced"})
CREATE (s33:Skill {id: "monitoring-logging", name: "Monitoring & Logging", description: "Tracking software health metrics and debug logs (Prometheus, Grafana, ELK).", level: "Intermediate"})
CREATE (s34:Skill {id: "web-security", name: "Web Security", description: "Vulnerability protection covering CORS, CSRF, XSS, and security headers.", level: "Intermediate"})
CREATE (s35:Skill {id: "ssl-tls", name: "SSL/TLS", description: "Secure transport layer encryption protecting data transit.", level: "Intermediate"})
CREATE (s36:Skill {id: "python-ds", name: "Python for Data Science", description: "Using Python's scientific libraries for descriptive and predictive data research.", level: "Intermediate"})
CREATE (s37:Skill {id: "pandas-numpy", name: "Pandas & NumPy", description: "Libraries for structured data analysis, manipulation, and array computation.", level: "Intermediate"})
CREATE (s38:Skill {id: "data-visualization", name: "Data Visualization", description: "Representing dataset trends visually (Matplotlib, Seaborn, D3.js).", level: "Intermediate"})
CREATE (s39:Skill {id: "machine-learning", name: "Machine Learning Basics", description: "Standard algorithms for classification, regression, and clustering.", level: "Advanced"})
CREATE (s40:Skill {id: "message-queues", name: "Message Queues", description: "Asynchronous task workers and brokers (RabbitMQ, Kafka, Redis PubSub).", level: "Advanced"})
CREATE (s41:Skill {id: "node-js", name: "Node.js", description: "V8-powered asynchronous JavaScript runtime for server-side execution.", level: "Intermediate"})
CREATE (s42:Skill {id: "web-sockets", name: "WebSockets", description: "Full-duplex persistent communication channel over a single TCP connection.", level: "Intermediate"})
CREATE (s43:Skill {id: "nginx", name: "Nginx", description: "High-performance reverse proxy server, load balancer, and HTTP cache.", level: "Intermediate"})
CREATE (s44:Skill {id: "bash-scripting", name: "Bash Scripting", description: "Shell scripting languages for OS-level task automation.", level: "Intermediate"})
CREATE (s45:Skill {id: "api-design", name: "API Design", description: "Synthesizing clean, standardized backend endpoints (routes, requests, responses).", level: "Intermediate"})
CREATE (s46:Skill {id: "microservices", name: "Microservices", description: "Decomposing applications into independent, networked functional modules.", level: "Advanced"})
CREATE (s47:Skill {id: "system-design", name: "System Design", description: "Planning scale architectures, load balancing, caching, and data partitions.", level: "Advanced"})
CREATE (s48:Skill {id: "redis-caching", name: "Redis & Caching", description: "In-memory database structure store used for caching and session stores.", level: "Intermediate"})
CREATE (s49:Skill {id: "orm-concepts", name: "ORM Concepts", description: "Object-Relational Mapping (Prisma, SQLAlchemy) translating code queries to SQL.", level: "Intermediate"})
CREATE (s50:Skill {id: "cybersecurity-basics", name: "Cybersecurity Basics", description: "Foundational threat modeling, vulnerability detection, and secure practice.", level: "Beginner"})
CREATE (s51:Skill {id: "cryptography", name: "Cryptography", description: "Encryption, decryption, hashing algorithms, and public-key infrastructure.", level: "Advanced"})
CREATE (s52:Skill {id: "data-warehousing", name: "Data Warehousing", description: "Consolidating transactional datasets for analytical intelligence.", level: "Advanced"})
CREATE (s53:Skill {id: "etl-pipelines", name: "ETL Pipelines", description: "Extract, Transform, Load script workflows for backend data engineering.", level: "Intermediate"})
CREATE (s54:Skill {id: "apache-spark", name: "Apache Spark", description: "Unified analytical engine for large-scale distributed data processing.", level: "Advanced"})
CREATE (s55:Skill {id: "clean-code", name: "Clean Code Practices", description: "Writing readable, maintainable, modular, and well-tested code code bases.", level: "Intermediate"})
CREATE (s56:Skill {id: "agile-scrum", name: "Agile & Scrum", description: "Modern software team project planning methodology and sprint processes.", level: "Beginner"})
CREATE (s57:Skill {id: "responsive-design", name: "Responsive Design", description: "CSS styling techniques for rendering across varied device viewports.", level: "Beginner"})
CREATE (s58:Skill {id: "css-animations", name: "CSS Animations", description: "Transitions, keyframes, and animations defining rich visual motion.", level: "Intermediate"})
CREATE (s59:Skill {id: "next-js", name: "Next.js", description: "React meta-framework enabling server-side rendering, routing, and optimization.", level: "Advanced"})
CREATE (s60:Skill {id: "graphql-schemas", name: "GraphQL Schemas", description: "Defining query fields, mutation routes, and strict type schemas for APIs.", level: "Intermediate"})

// 3. Create Role Nodes
CREATE (r1:Role {id: "frontend-developer", name: "Frontend Developer", description: "Builds responsive, high-performance web user interfaces using modern front-end frameworks."})
CREATE (r2:Role {id: "backend-developer", name: "Backend Developer", description: "Builds and secures scalable backend server APIs, databases, and microservices."})
CREATE (r3:Role {id: "fullstack-developer", name: "Fullstack Developer", description: "Possesses competency across the complete web stack, spanning database, server logic, and client UI."})
CREATE (r4:Role {id: "devops-engineer", name: "DevOps Engineer", description: "Automates development deployments, CI/CD pipelines, container orchestration, and server monitoring."})
CREATE (r5:Role {id: "data-engineer", name: "Data Engineer", description: "Processes and pipelines large datasets, engineering database engines, ETL networks, and analytical stores."})
CREATE (r6:Role {id: "security-engineer", name: "Security Engineer", description: "Protects systems and networks from threats, configuring cryptography, firewalls, and security policies."})
CREATE (r7:Role {id: "qa-engineer", name: "QA Engineer", description: "Assures software releases through automated unit, integration, end-to-end, and manual tests."})

// 4. Create Course Nodes
CREATE (c1:Course {id: "intro-programming", name: "Introduction to Programming", description: "Foundational programming logic covering basic syntax, variables, loop structures, and conditionals."})
CREATE (c2:Course {id: "git-github", name: "Git & GitHub Version Control", description: "Master version tracking, pull requests, merges, conflict resolution, and branching."})
CREATE (c3:Course {id: "html-css-basics", name: "HTML & CSS for Beginners", description: "Learn layout engines, selectors, responsive structure, and web style practices."})
CREATE (c4:Course {id: "js-deep-dive", name: "JavaScript Deep Dive", description: "Core asynchronous patterns, callbacks, promises, closures, dynamic execution, and browser API."})
CREATE (c5:Course {id: "modern-react", name: "Modern React & State Management", description: "JSX syntax, components, rendering lifecycles, hooks, and dynamic data state providers."})
CREATE (c6:Course {id: "python-backend", name: "Python Backend Development with FastAPI", description: "API services, routing, validation, Pydantic, parameters, and unit testing integration."})
CREATE (c7:Course {id: "sql-databases", name: "SQL & Relational Databases", description: "Query construction, table normalization, primary/foreign keys, joins, indexes, and ACID rules."})
CREATE (c8:Course {id: "docker-containers", name: "Docker & Containerization", description: "Create images, write Dockerfiles, configure volumes, networks, and compose multi-container systems."})
CREATE (c9:Course {id: "web-networking", name: "Web Networking Fundamentals", description: "Understand HTTP protocols, DNS servers, TCP/IP handshakes, network routing, and IP addressing."})
CREATE (c10:Course {id: "web-security-guide", name: "Practical Web Security", description: "Vulnerability analysis, security headers, token auth, JWT, cookies, and CORS configuration."})
CREATE (c11:Course {id: "ds-algo-python", name: "Data Structures & Algorithms in Python", description: "Implement binary trees, graphs, sorting lists, hash tables, big-O analysis, and algorithms."})
CREATE (c12:Course {id: "devops-bootcamp", name: "DevOps Bootcamp", description: "Automated pipelines, Kubernetes configurations, cloud compute setup, and log dashboards."})
CREATE (c13:Course {id: "data-science-intro", name: "Introduction to Data Science", description: "Analyze mathematical distributions, manipulate matrices, clean datasets, and draw insights."})
CREATE (c14:Course {id: "node-express", name: "Node.js & Express API Development", description: "Write server endpoints, construct middle-wares, handle exceptions, and route JSON operations."})
CREATE (c15:Course {id: "typescript-react", name: "TypeScript with React", description: "Type components, map interfaces, static typing state, and configure compilation options."})

// 5. Create Project Nodes
CREATE (p1:Project {id: "portfolio-website", name: "Personal Portfolio Website", description: "Static HTML/CSS responsive portfolio landing page showcasing work projects."})
CREATE (p2:Project {id: "task-manager-react", name: "React Task Manager", description: "Build interactive tasks boards, configuring complex local state and component styling."})
CREATE (p3:Project {id: "weather-dashboard-js", name: "JavaScript Weather Dashboard", description: "Dynamic browser application querying external weather services using fetch APIs."})
CREATE (p4:Project {id: "blog-api-fastapi", name: "FastAPI Blog API", description: "Backend database service providing full REST query routes for article entities."})
CREATE (p5:Project {id: "e-commerce-backend", name: "E-commerce Backend Service", description: "Scale relational database engine, handle authentication profiles, and query transactions."})
CREATE (p6:Project {id: "containerized-app", name: "Dockerized Multi-Container Application", description: "Bundle web app servers and SQL databases inside compose networks."})
CREATE (p7:Project {id: "ci-cd-pipeline-deploy", name: "Automated CI/CD Pipeline", description: "Create Git actions scripts mapping deployment pipelines to cloud environments."})
CREATE (p8:Project {id: "network-packet-sniffer", name: "Python Packet Sniffer", description: "Build a raw socket parser analyzing TCP header values in real-time."})
CREATE (p9:Project {id: "data-analysis-report", name: "Sales Data Analysis Report", description: "Write Jupyter scripts aggregating multi-year customer data outputs."})
CREATE (p10:Project {id: "chat-app-websockets", name: "Real-Time Chat Application", description: "Build full WebSocket pipelines pushing instant messages to connected users."})

// 6. Connect Skills - PREREQUISITE_OF
CREATE
(s1)-[:PREREQUISITE_OF]->(s2),
(s1)-[:PREREQUISITE_OF]->(s3),
(s3)-[:PREREQUISITE_OF]->(s7),
(s7)-[:PREREQUISITE_OF]->(s8),
(s8)-[:PREREQUISITE_OF]->(s59),
(s3)-[:PREREQUISITE_OF]->(s4),
(s4)-[:PREREQUISITE_OF]->(s59),
(s8)-[:PREREQUISITE_OF]->(s9),
(s5)-[:PREREQUISITE_OF]->(s7),
(s6)-[:PREREQUISITE_OF]->(s57),
(s57)-[:PREREQUISITE_OF]->(s10),
(s6)-[:PREREQUISITE_OF]->(s58),
(s13)-[:PREREQUISITE_OF]->(s14),
(s14)-[:PREREQUISITE_OF]->(s15),
(s15)-[:PREREQUISITE_OF]->(s16),
(s15)-[:PREREQUISITE_OF]->(s18),
(s17)-[:PREREQUISITE_OF]->(s18),
(s18)-[:PREREQUISITE_OF]->(s20),
(s18)-[:PREREQUISITE_OF]->(s19),
(s19)-[:PREREQUISITE_OF]->(s60),
(s21)-[:PREREQUISITE_OF]->(s22),
(s22)-[:PREREQUISITE_OF]->(s49),
(s22)-[:PREREQUISITE_OF]->(s48),
(s23)-[:PREREQUISITE_OF]->(s48),
(s22)-[:PREREQUISITE_OF]->(s24),
(s25)-[:PREREQUISITE_OF]->(s26),
(s1)-[:PREREQUISITE_OF]->(s25),
(s12)-[:PREREQUISITE_OF]->(s44),
(s11)-[:PREREQUISITE_OF]->(s30),
(s29)-[:PREREQUISITE_OF]->(s32),
(s29)-[:PREREQUISITE_OF]->(s30),
(s31)-[:PREREQUISITE_OF]->(s32),
(s30)-[:PREREQUISITE_OF]->(s33),
(s15)-[:PREREQUISITE_OF]->(s34),
(s34)-[:PREREQUISITE_OF]->(s35),
(s34)-[:PREREQUISITE_OF]->(s20),
(s50)-[:PREREQUISITE_OF]->(s51),
(s2)-[:PREREQUISITE_OF]->(s36),
(s36)-[:PREREQUISITE_OF]->(s37),
(s37)-[:PREREQUISITE_OF]->(s38),
(s37)-[:PREREQUISITE_OF]->(s39),
(s22)-[:PREREQUISITE_OF]->(s52),
(s52)-[:PREREQUISITE_OF]->(s53),
(s53)-[:PREREQUISITE_OF]->(s54),
(s18)-[:PREREQUISITE_OF]->(s45),
(s45)-[:PREREQUISITE_OF]->(s46),
(s46)-[:PREREQUISITE_OF]->(s47),
(s27)-[:PREREQUISITE_OF]->(s28),
(s55)-[:PREREQUISITE_OF]->(s47),
(s43)-[:PREREQUISITE_OF]->(s46)

// 7. Connect Roles - REQUIRES
CREATE
(r1)-[:REQUIRES]->(s5),
(r1)-[:REQUIRES]->(s6),
(r1)-[:REQUIRES]->(s3),
(r1)-[:REQUIRES]->(s8),
(r1)-[:REQUIRES]->(s11),
(r1)-[:REQUIRES]->(s10),
(r1)-[:REQUIRES]->(s4),
(r2)-[:REQUIRES]->(s2),
(r2)-[:REQUIRES]->(s41),
(r2)-[:REQUIRES]->(s21),
(r2)-[:REQUIRES]->(s22),
(r2)-[:REQUIRES]->(s18),
(r2)-[:REQUIRES]->(s11),
(r2)-[:REQUIRES]->(s27),
(r2)-[:REQUIRES]->(s29),
(r3)-[:REQUIRES]->(s5),
(r3)-[:REQUIRES]->(s3),
(r3)-[:REQUIRES]->(s8),
(r3)-[:REQUIRES]->(s41),
(r3)-[:REQUIRES]->(s22),
(r3)-[:REQUIRES]->(s18),
(r3)-[:REQUIRES]->(s11),
(r4)-[:REQUIRES]->(s12),
(r4)-[:REQUIRES]->(s44),
(r4)-[:REQUIRES]->(s11),
(r4)-[:REQUIRES]->(s29),
(r4)-[:REQUIRES]->(s30),
(r4)-[:REQUIRES]->(s32),
(r4)-[:REQUIRES]->(s31),
(r5)-[:REQUIRES]->(s2),
(r5)-[:REQUIRES]->(s21),
(r5)-[:REQUIRES]->(s22),
(r5)-[:REQUIRES]->(s37),
(r5)-[:REQUIRES]->(s53),
(r5)-[:REQUIRES]->(s54),
(r6)-[:REQUIRES]->(s13),
(r6)-[:REQUIRES]->(s14),
(r6)-[:REQUIRES]->(s34),
(r6)-[:REQUIRES]->(s35),
(r6)-[:REQUIRES]->(s50),
(r6)-[:REQUIRES]->(s51),
(r7)-[:REQUIRES]->(s1),
(r7)-[:REQUIRES]->(s2),
(r7)-[:REQUIRES]->(s27),
(r7)-[:REQUIRES]->(s28),
(r7)-[:REQUIRES]->(s11)

// 8. Connect Courses - TEACHES
CREATE
(c1)-[:TEACHES]->(s1),
(c1)-[:TEACHES]->(s2),
(c2)-[:TEACHES]->(s11),
(c3)-[:TEACHES]->(s5),
(c3)-[:TEACHES]->(s6),
(c4)-[:TEACHES]->(s3),
(c4)-[:TEACHES]->(s7),
(c5)-[:TEACHES]->(s8),
(c5)-[:TEACHES]->(s9),
(c6)-[:TEACHES]->(s2),
(c6)-[:TEACHES]->(s18),
(c6)-[:TEACHES]->(s27),
(c7)-[:TEACHES]->(s21),
(c7)-[:TEACHES]->(s22),
(c8)-[:TEACHES]->(s29),
(c9)-[:TEACHES]->(s13),
(c9)-[:TEACHES]->(s14),
(c9)-[:TEACHES]->(s15),
(c10)-[:TEACHES]->(s34),
(c10)-[:TEACHES]->(s20),
(c11)-[:TEACHES]->(s25),
(c11)-[:TEACHES]->(s26),
(c12)-[:TEACHES]->(s30),
(c12)-[:TEACHES]->(s32),
(c12)-[:TEACHES]->(s31),
(c13)-[:TEACHES]->(s36),
(c13)-[:TEACHES]->(s37),
(c14)-[:TEACHES]->(s41),
(c14)-[:TEACHES]->(s18),
(c15)-[:TEACHES]->(s4),
(c15)-[:TEACHES]->(s8)

// 9. Connect Projects - BUILDS
CREATE
(p1)-[:BUILDS]->(s5),
(p1)-[:BUILDS]->(s6),
(p1)-[:BUILDS]->(s57),
(p2)-[:BUILDS]->(s8),
(p2)-[:BUILDS]->(s9),
(p3)-[:BUILDS]->(s3),
(p3)-[:BUILDS]->(s7),
(p3)-[:BUILDS]->(s15),
(p4)-[:BUILDS]->(s2),
(p4)-[:BUILDS]->(s18),
(p4)-[:BUILDS]->(s21),
(p5)-[:BUILDS]->(s41),
(p5)-[:BUILDS]->(s22),
(p5)-[:BUILDS]->(s20),
(p6)-[:BUILDS]->(s29),
(p6)-[:BUILDS]->(s22),
(p7)-[:BUILDS]->(s30),
(p7)-[:BUILDS]->(s31),
(p8)-[:BUILDS]->(s2),
(p8)-[:BUILDS]->(s14),
(p9)-[:BUILDS]->(s37),
(p9)-[:BUILDS]->(s38),
(p10)-[:BUILDS]->(s41),
(p10)-[:BUILDS]->(s42),
(p10)-[:BUILDS]->(s34)

// 10. Connect Skills - RELATED_TO
CREATE
(s18)-[:RELATED_TO]->(s19),
(s22)-[:RELATED_TO]->(s23),
(s22)-[:RELATED_TO]->(s24),
(s23)-[:RELATED_TO]->(s24),
(s8)-[:RELATED_TO]->(s10),
(s29)-[:RELATED_TO]->(s43),
(s20)-[:RELATED_TO]->(s51),
(s25)-[:RELATED_TO]->(s37),
(s56)-[:RELATED_TO]->(s55),
(s58)-[:RELATED_TO]->(s57);
