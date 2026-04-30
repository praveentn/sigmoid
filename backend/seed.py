import os
from backend.auth import hash_password
from backend.models import (
    AdminUser, Award, Certification, Education, Experience,
    ImpactMetric, Profile, Project, Research, Skill,
)

SEED_PROFILE = {
    "name": "Praveen T N",
    "title": "Senior Technical Architect — Data & AI Global Practice",
    "company": "Material Plus",
    "tagline": "Architect of AI transformation. Builder of intelligent systems that don't just process data — they redefine how enterprises think, decide, and innovate.",
    "bio": (
        "16+ years at the intersection of AI architecture, enterprise systems, and human-centred design. "
        "Currently leading the Data & AI Global Practice at Material Plus (M+) — building the capability, "
        "culture, and client portfolio that positions M+ as a destination for enterprise AI transformation.\n\n"
        "Brings a rare combination: the depth of a hands-on AI architect who has designed and delivered 30+ "
        "enterprise-grade solutions, and the breadth of a practice leader who understands go-to-market strategy, "
        "team building, and the art of translating complex AI capability into business value.\n\n"
        "Spent 7+ years at Ernst & Young building EY's agentic AI and RAG platform from the ground up — "
        "rising from Lead Data Scientist to Assistant Director — architecting autonomous multi-agent systems, "
        "leading teams of 18+, and serving as SME for AI architecture programmes globally.\n\n"
        "Unique differentiator: The rare professional who can simultaneously architect a production LLM system, "
        "present to a C-suite, mentor a junior data scientist, and publish research on quantum cryptography."
    ),
    "email": "sigmoidptn@gmail.com",
    "phone": "+91 740 60 53 777",
    "location": "Bengaluru, India",
    "linkedin_url": "https://linkedin.com/in/tnpraveen",
    "credly_url": "https://credly.com/users/praveentn",
    "visa_info": "US B1/B2 Visa: Valid till 2029",
    "years_experience": 16,
    "solutions_delivered": 30,
}

SEED_EXPERIENCE = [
    {
        "company": "Material Plus (M+)",
        "role": "Senior Technical Architect — Data & AI Global Practice",
        "period_start": "Mar 2026",
        "period_end": "Present",
        "location": "Bengaluru, India",
        "tagline": "Leading Material India's Data & AI Global Practice — building capability, winning engagements, and defining the AI architecture standard for M+ globally.",
        "highlights": [
            "Architecting the Data & AI practice from ground up — defining methodology, capability framework, and delivery standards for enterprise AI engagements",
            "Driving GTM strategy for AI & Data services across Banking, Financial Services, Insurance, and Retail verticals",
            "Leading client advisory engagements for AI-first transformation programmes — bridging AI strategy with delivery roadmaps",
            "Building a high-performance Data & AI team — hiring, developing, and mentoring architects, data scientists, and engineers",
            "Establishing thought leadership presence through white papers, client workshops, and industry participation",
        ],
        "order": 1,
        "is_current": True,
    },
    {
        "company": "Ernst & Young",
        "role": "Assistant Director — AI & Data Architect",
        "period_start": "Oct 2021",
        "period_end": "Mar 2026",
        "location": "Thiruvananthapuram / Bengaluru, India",
        "tagline": "Led the vanguard of enterprise AI transformation — architecting autonomous intelligent systems that redefined how global organisations operate, decide, and innovate.",
        "highlights": [
            "Led Tennex Agents — agentic AI platform for enterprise procurement (PO Analysis, Spend Analysis, License Lens) using LangGraph and Copilot Studio; weekly demos to EY Global Innovation Head",
            "Architected 10+ specialised LLM-powered Agentic-RAG platforms: Credentials Engine, Global Payroll Operate, Talent Skill, Policy Navigation, NextWave, Capital Edge, Deal & Delivery",
            "Invented intelligent query routing architecture — 40% improvement in response accuracy across multi-agent orchestration",
            "Built and led team of 18+ ML engineers and data scientists; created culture of innovation and technical leadership",
            "EYQ Launch (Enterprise ChatGPT) — onboarding journeys, skill routing, multi-skill orchestration at scale",
            "Change Impact Experience Agents (AutoGen); PMO Assist — agentic project management intelligence",
            "SME for AI Architecture, Data Strategy, and Analytics badge programmes — shaping EY's global AI training standards",
            "~30% consulting: advisory across business units, client proposals, LLM strategy, AI governance (AIRA, AI QRM)",
        ],
        "order": 2,
        "is_current": False,
    },
    {
        "company": "Ernst & Young",
        "role": "Supervising Associate — Lead Data Scientist",
        "period_start": "Oct 2018",
        "period_end": "Oct 2021",
        "location": "Thiruvananthapuram, India",
        "tagline": "Pioneered AI-driven regulatory compliance and financial intelligence — transforming manual processes into intelligent automated systems.",
        "highlights": [
            "EY Smart Reviewer: AI-powered pharma regulatory compliance platform (7-8 ensemble ML/DL models) — 60% reduction in drug-to-market review time",
            "EY Tie: ML/DL value-based pipeline for investment audit — transforming from reactive to predictive intelligence",
            "Transfer Pricing Benchmarking: ML/NLP solution — 45% improvement in tax practitioner efficiency",
            "DTCC: AI Architect / Product Owner — full stakeholder management and technical delivery ownership",
            "RCO: ML models for risk & controls optimisation with EY NCoE (neurodiverse colleagues)",
            "Human-in-the-Loop Factory — sustainability and contract extraction use cases",
        ],
        "order": 3,
        "is_current": False,
    },
    {
        "company": "British Telecom",
        "role": "Senior Consultant — Data Intelligence, Platform",
        "period_start": "Feb 2017",
        "period_end": "Sep 2018",
        "location": "Bengaluru, India",
        "tagline": "Enterprise platform intelligence and AI-powered customer analytics for mission-critical telecom infrastructure.",
        "highlights": [
            "Led CMS migration and platform support for mission-critical telecom and cloud infrastructure — zero-downtime transitions",
            "Implemented NLP anomaly detection (one-class SVM), sentiment analysis, and change request classification",
            "Automated workflows for order & fault management, reducing manual intervention in Siebel CRM",
        ],
        "order": 4,
        "is_current": False,
    },
    {
        "company": "Tesco Technology",
        "role": "Principal Software Engineer — Data Analyst",
        "period_start": "Jan 2016",
        "period_end": "Feb 2017",
        "location": "Bengaluru, India",
        "tagline": "Retail data innovation — building analytics pipelines and digital platforms for one of the world's largest retailers.",
        "highlights": [
            "Built Python image processing pipelines for retail automation — cost-effective alternative to enterprise MediaBin solutions",
            "Led A/B testing via Adobe Analytics — measurable e-commerce conversion improvements",
            "Managed retail data pipelines, ClubCard analytics, and online order journey processing",
            "CMS migration across multiple Tesco business verticals",
        ],
        "order": 5,
        "is_current": False,
    },
    {
        "company": "Wipro | Cognizant | Mahindra Satyam",
        "role": "Software Engineer → Senior Developer",
        "period_start": "Mar 2010",
        "period_end": "Dec 2015",
        "location": "India",
        "tagline": "Built the technical foundation across enterprise web, CMS, and client-facing digital solutions in banking, healthcare, and financial services.",
        "highlights": [
            "Wipro — U.S. Bank: Received accolades for Student Loans and Credit Card web application development",
            "Cognizant — JH Investments: Designed website that won Best Mutual Funds Website Award (Web Marketing Association 2013-14)",
            "Mahindra Satyam — BOC-Linde, GE Healthcare, AirAsia: Full-stack CMS delivery across industrial, healthcare, and travel sectors",
            "AirAsia Destination Guide: Tourism portal contributing to significant revenue increase",
            "Completed ELTP Software Engineering Trainee programme at Mahindra Satyam",
        ],
        "order": 6,
        "is_current": False,
    },
]

SEED_EDUCATION = [
    {
        "institution": "Hult International Business School, Boston",
        "degree": "Master of Science in Business Analytics",
        "year": "2024",
        "description": "Graduate programme in data science, analytics strategy, and business intelligence.",
        "order": 1,
    },
    {
        "institution": "Universidad Politécnica de Madrid, Spain",
        "degree": "Diploma in Quantum Computing Technology",
        "year": "2023",
        "description": "Advanced programme in quantum algorithms, quantum cryptography, and quantum computing applications.",
        "order": 2,
    },
    {
        "institution": "IGNOU, India",
        "degree": "Master of Arts in Clinical Psychology",
        "year": "2015",
        "description": "Graduate programme in clinical psychology — informs human-centred AI design and behavioural analytics.",
        "order": 3,
    },
    {
        "institution": "TKM College of Engineering, Kollam",
        "degree": "B.Tech in Electrical & Electronics Engineering",
        "year": "2009",
        "description": "Final year project: Genetic Algorithm-based optimisation of starting torque in Induction Motors using MATLAB/Simulink.",
        "order": 4,
    },
]

SEED_SKILLS = [
    {
        "category": "AI Architecture & Strategy",
        "items": [
            "Agentic AI Systems", "LLM Orchestration", "RAG Frameworks",
            "Enterprise AI Architecture", "AI Governance", "Generative AI",
            "Multi-Agent Systems", "Model Context Protocol",
        ],
        "order": 1,
    },
    {
        "category": "Frameworks & Tools",
        "items": [
            "LangGraph", "AutoGen", "LangChain", "FastAPI", "React",
            "TensorFlow", "PyTorch", "Scikit-learn", "Copilot Studio", "Semantic Kernel",
        ],
        "order": 2,
    },
    {
        "category": "Cloud & MLOps",
        "items": [
            "Microsoft Azure", "Azure OpenAI", "Azure AI Services", "Azure ML",
            "MLOps", "CI/CD", "Docker", "Vector Databases", "Microservices",
        ],
        "order": 3,
    },
    {
        "category": "Programming & Data",
        "items": [
            "Python", "SQL", "JavaScript", "Node.js",
            "PostgreSQL", "MongoDB", "Data Engineering", "Data Architecture", "Pandas",
        ],
        "order": 4,
    },
    {
        "category": "Emerging & Specialised",
        "items": [
            "Quantum Computing", "Quantum Cryptography", "IBM Qiskit",
            "Computer Vision", "NLP", "Synthetic Data Generation",
            "LLM Evaluation", "Fine-tuning SLMs",
        ],
        "order": 5,
    },
    {
        "category": "Leadership & Consulting",
        "items": [
            "Practice Leadership", "P&L Ownership", "Team Building",
            "Client Management", "Technical Strategy", "Go-to-Market",
            "Thought Leadership", "AI Consulting",
        ],
        "order": 6,
    },
]

SEED_CERTIFICATIONS = [
    {"name": "EY Platinum Badge — Data Architecture", "issuer": "Ernst & Young", "year": "2025", "is_featured": True, "order": 1},
    {"name": "Microsoft Certified: Azure Solutions Architect Expert", "issuer": "Microsoft", "year": "2024", "is_featured": True, "order": 2},
    {"name": "EY Platinum Badge — Data Science", "issuer": "Ernst & Young", "year": "2024", "is_featured": True, "order": 3},
    {"name": "IBM Quantum Excellence — Quantum Challenge & QGSS", "issuer": "IBM", "year": "2020–2025", "is_featured": True, "order": 4},
    {"name": "EY Platinum Badge — Artificial Intelligence", "issuer": "Ernst & Young", "year": "2022", "is_featured": True, "order": 5},
    {"name": "Microsoft Certified: Azure Data Scientist Associate", "issuer": "Microsoft", "year": "2022", "is_featured": False, "order": 6},
    {"name": "IBM Qiskit Certified Quantum Developer", "issuer": "IBM", "year": "2021", "is_featured": False, "order": 7},
]

SEED_PROJECTS = [
    {
        "name": "Tennex Agents",
        "description": "Enterprise agentic AI platform for procurement intelligence — PO Analysis, Spend Analysis, Template Filling, License Lens, and License Re-harvesting. Led end-to-end delivery with weekly demos to EY Global Innovation Head.",
        "tech_stack": ["LangGraph", "Copilot Studio", "Python", "FastAPI", "React", "Azure", "Power Automate"],
        "period": "2024–2026",
        "category": "Agentic AI",
        "company": "Ernst & Young",
        "role": "AI + Solution Architect",
        "highlights": ["Led team of 5 10x engineers", "Weekly demos to Global Innovation Head", "End-to-end technical delivery"],
        "is_featured": True,
        "order": 1,
    },
    {
        "name": "EY Credentials Engine (EY Discover)",
        "description": "RAG-based semantic search platform replacing keyword search for EY credentials and expertise discovery. Served as both AI Architect and Data Architect.",
        "tech_stack": ["RAG", "Vector DB", "Azure OpenAI", "Python", "FastAPI"],
        "period": "2023–2024",
        "category": "RAG",
        "company": "Ernst & Young",
        "role": "AI Architect + Data Architect",
        "highlights": ["Led team of 6", "Replaced keyword search with semantic retrieval", "Contributed to EY Data Strategy"],
        "is_featured": True,
        "order": 2,
    },
    {
        "name": "Change Impact Experience Agents",
        "description": "Agentic automation of change impact generation and assessment using Microsoft AutoGen multi-agent framework.",
        "tech_stack": ["AutoGen", "Azure OpenAI", "Python", "FastAPI"],
        "period": "2023–2024",
        "category": "Agentic AI",
        "company": "Ernst & Young",
        "role": "AI Architect",
        "highlights": ["Multi-agent orchestration", "Automated impact assessment", "AutoGen framework"],
        "is_featured": True,
        "order": 3,
    },
    {
        "name": "EY Smart Reviewer",
        "description": "AI-powered pharmaceutical regulatory compliance platform — automated drug-to-market promotional material review using an ensemble of 7-8 ML/DL models.",
        "tech_stack": ["Ensemble ML/DL", "NLP", "Python", "TensorFlow", "Scikit-learn"],
        "period": "2019–2021",
        "category": "ML/DL",
        "company": "Ernst & Young",
        "role": "AI Architect",
        "highlights": ["60% reduction in review time", "7-8 model ensemble", "End-to-end delivery ownership"],
        "is_featured": True,
        "order": 4,
    },
    {
        "name": "Transfer Pricing Benchmarking",
        "description": "ML/NLP-powered benchmarking solution for tax practitioners — automated competitive intelligence for transfer pricing decisions.",
        "tech_stack": ["ML", "NLP", "Python", "Scikit-learn"],
        "period": "2019–2020",
        "category": "ML/NLP",
        "company": "Ernst & Young",
        "role": "Lead Data Scientist",
        "highlights": ["45% efficiency improvement", "End-to-end TP automation", "Tax practitioner productivity"],
        "is_featured": True,
        "order": 5,
    },
    {
        "name": "PMO Assist (T-Hub)",
        "description": "Integrated agentic capabilities into EY's internal project management suite for intelligent project oversight and decision support.",
        "tech_stack": ["LangGraph", "Azure OpenAI", "Python", "FastAPI"],
        "period": "2023–2024",
        "category": "Agentic AI",
        "company": "Ernst & Young",
        "role": "AI Architect",
        "highlights": ["Project management intelligence", "Agentic decision support"],
        "is_featured": False,
        "order": 6,
    },
    {
        "name": "EYQ Launch — Enterprise ChatGPT",
        "description": "Enterprise-grade ChatGPT deployment for EY — solved onboarding journeys, skill routing, and multi-skill orchestration at scale.",
        "tech_stack": ["Azure OpenAI", "Python", "FastAPI", "React"],
        "period": "2023",
        "category": "GenAI Platform",
        "company": "Ernst & Young",
        "role": "AI Architect",
        "highlights": ["Enterprise-scale deployment", "Multi-skill orchestration", "Intelligent routing"],
        "is_featured": False,
        "order": 7,
    },
    {
        "name": "Spectrum AI",
        "description": "Mobile app for visually impaired users with agentic capabilities — navigation assist, voice interaction, and environmental awareness.",
        "tech_stack": ["Computer Vision", "Python", "Mobile AI", "Voice AI"],
        "period": "2022–2023",
        "category": "Accessibility AI",
        "company": "Ernst & Young",
        "role": "AI Consultant",
        "highlights": ["Agentic accessibility", "Navigation assistance", "Voice interaction"],
        "is_featured": False,
        "order": 8,
    },
]

SEED_RESEARCH = [
    {
        "title": "Effect of Multiple Eavesdroppers on BB84 QKD Protocol Security",
        "description": "Graduate thesis exploring quantum cryptography vulnerabilities and security implications in practical quantum key distribution systems. Analysed multi-eavesdropper scenarios and their impact on BB84 protocol integrity.",
        "type": "thesis",
        "focus_area": "Quantum Cryptography",
        "order": 1,
    },
    {
        "title": "Neural Network-based Polygon Mid-surface Identification",
        "description": "Novel encoder-decoder architecture research for computational geometry applications in CAD/CAM systems — mid-surface extraction from complex 3D geometries.",
        "type": "publication",
        "focus_area": "Computer Vision & Deep Learning",
        "order": 2,
    },
    {
        "title": "From Qubit to Shor's Algorithm",
        "description": "Comprehensive technical article demystifying quantum computing fundamentals for enterprise audiences — from basic qubit mechanics to Shor's algorithm implications for cryptography.",
        "type": "article",
        "focus_area": "Quantum Computing",
        "order": 3,
    },
    {
        "title": "Genetic Algorithm-based Optimisation for Induction Motor Starting Torque",
        "description": "MATLAB/Simulink implementation demonstrating evolutionary computation for optimising SCR firing angles to maximise starting torque in induction motors.",
        "type": "publication",
        "focus_area": "Optimisation Algorithms",
        "order": 4,
    },
]

SEED_AWARDS = [
    {
        "title": "BI Stratus Award 2023",
        "description": "Outstanding contribution to AI innovation at Ernst & Young — recognising exceptional impact in enterprise AI architecture and delivery.",
        "year": "2023",
        "organization": "Ernst & Young",
        "order": 1,
    },
    {
        "title": "GDG Star Performer Awards",
        "description": "Multiple recognitions for technical excellence and outstanding contribution to delivery engagement performance.",
        "year": "Multiple",
        "organization": "EY GDG",
        "order": 2,
    },
    {
        "title": "Best Mutual Funds Website",
        "description": "Web Marketing Association Award for the JH Investments website — recognised as best mutual funds website for 2013-14.",
        "year": "2013–14",
        "organization": "Web Marketing Association",
        "order": 3,
    },
]

SEED_IMPACT_METRICS = [
    {"metric": "16+", "label": "Years Experience", "description": "Spanning web engineering, data science, and AI architecture across 6 organisations", "order": 1},
    {"metric": "30+", "label": "Enterprise AI Solutions", "description": "Delivered across Banking, Finance, Insurance, Healthcare, and Retail domains", "order": 2},
    {"metric": "60%", "label": "Process Acceleration", "description": "Reduction in pharma compliance review time via EY Smart Reviewer", "order": 3},
    {"metric": "45%", "label": "Efficiency Gain", "description": "Tax practitioner productivity via Transfer Pricing Benchmarking solution", "order": 4},
    {"metric": "40%", "label": "Accuracy Improvement", "description": "Response accuracy gain via Intelligent Routing Architecture for multi-agent systems", "order": 5},
    {"metric": "18+", "label": "Engineers Mentored", "description": "ML engineers and data scientists developed into technical leaders", "order": 6},
]


def run_seed(db):
    """Seed the database with Praveen's data if it's empty."""

    # Admin user
    if not db.query(AdminUser).first():
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        db.add(AdminUser(username="admin", password_hash=hash_password(admin_password)))
        print(f"[seed] Created admin user (password from ADMIN_PASSWORD env var)")

    if db.query(Profile).first():
        print("[seed] Data already seeded, skipping.")
        return

    # Profile
    db.add(Profile(**SEED_PROFILE))

    # Experience
    for item in SEED_EXPERIENCE:
        db.add(Experience(**item))

    # Education
    for item in SEED_EDUCATION:
        db.add(Education(**item))

    # Skills
    for item in SEED_SKILLS:
        db.add(Skill(**item))

    # Certifications
    for item in SEED_CERTIFICATIONS:
        db.add(Certification(**item))

    # Projects
    for item in SEED_PROJECTS:
        db.add(Project(**item))

    # Research
    for item in SEED_RESEARCH:
        db.add(Research(**item))

    # Awards
    for item in SEED_AWARDS:
        db.add(Award(**item))

    # Impact Metrics
    for item in SEED_IMPACT_METRICS:
        db.add(ImpactMetric(**item))

    db.commit()
    print("[seed] Database seeded with Praveen T N's profile data.")
