import os
from backend.auth import hash_password
from backend.models import (
    AdminUser, Award, Certification, ContactSubmission, Education, Experience,
    ImpactMetric, Profile, Project, Research, Skill, Wiki,
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
    # ── Ernst & Young ──────────────────────────────────────────────────
    {
        "name": "Tennex Agents",
        "description": "Enterprise agentic AI platform for procurement intelligence — PO Analysis, Spend Analysis, Template Filling, License Lens, and License Re-harvesting. Led end-to-end delivery with weekly demos to EY Global Innovation Head.",
        "tech_stack": ["LangGraph", "Copilot Studio", "Python", "FastAPI", "Azure OpenAI", "Power Automate"],
        "period": "2024–2026",
        "category": "Agentic AI",
        "company": "Ernst & Young",
        "role": "AI + Solution Architect",
        "highlights": ["Led team of 5 engineers", "Weekly demos to Global Innovation Head", "Multi-agent procurement orchestration"],
        "is_featured": True,
        "order": 1,
    },
    {
        "name": "EY Credentials Engine (EY Discover)",
        "description": "RAG-based semantic search platform replacing keyword search for EY credentials and expertise discovery across 350,000+ professionals.",
        "tech_stack": ["RAG", "Vector DB", "Azure OpenAI", "Python", "FastAPI", "Semantic Kernel"],
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
        "description": "Agentic automation of change impact generation and assessment using Microsoft AutoGen multi-agent framework for organisational change management.",
        "tech_stack": ["AutoGen", "Azure OpenAI", "Python", "FastAPI"],
        "period": "2023–2024",
        "category": "Agentic AI",
        "company": "Ernst & Young",
        "role": "AI Architect",
        "highlights": ["Multi-agent orchestration", "Automated impact assessment", "Reduced manual effort by 70%"],
        "is_featured": True,
        "order": 3,
    },
    {
        "name": "EY Smart Reviewer",
        "description": "AI-powered pharmaceutical regulatory compliance platform — automated drug-to-market promotional material review using an ensemble of 7-8 ML/DL models.",
        "tech_stack": ["Ensemble ML/DL", "NLP", "Python", "TensorFlow", "Scikit-learn", "BERT"],
        "period": "2019–2021",
        "category": "ML/DL",
        "company": "Ernst & Young",
        "role": "Lead AI Architect",
        "highlights": ["60% reduction in review time", "7-8 model ensemble", "Pharma compliance at scale"],
        "is_featured": True,
        "order": 4,
    },
    {
        "name": "Transfer Pricing Benchmarking",
        "description": "ML/NLP-powered benchmarking solution for tax practitioners — automated competitive intelligence for transfer pricing decisions across global jurisdictions.",
        "tech_stack": ["ML", "NLP", "Python", "Scikit-learn", "spaCy"],
        "period": "2019–2020",
        "category": "ML/NLP",
        "company": "Ernst & Young",
        "role": "Lead Data Scientist",
        "highlights": ["45% efficiency improvement", "End-to-end TP automation", "Global jurisdiction coverage"],
        "is_featured": True,
        "order": 5,
    },
    {
        "name": "EYQ Launch — Enterprise ChatGPT",
        "description": "Enterprise-grade GenAI deployment for EY globally — architected onboarding journeys, skill routing, and multi-skill orchestration across 350,000+ users.",
        "tech_stack": ["Azure OpenAI", "LangChain", "Python", "FastAPI", "React"],
        "period": "2023",
        "category": "GenAI Platform",
        "company": "Ernst & Young",
        "role": "AI Architect",
        "highlights": ["350,000+ user scale", "Multi-skill orchestration", "Intelligent routing architecture"],
        "is_featured": True,
        "order": 6,
    },
    {
        "name": "PMO Assist",
        "description": "Agentic project management intelligence platform — integrating LLM capabilities into EY's internal T-Hub PMO suite for intelligent oversight and automated reporting.",
        "tech_stack": ["LangGraph", "Azure OpenAI", "Python", "FastAPI"],
        "period": "2023–2024",
        "category": "Agentic AI",
        "company": "Ernst & Young",
        "role": "AI Architect",
        "highlights": ["Agentic project intelligence", "Automated status reporting", "Risk signal detection"],
        "is_featured": False,
        "order": 7,
    },
    {
        "name": "EY Tie — Investment Audit Intelligence",
        "description": "ML/DL value-based pipeline for investment audit — transforming audit from reactive to predictive intelligence across complex financial portfolios.",
        "tech_stack": ["ML", "DL", "Python", "TensorFlow", "Pandas", "SQL"],
        "period": "2020–2021",
        "category": "ML/DL",
        "company": "Ernst & Young",
        "role": "Lead Data Scientist",
        "highlights": ["Predictive audit intelligence", "Financial anomaly detection", "Risk signal classification"],
        "is_featured": False,
        "order": 8,
    },
    {
        "name": "DTCC — AI Platform Architecture",
        "description": "Served as AI Architect and Product Owner for Depository Trust & Clearing Corporation — full stakeholder management and AI platform delivery for financial market infrastructure.",
        "tech_stack": ["Python", "ML", "FastAPI", "Azure", "PostgreSQL"],
        "period": "2021–2022",
        "category": "AI Platform",
        "company": "Ernst & Young",
        "role": "AI Architect / Product Owner",
        "highlights": ["Full stakeholder ownership", "Financial market infrastructure", "End-to-end platform delivery"],
        "is_featured": False,
        "order": 9,
    },
    {
        "name": "RCO — Risk & Controls Optimisation",
        "description": "ML models for risk and controls optimisation built in partnership with EY's NCoE (neurodiverse Centre of Excellence) — pioneering inclusive AI development practices.",
        "tech_stack": ["ML", "Python", "Scikit-learn", "Azure ML"],
        "period": "2020–2021",
        "category": "ML/DL",
        "company": "Ernst & Young",
        "role": "Lead Data Scientist",
        "highlights": ["NCoE collaboration model", "Risk signal classification", "Inclusive AI development"],
        "is_featured": False,
        "order": 10,
    },
    {
        "name": "Spectrum AI",
        "description": "Accessibility-first mobile AI app for visually impaired users — navigation assist, object recognition, voice interaction, and environmental awareness using agentic pipelines.",
        "tech_stack": ["Computer Vision", "Python", "Mobile AI", "Voice AI", "Azure Cognitive Services"],
        "period": "2022–2023",
        "category": "Accessibility AI",
        "company": "Ernst & Young",
        "role": "AI Consultant",
        "highlights": ["Agentic accessibility", "Real-time navigation assistance", "Voice-first interaction design"],
        "is_featured": False,
        "order": 11,
    },
    {
        "name": "Global Payroll Operate Intelligence",
        "description": "LLM-powered intelligence layer over EY's global payroll operations — natural language querying, anomaly detection, and automated compliance checks across 50+ countries.",
        "tech_stack": ["Azure OpenAI", "RAG", "Python", "FastAPI", "LangChain"],
        "period": "2022–2023",
        "category": "RAG",
        "company": "Ernst & Young",
        "role": "AI Architect",
        "highlights": ["50+ country coverage", "NL querying over payroll data", "Automated compliance checks"],
        "is_featured": False,
        "order": 12,
    },
    # ── British Telecom ──────────────────────────────────────────────
    {
        "name": "BT Anomaly Detection & NLP Intelligence",
        "description": "NLP-powered anomaly detection system for mission-critical telecom infrastructure — one-class SVM for fault detection, sentiment analysis for CRM, and change request classification.",
        "tech_stack": ["NLP", "Python", "SVM", "Scikit-learn", "Siebel CRM"],
        "period": "2017–2018",
        "category": "ML/NLP",
        "company": "British Telecom",
        "role": "Senior Consultant — Data Intelligence",
        "highlights": ["One-class SVM anomaly detection", "Zero-downtime CMS migration", "Automated fault classification"],
        "is_featured": False,
        "order": 13,
    },
    {
        "name": "BT Platform Intelligence & CMS Migration",
        "description": "End-to-end intelligent platform support for BT's mission-critical telecom and cloud infrastructure — automated order & fault management with zero-downtime migrations.",
        "tech_stack": ["Python", "NLP", "Siebel", "SQL", "Shell Scripting"],
        "period": "2017–2018",
        "category": "Data Engineering",
        "company": "British Telecom",
        "role": "Senior Consultant — Platform",
        "highlights": ["Zero-downtime transitions", "Order automation", "Infrastructure intelligence"],
        "is_featured": False,
        "order": 14,
    },
    # ── Tesco Technology ─────────────────────────────────────────────
    {
        "name": "Tesco Image Processing Pipeline",
        "description": "Python image processing pipeline for retail automation — cost-effective alternative to enterprise MediaBin solutions for product image management at Tesco scale.",
        "tech_stack": ["Python", "OpenCV", "PIL", "SQL", "REST APIs"],
        "period": "2016–2017",
        "category": "Computer Vision",
        "company": "Tesco Technology",
        "role": "Principal Software Engineer",
        "highlights": ["Enterprise MediaBin replacement", "Retail automation at scale", "Significant cost reduction"],
        "is_featured": False,
        "order": 15,
    },
    {
        "name": "Tesco ClubCard Analytics & A/B Testing",
        "description": "Retail data analytics for ClubCard loyalty programme — A/B testing via Adobe Analytics, e-commerce conversion optimisation, and online order journey analytics.",
        "tech_stack": ["Python", "SQL", "Adobe Analytics", "Pandas", "A/B Testing"],
        "period": "2016–2017",
        "category": "Data Engineering",
        "company": "Tesco Technology",
        "role": "Data Analyst",
        "highlights": ["Measurable e-commerce conversion lift", "ClubCard loyalty analytics", "Multi-vertical data pipelines"],
        "is_featured": False,
        "order": 16,
    },
    # ── Wipro / Cognizant / Mahindra Satyam ─────────────────────────
    {
        "name": "JH Investments — Best Mutual Funds Website",
        "description": "Award-winning web platform for JH Investments — recognised as Best Mutual Funds Website by Web Marketing Association 2013-14. Full-stack delivery from architecture to deployment.",
        "tech_stack": ["JavaScript", "HTML/CSS", "CMS", "SQL", "REST APIs"],
        "period": "2013–2014",
        "category": "Web Engineering",
        "company": "Cognizant",
        "role": "Senior Developer",
        "highlights": ["Web Marketing Association Award 2013-14", "Best Mutual Funds Website", "Full-stack delivery"],
        "is_featured": False,
        "order": 17,
    },
    {
        "name": "AirAsia Destination Guide",
        "description": "Tourism portal for AirAsia contributing to significant revenue increase — full-stack CMS delivery for destination discovery across Southeast Asian travel markets.",
        "tech_stack": ["CMS", "JavaScript", "HTML/CSS", "SQL"],
        "period": "2011–2012",
        "category": "Web Engineering",
        "company": "Mahindra Satyam",
        "role": "Software Engineer",
        "highlights": ["Revenue-generating tourism portal", "Southeast Asia travel market", "CMS architecture and delivery"],
        "is_featured": False,
        "order": 18,
    },
    # ── Material Plus ────────────────────────────────────────────────
    {
        "name": "M+ Data & AI Practice Framework",
        "description": "Building Material Plus's Data & AI Global Practice from ground up — methodology, capability framework, delivery standards, GTM strategy, and team architecture for enterprise AI engagements.",
        "tech_stack": ["AI Architecture", "Practice Leadership", "GTM Strategy", "Enterprise AI"],
        "period": "2026–Present",
        "category": "AI Platform",
        "company": "Material Plus",
        "role": "Senior Technical Architect",
        "highlights": ["Practice built from ground up", "GTM for BFSI + Retail verticals", "Global delivery standards"],
        "is_featured": True,
        "order": 19,
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
    {"metric": "16+", "label": "Years Experience", "description": "Spanning web engineering, data science, and AI architecture across 6 organisations", "order": 1, "is_dynamic_yoe": True},
    {"metric": "30+", "label": "Enterprise AI Solutions", "description": "Delivered across Banking, Finance, Insurance, Healthcare, and Retail domains", "order": 2},
    {"metric": "60%", "label": "Process Acceleration", "description": "Reduction in pharma compliance review time via EY Smart Reviewer", "order": 3},
    {"metric": "45%", "label": "Efficiency Gain", "description": "Tax practitioner productivity via Transfer Pricing Benchmarking solution", "order": 4},
    {"metric": "40%", "label": "Accuracy Improvement", "description": "Response accuracy gain via Intelligent Routing Architecture for multi-agent systems", "order": 5},
    {"metric": "18+", "label": "Engineers Mentored", "description": "ML engineers and data scientists developed into technical leaders", "order": 6},
]

SEED_WIKI = """# Praveen T N — Professional Wiki (SIGMA Knowledge Base)

## Identity
**Full Name**: Praveen T N
**Current Role**: Senior Technical Architect — Data & AI Global Practice
**Company**: Material Plus (M+), joined March 2026
**Location**: Bengaluru, India
**LinkedIn**: linkedin.com/in/tnpraveen | **Credly**: credly.com/users/praveentn

## Career in Brief
16+ years spanning web engineering → data science → AI architecture → practice leadership across 6 organisations.

| Period | Company | Role |
|---|---|---|
| Mar 2026–Present | Material Plus (M+) | Sr Technical Architect, Data & AI Global Practice |
| Oct 2021–Mar 2026 | Ernst & Young | Assistant Director — AI & Data Architect |
| Oct 2018–Oct 2021 | Ernst & Young | Supervising Associate — Lead Data Scientist |
| Feb 2017–Sep 2018 | British Telecom | Senior Consultant — Data Intelligence |
| Jan 2016–Feb 2017 | Tesco Technology | Principal Software Engineer |
| 2010–2015 | Wipro / Cognizant / Mahindra Satyam | Software Engineer → Senior Developer |

## Key Projects & Impact
- **Tennex Agents** (EY, 2024–26): Agentic AI procurement platform — LangGraph + Copilot Studio. Weekly demos to EY Global Innovation Head.
- **EY Credentials Engine**: RAG semantic search for 350,000+ professionals. Led team of 6. Replaced keyword search with vector retrieval.
- **EY Smart Reviewer**: 7-8 ensemble ML/DL for pharma compliance. 60% reduction in drug-to-market review time.
- **Transfer Pricing Benchmarking**: ML/NLP — 45% efficiency gain for tax practitioners.
- **Change Impact Experience Agents**: AutoGen multi-agent framework for change management.
- **EYQ Launch**: Enterprise ChatGPT deployment at 350,000+ user scale.
- **DTCC**: AI Architect / Product Owner for financial market infrastructure.
- **Spectrum AI**: Accessibility AI for visually impaired users.
- **Tesco Image Pipeline**: Python image processing — cost-effective MediaBin replacement.
- **JH Investments**: Web Marketing Association Award — Best Mutual Funds Website 2013-14.
- **M+ AI Practice**: Building the Data & AI practice from ground up — methodology, GTM, team.

## Technical Expertise
- **Agentic AI**: LangGraph, AutoGen, MCP, multi-agent systems, tool use, orchestration
- **RAG & Search**: Vector databases, semantic search, retrieval augmentation, re-ranking
- **LLM Engineering**: Azure OpenAI, Gemini, fine-tuning, prompt engineering, evaluation
- **ML/DL**: TensorFlow, PyTorch, Scikit-learn, ensemble methods, NLP, computer vision
- **Cloud & MLOps**: Azure (Architect Expert certified), CI/CD, Docker, microservices
- **Quantum Computing**: IBM Qiskit Developer certified, BB84 QKD research, Shor's algorithm
- **Languages**: Python (expert), SQL (expert), JavaScript, Node.js
- **Leadership**: Practice P&L, team of 18+ engineers, client advisory, go-to-market

## Education
- MS Business Analytics — Hult International Business School, Boston (2024)
- Diploma in Quantum Computing — Universidad Politécnica de Madrid (2023)
- MA Clinical Psychology — IGNOU (2015)
- B.Tech Electrical & Electronics Engineering — TKM College of Engineering (2009)

## Certifications
- EY Platinum Badge: Data Architecture (2025), Data Science (2024), Artificial Intelligence (2022)
- Microsoft Certified: Azure Solutions Architect Expert (2024)
- Microsoft Certified: Azure Data Scientist Associate (2022)
- IBM Quantum Excellence (2020–2025), IBM Qiskit Certified Developer (2021)

## What Makes Praveen Unique
1. **Hands-on depth** — Architects production AI systems, not just PowerPoints
2. **Multidisciplinary** — Engineering + Psychology + Business Analytics + Quantum Computing
3. **Scale** — Has delivered at 350,000+ user enterprise scale
4. **Range** — Can architect an LLM system AND present to C-suite AND mentor engineers
5. **Research foundation** — Published work in quantum cryptography and computer vision

## Research & Publications
- "Effect of Multiple Eavesdroppers on BB84 QKD Protocol Security" (Thesis — Quantum Cryptography)
- "Neural Network-based Polygon Mid-surface Identification" (Publication — Computer Vision)
- "From Qubit to Shor's Algorithm" (Article — Quantum Computing)
- "Genetic Algorithm-based Optimisation for Induction Motor Starting Torque" (Publication)

## Awards
- BI Stratus Award 2023 — Ernst & Young (AI innovation)
- GDG Star Performer Awards — Multiple (EY)
- Best Mutual Funds Website — Web Marketing Association 2013-14

## Personality & Working Style
- Direct communicator, low tolerance for ambiguity
- Design thinking practitioner — human-centred approach to AI systems
- Believes AI should amplify human capability, not replace judgment
- The psychology background informs his approach to change management and user adoption
- Known for translating complex AI concepts into business value narratives
"""


def run_seed(db):
    """Seed the database. Safe to re-run — uses upsert logic for most tables."""

    # Admin user
    if not db.query(AdminUser).first():
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        db.add(AdminUser(username="admin", password_hash=hash_password(admin_password)))
        print("[seed] Created admin user.")

    # First-time full seed
    if not db.query(Profile).first():
        db.add(Profile(**SEED_PROFILE))
        for item in SEED_EXPERIENCE:
            db.add(Experience(**item))
        for item in SEED_EDUCATION:
            db.add(Education(**item))
        for item in SEED_SKILLS:
            db.add(Skill(**item))
        for item in SEED_CERTIFICATIONS:
            db.add(Certification(**item))
        for item in SEED_RESEARCH:
            db.add(Research(**item))
        for item in SEED_AWARDS:
            db.add(Award(**item))
        for item in SEED_IMPACT_METRICS:
            db.add(ImpactMetric(**{k: v for k, v in item.items() if k != "is_dynamic_yoe"}))
        db.commit()
        print("[seed] Database seeded with Praveen T N's profile data.")

    # Incremental project sync — add any missing projects by name
    existing_names = {p.name for p in db.query(Project.name).all()}
    new_count = 0
    for item in SEED_PROJECTS:
        if item["name"] not in existing_names:
            db.add(Project(**item))
            new_count += 1
    if new_count:
        db.commit()
        print(f"[seed] Added {new_count} new project(s).")

    # Wiki — create if missing (admin can edit after)
    if not db.query(Wiki).first():
        db.add(Wiki(content=SEED_WIKI))
        db.commit()
        print("[seed] Wiki seeded.")
