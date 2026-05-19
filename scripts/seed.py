"""
Seed NegotiateIQ with realistic NYC tech job descriptions and candidate profiles.
Run: python -m scripts.seed
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.embeddings import embed
from core.database import insert_job_description, insert_candidate_profile

JOB_DESCRIPTIONS = [
    {
        "title": "Senior Software Engineer",
        "company": "Ramp",
        "location": "New York, NY",
        "salary_min": 185000,
        "salary_max": 220000,
        "content": (
            "Ramp is hiring a Senior Software Engineer to join our platform team. "
            "You'll build the infrastructure that powers our finance automation product used by 15,000+ companies. "
            "We're looking for 5+ years of backend experience, strong Python or Go skills, and experience with distributed systems. "
            "We offer $185k–$220k base + equity + unlimited PTO + 100% remote-friendly. "
            "Skills: Python, PostgreSQL, Kafka, AWS, distributed systems, REST APIs."
        ),
    },
    {
        "title": "AI/ML Engineer",
        "company": "Perplexity AI",
        "location": "New York, NY (Hybrid)",
        "salary_min": 200000,
        "salary_max": 260000,
        "content": (
            "Perplexity is looking for an AI/ML Engineer to improve our answer engine. "
            "You'll work on fine-tuning LLMs, building evaluation pipelines, and shipping features that reach millions of users. "
            "Requirements: 3+ years ML experience, strong Python, experience with LLMs or transformers, PyTorch. "
            "Compensation: $200k–$260k + significant equity + $10k/yr learning budget."
        ),
    },
    {
        "title": "Full Stack Engineer",
        "company": "Brex",
        "location": "New York, NY",
        "salary_min": 160000,
        "salary_max": 195000,
        "content": (
            "Brex is hiring a Full Stack Engineer for our spend management platform. "
            "You'll own features end to end — from database schema to polished UI. "
            "We use React, TypeScript, Elixir, and PostgreSQL. 3–6 years experience preferred. "
            "Base: $160k–$195k + equity + $3k home office stipend + 4% 401k match."
        ),
    },
    {
        "title": "Staff Software Engineer",
        "company": "Figma",
        "location": "New York, NY",
        "salary_min": 230000,
        "salary_max": 300000,
        "content": (
            "Figma is hiring a Staff Engineer to lead our real-time collaboration infrastructure. "
            "8+ years of experience required. You'll architect systems that serve 4M+ daily active users. "
            "Tech: C++, Rust, TypeScript, WebAssembly. We value deep technical expertise and cross-team influence. "
            "Comp: $230k–$300k base + RSUs + comprehensive benefits."
        ),
    },
    {
        "title": "Backend Engineer",
        "company": "Persona",
        "location": "New York, NY",
        "salary_min": 150000,
        "salary_max": 185000,
        "content": (
            "Persona is building the identity layer for the internet. "
            "We need a Backend Engineer with 2–5 years experience to build our verification APIs. "
            "Python, Django, PostgreSQL, Redis, AWS. Fast-paced Series C startup environment. "
            "Salary: $150k–$185k + early-stage equity with strong upside."
        ),
    },
    {
        "title": "Senior AI Engineer",
        "company": "Harvey AI",
        "location": "New York, NY",
        "salary_min": 210000,
        "salary_max": 270000,
        "content": (
            "Harvey is building AI for legal professionals and is looking for a Senior AI Engineer. "
            "You'll work directly with LLMs, build RAG pipelines, and ship features for Fortune 500 law firms. "
            "4+ years experience, strong Python, experience with LangChain, vector databases, and production AI systems. "
            "Comp: $210k–$270k + competitive equity + fully remote option."
        ),
    },
    {
        "title": "Software Engineer II",
        "company": "Spotify",
        "location": "New York, NY",
        "salary_min": 155000,
        "salary_max": 190000,
        "content": (
            "Spotify NYC is hiring an Engineer II for our Creator Tools team. "
            "You'll build tools used by 10M+ podcasters and musicians. Java, Python, Kubernetes, GCP. "
            "2–4 years experience. Strong systems thinking, good at cross-functional work. "
            "Base: $155k–$190k + RSU refreshers + 6% 401k match + premium benefits."
        ),
    },
    {
        "title": "Data Engineer",
        "company": "Navan",
        "location": "New York, NY",
        "salary_min": 145000,
        "salary_max": 175000,
        "content": (
            "Navan (formerly TripActions) needs a Data Engineer to build our analytics platform. "
            "3+ years of data engineering experience. dbt, Snowflake, Airflow, Python, SQL. "
            "You'll work with the CTO to shape our data strategy as we scale to IPO. "
            "Salary: $145k–$175k + equity + unlimited PTO + $2k annual learning budget."
        ),
    },
]

CANDIDATE_PROFILES = [
    {
        "name": None,
        "title": "Senior Software Engineer",
        "years_exp": 5,
        "skills": ["Python", "FastAPI", "PostgreSQL", "AWS", "Docker", "React"],
        "content": (
            "5 years of backend engineering experience at Series B and Series C startups in NYC. "
            "Led migration of monolith to microservices serving 500k DAU. "
            "Open source contributor. Previously at two YC-backed companies. "
            "Negotiated from $165k to $195k at last role by highlighting system design impact."
        ),
    },
    {
        "name": None,
        "title": "AI/ML Engineer",
        "years_exp": 3,
        "skills": ["Python", "PyTorch", "LLMs", "RAG", "LangChain", "Hugging Face"],
        "content": (
            "3 years specializing in production ML systems. Built fine-tuned LLM pipeline "
            "that reduced customer support costs by 40%. MS in Computer Science from NYU. "
            "Previous offer: $175k. Successfully countered to $210k + $30k signing bonus "
            "by demonstrating unique LLM expertise during tight hiring market."
        ),
    },
    {
        "name": None,
        "title": "Full Stack Engineer",
        "years_exp": 4,
        "skills": ["React", "TypeScript", "Node.js", "PostgreSQL", "GraphQL"],
        "content": (
            "4 years full stack experience. Built consumer-facing features at a fintech startup (Series D). "
            "Strong TypeScript skills. Previously negotiated a $20k increase by getting competing offer "
            "from Stripe. Works well in cross-functional environments."
        ),
    },
    {
        "name": None,
        "title": "Staff Engineer",
        "years_exp": 8,
        "skills": ["Java", "Distributed Systems", "Kubernetes", "Go", "Architecture"],
        "content": (
            "8 years in engineering with last 3 as tech lead. Architected systems at scale (50M+ events/day). "
            "Managed team of 6. Strong systems design. Got offer from Google as leverage to negotiate "
            "from $220k to $275k + extra RSU grant."
        ),
    },
    {
        "name": None,
        "title": "Backend Engineer",
        "years_exp": 2,
        "skills": ["Python", "Django", "PostgreSQL", "Redis", "REST APIs"],
        "content": (
            "2 years backend experience post bootcamp + 1 yr self-taught. "
            "Built internal tools saving 15 hrs/week at previous company. "
            "Negotiated $20k above initial offer by emphasizing rapid ramp-up and shipping velocity."
        ),
    },
]


def main():
    print("Seeding job descriptions...")
    for jd in JOB_DESCRIPTIONS:
        vec = embed(f"{jd['title']} {jd['company']} {jd['location']} {jd['content']}")
        r = insert_job_description(**jd, embedding=vec)
        print(f"  ✓ {jd['title']} @ {jd['company']} → {r['id']}")

    print("\nSeeding candidate profiles...")
    for p in CANDIDATE_PROFILES:
        skills_str = ", ".join(p["skills"])
        vec = embed(f"{p['title']} {p['years_exp']} years {skills_str} {p['content']}")
        r = insert_candidate_profile(**p, embedding=vec)
        print(f"  ✓ {p['title']} ({p['years_exp']} yrs) → {r['id']}")

    print("\n✅ Seed complete.")


if __name__ == "__main__":
    main()
