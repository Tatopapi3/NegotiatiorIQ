import anthropic
from core.config import ANTHROPIC_API_KEY, CLAUDE_MODEL

_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are a senior tech recruiter with 6 years of experience placing software engineers \
and AI practitioners at high-growth NYC startups including Series A through Series D companies. \
You have negotiated hundreds of offers and know exactly what companies will and won't budge on.

Your job is to give the candidate real, specific, actionable negotiation advice — not generic tips. \
When you give numbers, give exact dollar amounts. When you give scripts, write them word for word \
as if the candidate is going to copy and paste them into an email right now.

Be direct. Be confident. Be specific. The candidate is counting on you to give them the real intel."""


def get_negotiation_coaching(
    offer: dict,
    similar_jds: list[dict],
    similar_profiles: list[dict],
) -> dict:
    """
    Call Claude with the offer + RAG context and return structured coaching.
    Returns: { market_rate, counter_range, negotiation_script, key_points }
    """

    jd_context = "\n\n".join([
        f"JD #{i+1} — {jd['title']} at {jd['company']} ({jd['location']})\n"
        f"Salary range: ${jd.get('salary_min', 'N/A'):,} – ${jd.get('salary_max', 'N/A'):,}\n"
        f"{jd['content'][:600]}"
        for i, jd in enumerate(similar_jds)
    ]) or "No similar job descriptions found."

    profile_context = "\n\n".join([
        f"Profile #{i+1} — {p['title']} | {p['years_exp']} yrs exp | Skills: {', '.join(p.get('skills', []))}\n"
        f"{p['content'][:400]}"
        for i, p in enumerate(similar_profiles)
    ]) or "No similar candidate profiles found."

    user_message = f"""
## Candidate's Current Offer
- Role: {offer['role']}
- Company: {offer['company']}
- Location: {offer['location']}
- Offered Salary: ${offer['salary']:,}
- Years of Experience: {offer['years_exp']}
- Additional context: {offer.get('notes', 'None provided')}

## Similar Job Descriptions (Market Comps)
{jd_context}

## Similar Candidate Profiles (Comparable Candidates)
{profile_context}

---

Based on this market data, provide:

1. **Market Rate Assessment** — Is this offer below, at, or above market? Give specific numbers.

2. **Counter-Offer Range** — Exact dollar range they should counter with (low / target / stretch). \
Also mention any non-salary items worth negotiating (equity, signing bonus, PTO, remote flexibility).

3. **Negotiation Script** — Write the exact email or talking points the candidate should use \
word for word. Make it confident but professional. Include a subject line if it's an email.

4. **Key Leverage Points** — 3 bullet points of specific reasons this candidate has leverage.

Format your response clearly with these four sections using markdown headers.
"""

    message = _client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = message.content[0].text

    # Parse sections from Claude's markdown response
    sections = {"market_rate": "", "counter_range": "", "negotiation_script": "", "key_points": ""}
    current = None
    buffer: list[str] = []

    for line in raw.splitlines():
        lower = line.lower()
        if "market rate" in lower and line.startswith("#"):
            if current: sections[current] = "\n".join(buffer).strip()
            current, buffer = "market_rate", []
        elif "counter" in lower and line.startswith("#"):
            if current: sections[current] = "\n".join(buffer).strip()
            current, buffer = "counter_range", []
        elif "negotiation script" in lower and line.startswith("#"):
            if current: sections[current] = "\n".join(buffer).strip()
            current, buffer = "negotiation_script", []
        elif "key leverage" in lower and line.startswith("#"):
            if current: sections[current] = "\n".join(buffer).strip()
            current, buffer = "key_points", []
        elif current:
            buffer.append(line)

    if current and buffer:
        sections[current] = "\n".join(buffer).strip()

    sections["raw"] = raw
    return sections


FREE_SYSTEM_PROMPT = """You are an elite negotiation coach with expertise across salary, freelance rates, \
rent, vendor contracts, business deals, and any other negotiation scenario. \
Your specialty is AI and tech salary negotiation, but you handle everything.

You give word-for-word scripts, not vague advice. You understand leverage, anchoring, and BATNA. \
Be specific, be direct, and give the candidate exactly what they need to say."""


def get_free_negotiation_coaching(situation: str) -> dict:
    user_message = f"""Here is the negotiation situation:

{situation}

Provide:

1. **Strategy** — What's the optimal negotiation approach here? Name the tactic (e.g., anchoring, \
competing offer leverage, silence, etc.) and explain briefly why it fits this situation.

2. **Word-for-Word Script** — Write exactly what the person should say or email. Make it complete \
and ready to use. If it's an email, include a subject line.

3. **Key Tactics** — 3–4 bullet points of the most important moves to make (and what to avoid).

Format with markdown headers for each section."""

    message = _client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1200,
        system=FREE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = message.content[0].text

    sections: dict = {"strategy": "", "script": "", "tactics": ""}
    current = None
    buffer: list[str] = []

    for line in raw.splitlines():
        lower = line.lower()
        if "strategy" in lower and line.startswith("#"):
            if current: sections[current] = "\n".join(buffer).strip()
            current, buffer = "strategy", []
        elif ("word-for-word" in lower or "script" in lower) and line.startswith("#"):
            if current: sections[current] = "\n".join(buffer).strip()
            current, buffer = "script", []
        elif ("key tactic" in lower or "tactic" in lower) and line.startswith("#"):
            if current: sections[current] = "\n".join(buffer).strip()
            current, buffer = "tactics", []
        elif current:
            buffer.append(line)

    if current and buffer:
        sections[current] = "\n".join(buffer).strip()

    # Fallback: if parsing missed sections, dump everything into strategy
    if not any(sections.values()):
        sections["strategy"] = raw

    return sections
