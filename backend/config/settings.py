"""
config/settings.py — Application Configuration
All environment variables and role keyword databases live here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Base directory (two levels up from this file: config/ → backend root) ──
BASE_DIR = Path(__file__).resolve().parent.parent

# ── MongoDB ────────────────────────────────────────────────────────────────
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME   = os.getenv("DB_NAME",   "ResuSenseiDB")

# ── OpenAI (optional — for AI-enhanced recommendations) ───────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ── File uploads ───────────────────────────────────────────────────────────
_upload_env    = os.getenv("UPLOAD_FOLDER")
UPLOAD_FOLDER  = Path(_upload_env) if _upload_env else BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE      = 10 * 1024 * 1024          # 10 MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".rtf"}

# ── API metadata ───────────────────────────────────────────────────────────
API_VERSION     = "2.0"
API_TITLE       = "ResuSensei — AI Resume Analyzer"
API_DESCRIPTION = "ATS-optimised resume analysis with role-specific recommendations"

# ── Rate limiting ──────────────────────────────────────────────────────────
RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_HOUR   = 100

# ── Model storage ──────────────────────────────────────────────────────────
MODEL_PATH = BASE_DIR / "models"
MODEL_PATH.mkdir(parents=True, exist_ok=True)

# ── Logs ───────────────────────────────────────────────────────────────────
LOG_PATH = BASE_DIR / "logs"
LOG_PATH.mkdir(parents=True, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROLE KEYWORDS DATABASE
# Each role has: essential_keywords, preferred_keywords, action_verbs,
#                certifications
# ══════════════════════════════════════════════════════════════════════════════

ROLE_KEYWORDS = {
    "frontend_developer": {
        "name": "Frontend Developer",
        "essential_keywords": [
            "JavaScript", "TypeScript", "React", "Vue", "Angular", "HTML", "CSS",
            "Responsive Design", "UI/UX", "Redux", "Webpack", "npm", "Git",
            "RESTful API", "GraphQL", "Testing", "Jest", "Cypress",
        ],
        "preferred_keywords": [
            "Next.js", "Tailwind CSS", "Material-UI", "Bootstrap", "SCSS", "SASS",
            "Web Performance", "Accessibility", "PWA", "Web Components", "Figma",
            "Adobe XD", "Chrome DevTools", "ES6+", "Babel", "Vite",
        ],
        "action_verbs": [
            "Developed", "Implemented", "Designed", "Optimized", "Built", "Created",
            "Delivered", "Migrated", "Refactored", "Enhanced", "Improved",
        ],
        "certifications": [
            "Meta Front-End Developer", "AWS Certified Developer", "Google UX Design",
        ],
    },
    "backend_developer": {
        "name": "Backend Developer",
        "essential_keywords": [
            "Python", "Java", "Node.js", "C#", "Go", "SQL", "PostgreSQL", "MongoDB",
            "API Development", "RESTful", "Microservices", "Docker", "Kubernetes",
            "Git", "CI/CD", "AWS", "Azure", "Authentication", "Security",
        ],
        "preferred_keywords": [
            "GraphQL", "gRPC", "Redis", "RabbitMQ", "Kafka", "Elasticsearch",
            "Jenkins", "GitLab CI", "Terraform", "Linux", "Nginx", "Load Balancing",
            "Caching", "Message Queues", "Event-Driven", "Serverless", "Lambda",
        ],
        "action_verbs": [
            "Architected", "Developed", "Deployed", "Optimized", "Scaled", "Integrated",
            "Implemented", "Maintained", "Designed", "Automated", "Configured",
        ],
        "certifications": [
            "AWS Certified Solutions Architect", "Google Cloud Professional",
            "Certified Kubernetes Administrator", "Oracle Certified Professional",
        ],
    },
    "data_analyst": {
        "name": "Data Analyst",
        "essential_keywords": [
            "SQL", "Python", "R", "Excel", "Data Visualization", "Tableau", "Power BI",
            "Statistics", "Data Analysis", "Data Mining", "Reporting", "Dashboard",
            "Google Analytics", "ETL", "Data Cleaning", "Business Intelligence",
        ],
        "preferred_keywords": [
            "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter", "Looker",
            "Snowflake", "BigQuery", "dbt", "Airflow", "A/B Testing",
            "Predictive Analytics", "KPI", "Metrics", "Data Modeling",
            "Funnel Analysis", "Cohort Analysis",
        ],
        "action_verbs": [
            "Analyzed", "Identified", "Visualized", "Optimized", "Forecasted",
            "Discovered", "Improved", "Reduced", "Increased", "Measured", "Tracked",
        ],
        "certifications": [
            "Google Data Analytics", "Microsoft Certified Data Analyst",
            "Tableau Desktop Specialist", "AWS Certified Data Analytics",
        ],
    },
    "data_scientist": {
        "name": "Data Scientist",
        "essential_keywords": [
            "Machine Learning", "Python", "R", "TensorFlow", "PyTorch", "scikit-learn",
            "Deep Learning", "NLP", "Computer Vision", "Statistics", "SQL", "Big Data",
            "Feature Engineering", "Model Deployment", "A/B Testing", "Algorithms",
        ],
        "preferred_keywords": [
            "Keras", "XGBoost", "Random Forest", "Neural Networks", "CNN", "RNN",
            "Transformers", "BERT", "GPT", "Apache Spark", "Hadoop", "MLOps",
            "Docker", "Kubernetes", "AWS SageMaker", "Azure ML", "Git", "DVC",
        ],
        "action_verbs": [
            "Developed", "Trained", "Deployed", "Optimized", "Built", "Researched",
            "Implemented", "Achieved", "Improved", "Reduced", "Increased", "Predicted",
        ],
        "certifications": [
            "TensorFlow Developer Certificate", "AWS Certified Machine Learning",
            "Google Professional ML Engineer", "IBM Data Science Professional",
        ],
    },
    "full_stack_developer": {
        "name": "Full Stack Developer",
        "essential_keywords": [
            "JavaScript", "Python", "React", "Node.js", "SQL", "MongoDB", "Git",
            "HTML", "CSS", "RESTful API", "Docker", "AWS", "CI/CD", "Agile",
            "Testing", "TypeScript", "Express", "Authentication",
        ],
        "preferred_keywords": [
            "Next.js", "GraphQL", "Redis", "PostgreSQL", "Kubernetes", "Microservices",
            "Serverless", "Lambda", "S3", "CloudFront", "Nginx", "WebSockets",
            "OAuth", "JWT", "Jenkins", "GitHub Actions", "Terraform",
        ],
        "action_verbs": [
            "Developed", "Built", "Deployed", "Implemented", "Designed", "Optimized",
            "Delivered", "Created", "Maintained", "Integrated", "Automated",
        ],
        "certifications": [
            "AWS Certified Developer", "Meta Full Stack Engineer",
            "Google Cloud Professional Developer",
        ],
    },
    "virtual_assistant": {
        "name": "Virtual Assistant",
        "essential_keywords": [
            "Administrative Support", "Calendar Management", "Email Management",
            "Scheduling", "Customer Service", "Data Entry", "Communication",
            "Microsoft Office", "Google Workspace", "Time Management", "Organization",
        ],
        "preferred_keywords": [
            "CRM", "Salesforce", "HubSpot", "Asana", "Trello", "Slack", "Zoom",
            "Social Media Management", "Content Creation", "Bookkeeping", "QuickBooks",
            "Travel Arrangements", "Event Planning", "Research", "Multitasking",
        ],
        "action_verbs": [
            "Managed", "Coordinated", "Organized", "Scheduled", "Streamlined",
            "Assisted", "Handled", "Maintained", "Supported", "Facilitated", "Processed",
        ],
        "certifications": [
            "Certified Administrative Professional", "Google Workspace Certification",
            "Microsoft Office Specialist", "Virtual Assistant Certification",
        ],
    },
    "product_manager": {
        "name": "Product Manager",
        "essential_keywords": [
            "Product Strategy", "Roadmap", "User Stories", "Agile", "Scrum", "Jira",
            "Stakeholder Management", "Product Lifecycle", "Market Research",
            "Requirements Gathering", "A/B Testing", "Analytics", "KPIs", "Metrics",
        ],
        "preferred_keywords": [
            "Product-Market Fit", "Go-to-Market", "OKRs", "User Research",
            "Wireframing", "Prototyping", "Figma", "SQL", "Data Analysis",
            "Prioritization", "Feature Definition", "Competitive Analysis",
            "User Experience", "MVP",
        ],
        "action_verbs": [
            "Launched", "Delivered", "Defined", "Prioritized", "Led", "Drove",
            "Collaborated", "Analyzed", "Optimized", "Increased", "Improved", "Scaled",
        ],
        "certifications": [
            "Certified Scrum Product Owner", "Product Management Certification",
            "Google Project Management", "Pragmatic Marketing Certified",
        ],
    },
    "devops_engineer": {
        "name": "DevOps Engineer",
        "essential_keywords": [
            "CI/CD", "Docker", "Kubernetes", "Jenkins", "Git", "AWS", "Azure", "GCP",
            "Linux", "Terraform", "Ansible", "Python", "Bash", "Monitoring",
            "Infrastructure as Code", "Automation", "Cloud Computing",
        ],
        "preferred_keywords": [
            "GitLab CI", "GitHub Actions", "ArgoCD", "Helm", "Prometheus", "Grafana",
            "ELK Stack", "Nginx", "Load Balancing", "Microservices", "Serverless",
            "Lambda", "CloudFormation", "Chef", "Puppet", "Redis", "RabbitMQ",
        ],
        "action_verbs": [
            "Automated", "Deployed", "Implemented", "Optimized", "Configured",
            "Managed", "Reduced", "Improved", "Designed", "Built", "Migrated",
        ],
        "certifications": [
            "AWS Certified DevOps Engineer", "Certified Kubernetes Administrator",
            "Google Cloud Professional DevOps", "Azure DevOps Engineer",
        ],
    },
    "ui_ux_designer": {
        "name": "UI/UX Designer",
        "essential_keywords": [
            "UI Design", "UX Design", "Figma", "Adobe XD", "Sketch", "Wireframing",
            "Prototyping", "User Research", "Usability Testing", "Design Systems",
            "User-Centered Design", "Information Architecture", "Interaction Design",
        ],
        "preferred_keywords": [
            "Adobe Creative Suite", "InVision", "Principle", "Framer", "Zeplin",
            "User Flows", "Journey Mapping", "Persona Development", "A/B Testing",
            "Accessibility", "WCAG", "Responsive Design", "Mobile-First", "HTML", "CSS",
        ],
        "action_verbs": [
            "Designed", "Created", "Developed", "Improved", "Collaborated",
            "Conducted", "Redesigned", "Optimized", "Enhanced", "Delivered", "Validated",
        ],
        "certifications": [
            "Google UX Design Certificate", "Nielsen Norman Group UX Certification",
            "Adobe Certified Expert", "Interaction Design Foundation",
        ],
    },
    "cybersecurity_analyst": {
        "name": "Cybersecurity Analyst",
        "essential_keywords": [
            "Security", "Threat Analysis", "Vulnerability Assessment", "Incident Response",
            "SIEM", "Firewall", "IDS/IPS", "Network Security", "Penetration Testing",
            "Risk Assessment", "Compliance", "Encryption", "Authentication",
        ],
        "preferred_keywords": [
            "Splunk", "Wireshark", "Metasploit", "Nessus", "Burp Suite", "OWASP",
            "ISO 27001", "NIST", "SOC", "GDPR", "HIPAA", "PCI DSS", "Forensics",
            "Malware Analysis", "Security Auditing", "Zero Trust", "EDR",
        ],
        "action_verbs": [
            "Identified", "Mitigated", "Investigated", "Implemented", "Monitored",
            "Analyzed", "Secured", "Detected", "Responded", "Prevented", "Assessed",
        ],
        "certifications": [
            "CISSP", "CEH", "CompTIA Security+", "CISM", "OSCP", "GIAC",
        ],
    },
}


# ── ATS Optimization Rules ────────────────────────────────────────────────
ATS_RULES = {
    "format": {
        "standard_fonts":    ["Arial", "Calibri", "Helvetica", "Times New Roman"],
        "avoid":             ["tables", "text_boxes", "images", "headers_footers"],
        "standard_sections": [
            "Professional Summary", "Work Experience", "Education",
            "Skills", "Certifications", "Projects",
        ],
        "file_formats":      [".pdf", ".docx"],
    },
    "content": {
        "min_word_count":        300,
        "max_word_count":        800,
        "use_bullet_points":     True,
        "quantify_achievements": True,
        "use_action_verbs":      True,
        "avoid_personal_pronouns": True,
    },
    "sections": {
        "required":    ["Contact Information", "Work Experience", "Education"],
        "recommended": ["Skills", "Professional Summary", "Certifications"],
        "optional":    ["Projects", "Publications", "Awards", "Volunteer Work"],
    },
}


# ── Scoring Weights (must sum to 1.0) ────────────────────────────────────
SCORING_WEIGHTS = {
    "ats_compatibility":   0.25,
    "content_quality":     0.25,
    "keyword_optimization":0.20,
    "structure":           0.15,
    "achievements":        0.10,
    "formatting":          0.05,
}