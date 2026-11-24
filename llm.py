"""Talking to the AI model: build the prompt, send it, read the answer."""
import json
import os

CATEGORIES = ["account_access", "printing", "network", "hardware", "software", "onboarding", "other"]
URGENCIES = ["low", "medium", "high"]

PROMPT = """You are helping an IT service desk triage tickets.

Ticket subject: {subject}
Ticket body: {body}

Relevant guide (may be empty):
{guide}

Answer with JSON only, no other text, in exactly this shape:
{{"category": "<one of {categories}>", "urgency": "<one of {urgencies}>", "reply": "<a short, friendly reply to the user, using the guide if it helps>"}}

Urgency is high when several people or customers are affected, or someone cannot work at all."""


def build_prompt(subject, body, guide):
    return PROMPT.format(
        subject=subject,
        body=body,
        guide=guide or "(none)",
        categories=", ".join(CATEGORIES),
        urgencies=", ".join(URGENCIES),
    )


def parse_response(text):
    """Turn the model's text into a dict. Falls back to other/medium if anything is wrong."""
    fallback = {"category": "other", "urgency": "medium", "reply": ""}
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        return fallback
    try:
        data = json.loads(text[start:end + 1])
    except ValueError:
        return fallback
    if not isinstance(data, dict):
        return fallback
    return {
        "category": data.get("category") if data.get("category") in CATEGORIES else "other",
        "urgency": data.get("urgency") if data.get("urgency") in URGENCIES else "medium",
        "reply": str(data.get("reply", "")),
    }


def ask_model(prompt):
    """Send the prompt to the AI model and return its text answer."""
    if os.getenv("LLM_PROVIDER") == "anthropic":  # optional paid alternative
        import anthropic

        client = anthropic.Anthropic()
        message = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-5-5"),
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    from google import genai  # free tier; reads GEMINI_API_KEY from the environment

    client = genai.Client()
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        contents=prompt,
    )
    return response.text or ""