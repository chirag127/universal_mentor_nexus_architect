import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict

# Load environment variables
load_dotenv()


class AppConfig(BaseModel):
    # Key from cloud.cerebras.ai
    CEREBRAS_API_KEY: str = os.getenv("CEREBRAS_API_KEY")

    # CEREBRAS BASE URL
    BASE_URL: str = "https://api.cerebras.ai/v1"
    # Size,Model ID,Model Name
    # 8B,llama3.1-8b,Llama 3.1 8B
    # 32B,qwen-3-32b,Qwen 3 32B
    # 70B,llama-3.3-70b,Llama 3.3 70B
    # 120B,gpt-oss-120b,OpenAI GPT OSS
    # 235B,qwen-3-235b-a22b-instruct-2507,Qwen 3 235B Instruct
    # 357B,zai-glm-4.6,Z.ai GLM 4.6
    # --- CEREBRAS MODELS ---
    MODELS: List[str] = [
        "zai-glm-4.6",
        "qwen-3-235b-a22b-instruct-2507",
        "gpt-oss-120b",
        "llama-3.3-70b",
        "qwen-3-32b",
        "llama3.1-8b",
    ]

    CACHE_DIR: str = "data/cache"
    LOG_DIR: str = "logs"

    # Cerebras Context Window
    MAX_TOKENS: int = 4096

    # High concurrency for speed (Cerebras is fast!)
    MAX_WORKERS: int = 20

    # --- 3-Layer Subject Structure (Broad -> Sub -> Topics) ---
    # This structure covers your Wealth, AI Nobel, and Life goals.
    SUBJECT_STRUCTURE: Dict[str, Dict[str, List[str]]] = {
        # --- DOMAIN 1: THE CORE (THINKING & MATH) ---
        "01_CORE_THINKING": {
            "Meta_Learning": [
                "Spaced Repetition Algorithms",
                "Feynman Technique Mastery",
                "Active Recall Systems",
                "Speed Reading Science",
                "Autodidact Frameworks",
            ],
            "Logic_Reasoning": [
                "Propositional Logic",
                "Cognitive Biases (Kahneman)",
                "First Principles Thinking",
                "Socratic Questioning",
                "Game Theory Basics",
            ],
            "Systems_Thinking": [
                "Feedback Loops",
                "Stock and Flow Diagrams",
                "Cybernetics",
                "Antifragility (Taleb)",
                "Complexity Theory",
            ],
            "Research_Methods": [
                "Scientific Method Deep Dive",
                "Double-Blind Studies",
                "Statistical Significance",
                "Causal Inference",
                "Literature Review Strategy",
            ],
        },
        "02_MATHEMATICS_PURE": {
            "Arithmetic_Algebra": [
                "Number Theory Basics",
                "Polynomials",
                "Logarithms",
                "Complex Numbers",
                "Combinatorics",
            ],
            "Calculus": [
                "Limits and Continuity",
                "Derivatives",
                "Integrals",
                "Differential Equations",
                "Multivariable Calculus",
            ],
            "Linear_Algebra": [
                "Vector Spaces",
                "Eigenvalues & Eigenvectors",
                "Matrix Factorization",
                "SVD",
                "Tensors",
            ],
        },
        "03_MATHEMATICS_APPLIED": {
            "Probability": [
                "Bayes Theorem",
                "Distributions",
                "Markov Chains",
                "Monte Carlo Methods",
                "Information Theory",
            ],
            "Statistics": [
                "Hypothesis Testing",
                "Regression Analysis",
                "ANOVA",
                "A/B Testing Math",
                "Time Series Analysis",
            ],
            "Optimization": [
                "Convex Optimization",
                "Gradient Descent",
                "Linear Programming",
                "Lagrange Multipliers",
                "Stochastic Optimization",
            ],
        },
        # --- DOMAIN 2: COMPUTER SCIENCE & AI (THE NOBEL PATH) ---
        "04_CS_FOUNDATIONS": {
            "Architecture": [
                "Von Neumann Architecture",
                "CPU Caching",
                "Bitwise Operations",
                "Memory Management",
                "Assembly Basics",
            ],
            "OS_Networking": [
                "Kernel Design",
                "Process Scheduling",
                "TCP_IP Stack",
                "HTTP_HTTPS Protocols",
                "Distributed Systems",
            ],
            "Algorithms": [
                "Big O Notation",
                "Sorting & Searching",
                "Graph Algorithms (Dijkstra)",
                "Dynamic Programming",
                "Hashing",
            ],
        },
        "05_SOFTWARE_ENGINEERING": {
            "Languages": [
                "Python Advanced Patterns",
                "C++ Memory Model",
                "Rust Ownership",
                "JavaScript Engines",
                "TypeScript Types",
            ],
            "System_Design": [
                "Microservices",
                "Load Balancing",
                "CAP Theorem",
                "Database Sharding",
                "Caching Strategies",
            ],
            "DevOps": [
                "Docker Containers",
                "Kubernetes Orchestration",
                "CI_CD Pipelines",
                "Infrastructure as Code",
                "Observability",
            ],
        },
        "06_DATA_ENGINEERING": {
            "Databases": [
                "SQL Indexing",
                "NoSQL Patterns (MongoDB)",
                "Vector Databases",
                "ACID Transactions",
                "Data Modeling",
            ],
            "Big_Data": [
                "MapReduce",
                "Spark Streaming",
                "Data Warehousing",
                "ETL Pipelines",
                "Data Lakes",
            ],
        },
        "07_AI_MACHINE_LEARNING": {
            "ML_Basics": [
                "Supervised vs Unsupervised",
                "Bias-Variance Tradeoff",
                "Decision Trees",
                "SVMs",
                "Ensemble Methods",
            ],
            "Deep_Learning": [
                "Backpropagation",
                "CNNs",
                "RNNs & LSTMs",
                "Activation Functions",
                "Regularization",
            ],
            "Transformers": [
                "Attention Mechanisms",
                "Transformer Architecture",
                "BERT vs GPT",
                "Tokenization",
                "Positional Encoding",
            ],
        },
        "08_AI_AGENTS_LLMS": {
            "LLM_Ops": [
                "Fine-tuning Strategies",
                "RAG Systems",
                "Prompt Engineering",
                "Context Windows",
                "Quantization",
            ],
            "Agents": [
                "Autonomous Agent Architecture",
                "Tool Use & Function Calling",
                "Multi-Agent Systems",
                "LangChain Framework",
                "Agentic Memory",
            ],
            "Safety_Ethics": [
                "AI Alignment",
                "RLHF",
                "Interpretability",
                "Bias Mitigation",
                "AI Governance",
            ],
        },
        # --- DOMAIN 3: THE WEALTH ENGINE (FAMILY BIZ & RE) ---
        "09_REAL_ESTATE_DEV": {
            "Finance": [
                "Construction Loan Math",
                "ROI Calculation",
                "Cap Rates",
                "Leverage Strategy",
                "Tax Benefits",
            ],
            "Legal_India": [
                "RERA Regulations",
                "GDA Bye-laws",
                "Stamp Duty & Registration",
                "Land Conversion",
                "Property Disputes",
            ],
            "Construction": [
                "Civil Engineering Basics",
                "Cost Estimation",
                "Material Sourcing",
                "Project Management",
                "Green Building",
            ],
        },
        "10_CATTLE_FEED_BIZ": {
            "Nutrition": [
                "Ruminant Digestive Systems",
                "Protein/Energy Balance",
                "Micro-nutrient Formulation",
                "Feed Additives",
                "Toxin Management",
            ],
            "Manufacturing": [
                "Pellet Mill Operations",
                "Grinding & Mixing",
                "Quality Control",
                "Inventory Management",
                "Plant Maintenance",
            ],
            "Supply_Chain": [
                "Commodity Hedging",
                "Logistics Optimization",
                "Vendor Negotiation",
                "Cold Chain",
                "Demand Forecasting",
            ],
        },
        "11_BUSINESS_STRATEGY": {
            "Models": [
                "SaaS Economics",
                "D2C Strategies",
                "Marketplace Dynamics",
                "Network Effects",
                "Platform Business",
            ],
            "Sales": [
                "Sales Funnel Design",
                "Negotiation Tactics",
                "CRM Systems",
                "Objection Handling",
                "Closing Techniques",
            ],
            "Marketing": [
                "Brand Positioning",
                "Performance Marketing",
                "Copywriting Psychology",
                "SEO Strategy",
                "Social Media Growth",
            ],
        },
        "12_FINANCE_WEALTH": {
            "Personal": [
                "Asset Allocation",
                "Tax Optimization (HUF)",
                "Estate Planning",
                "Insurance Hedging",
                "Retirement Planning",
            ],
            "Corporate": [
                "Financial Modeling (DCF)",
                "Balance Sheet Analysis",
                "M&A Basics",
                "Capital Structure",
                "Dividend Policy",
            ],
            "Investing": [
                "Value Investing",
                "Technical Analysis (Limits)",
                "Crypto/Web3",
                "Venture Capital",
                "Angel Investing",
            ],
        },
        # --- DOMAIN 4: THE LIFE ENGINE (HEALTH & SOFT SKILLS) ---
        "13_HEALTH_LONGEVITY": {
            "Physiology": [
                "Metabolic Health",
                "Cardiovascular Systems",
                "Neurochemistry",
                "Hormonal Balance",
                "Immune System",
            ],
            "Nutrition": [
                "Macronutrients",
                "Fasting Protocols",
                "Gut Microbiome",
                "Supplements Science",
                "Hydration Science",
            ],
            "Fitness": [
                "Hypertrophy Mechanics",
                "Zone 2 Cardio",
                "Mobility & Flexibility",
                "Recovery Protocols",
                "Biomechanics",
            ],
        },
        "14_SOFT_POWER": {
            "Psychology": [
                "Evolutionary Psychology",
                "Behavioral Economics",
                "Personality Theory",
                "Social Dynamics",
                "Influence Tactics",
            ],
            "Communication": [
                "Public Speaking",
                "Storytelling Structures",
                "Non-verbal Communication",
                "Persuasion",
                "Active Listening",
            ],
            "Leadership": [
                "Team Dynamics",
                "Conflict Resolution",
                "Decision Making Under Pressure",
                "Mentorship",
                "Vision Setting",
            ],
        },
        "15_CREATIVE_ARTS": {
            "Music": [
                "Music Theory",
                "Guitar Chord Progressions",
                "Rhythm & Timing",
                "Audio Engineering",
                "Songwriting",
            ],
            "Visual": [
                "Composition Rules",
                "Color Theory",
                "Photography Basics",
                "UI/UX Design",
                "Videography",
            ],
            "Writing": [
                "Narrative Structure",
                "Editing Principles",
                "Technical Writing",
                "Scriptwriting",
                "Journalism Basics",
            ],
        },
        "16_PRACTICAL_SKILLS": {
            "Digital_Security": [
                "Encryption Basics",
                "OpSec Protocols",
                "Password Management",
                "Phishing Detection",
                "VPN/Tor",
            ],
            "Legal_Life": [
                "Contract Law Basics",
                "IP Rights",
                "Consumer Protection",
                "Tort Law",
                "Labor Law",
            ],
            "Survival": [
                "First Aid/CPR",
                "Emergency Preparedness",
                "Basic Mechanics",
                "Navigation",
                "Self Defense",
            ],
        },
        # --- EXPANSION SLOTS ---
        "17_HISTORY": {
            "World": ["Ancient Civilizations", "Industrial Revolution"],
            "Economic": ["History of Money", "Great Depressions"],
        },
        "18_PHYSICS": {
            "Classical": ["Newtonian Mechanics", "Thermodynamics"],
            "Modern": ["Quantum Mechanics", "Relativity"],
        },
        "19_CHEMISTRY": {
            "Organic": ["Carbon Compounds", "Reactions"],
            "Inorganic": ["Periodic Table", "Metals"],
        },
        "20_BIOLOGY": {
            "Genetics": ["DNA/RNA", "CRISPR"],
            "Evolution": ["Natural Selection", "Evolutionary Game Theory"],
        },
        "21_POLITICAL_SCIENCE": {
            "Theory": ["Justice", "Power"],
            "Systems": ["Democracy", "Authoritarianism"],
        },
        "22_SOCIOLOGY": {
            "Structures": ["Class Systems", "Institutions"],
            "Change": ["Social Movements", "Demographics"],
        },
        "23_ANTHROPOLOGY": {
            "Cultural": ["Rituals", "Kinship"],
            "Biological": ["Human Origins", "Primatology"],
        },
        "24_LINGUISTICS": {
            "Structure": ["Syntax", "Phonology"],
            "Acquisition": ["Language Learning", "NLP Basics"],
        },
        "25_PHILOSOPHY": {
            "Metaphysics": ["Existence", "Time"],
            "Ethics": ["Utilitarianism", "Deontology"],
        },
        "26_EDUCATION": {
            "Pedagogy": ["Teaching Methods", "Curriculum Design"],
            "EdTech": ["LMS", "Gamification"],
        },
        "27_AGRICULTURE": {
            "Soil_Science": ["Permaculture", "Hydroponics"],
            "Agri_Tech": ["Precision Farming", "IoT in Ag"],
        },
        "28_ENERGY": {
            "Renewable": ["Solar", "Wind"],
            "Nuclear": ["Fission", "Fusion"],
        },
        "29_ENVIRONMENT": {
            "Climate": ["Carbon Cycle", "Geoengineering"],
            "Ecology": ["Biodiversity", "Conservation"],
        },
        "30_SPACE": {
            "Rocketry": ["Propulsion", "Orbital Mechanics"],
            "Astronomy": ["Star Formation", "Exoplanets"],
        },
        "31_ROBOTICS": {
            "Control": ["PID Controllers", "Kinematics"],
            "Perception": ["Computer Vision", "Sensors"],
        },
        "32_BLOCKCHAIN": {
            "Core": ["Consensus Mechanisms", "Cryptography"],
            "DeFi": ["Smart Contracts", "Tokenomics"],
        },
        "33_CYBERSECURITY_ADV": {
            "Offensive": ["Penetration Testing", "Exploit Dev"],
            "Defensive": ["SOC Operations", "Threat Hunting"],
        },
        "34_CLOUD_ARCH": {
            "AWS": ["EC2/S3", "Lambda"],
            "Patterns": ["Serverless", "Event-Driven"],
        },
        "35_MOBILE_DEV": {
            "iOS": ["Swift", "SwiftUI"],
            "Android": ["Kotlin", "Jetpack Compose"],
        },
        "36_GAME_DEV": {
            "Engines": ["Unity", "Unreal"],
            "Design": ["Level Design", "Game Loops"],
        },
        "37_DATA_SCIENCE": {
            "Analysis": ["Pandas/NumPy", "Visualization"],
            "Mining": ["Clustering", "Association Rules"],
        },
        "38_PRODUCT_MGMT": {
            "Strategy": ["Roadmapping", "Prioritization"],
            "Execution": ["Agile/Scrum", "User Stories"],
        },
        "39_UX_RESEARCH": {
            "Methods": ["User Interviews", "Usability Testing"],
            "Analysis": ["Personas", "Journey Maps"],
        },
        "40_SALES_ENGINEERING": {
            "Demo": ["Technical Demos", "PoC Management"],
            "Closing": ["Value Selling", "RFP Response"],
        },
        "41_SUPPLY_CHAIN_ADV": {
            "Logistics": ["Last Mile", "Warehousing"],
            "Strategy": ["Just-in-Time", "Risk Mgmt"],
        },
        "42_ECONOMICS": {
            "Micro": ["Supply/Demand", "Elasticity"],
            "Macro": ["GDP", "Inflation"],
        },
        "43_ACCOUNTING": {
            "Financial": ["GAAP/IFRS", "Auditing"],
            "Managerial": ["Cost Accounting", "Budgeting"],
        },
        "44_LAW_CORP": {
            "Contracts": ["Drafting", "Negotiation"],
            "IP": ["Patents", "Trademarks"],
        },
        "45_MEDICINE_BASIC": {
            "Anatomy": ["Musculoskeletal", "Nervous"],
            "Pathology": ["Disease Mechanisms", "Immunology"],
        },
        "46_PHARMACOLOGY": {
            "Drug_Action": ["Pharmacokinetics", "Pharmacodynamics"],
            "Classes": ["Antibiotics", "Nootropics"],
        },
        "47_NEUROSCIENCE": {
            "Cognitive": ["Memory", "Attention"],
            "Computational": ["Neural Coding", "Brain-Computer Interfaces"],
        },
        "48_NANOTECH": {
            "Materials": ["Graphene", "Carbon Nanotubes"],
            "Applications": ["Medicine", "Electronics"],
        },
        "49_QUANTUM_COMP": {
            "Qubits": ["Superposition", "Entanglement"],
            "Algorithms": ["Shor's", "Grover's"],
        },
        "50_COMPUTATIONAL_BIO": {
            "Genomics": ["Sequencing", "Bioinformatics"],
            "Proteomics": ["Protein Folding", "AlphaFold"],
        },
    }

    def get_full_topic_list(self) -> List[str]:
        full_list = []
        for broad, sub_dict in self.SUBJECT_STRUCTURE.items():
            for sub, topics in sub_dict.items():
                if not topics:
                    for i in range(1, 4):
                        full_list.append(f"{broad}/{sub}: Topic {i}")
                else:
                    for topic in topics:
                        full_list.append(f"{broad}/{sub}: {topic}")
        return full_list


CONFIG = AppConfig()
