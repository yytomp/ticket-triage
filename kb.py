"""Find the knowledge-base guide that best matches a ticket."""
import re
from pathlib import Path

STOPWORDS = {
    "the", "and", "for", "can", "you", "your", "with", "this", "that", "have", "not",
    "are", "was", "but", "they", "their", "our", "get", "any", "all", "its", "from",
    "when", "what", "then", "will", "it's", "can't", "please", "need",
    "work", "working", "won", "isn", "don", "could", "look", "help",
}


def words(text):
    """Lower-case words of 3+ letters, without common filler words."""
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2 and w not in STOPWORDS}


def load_guides(folder="kb"):
    """Read every .md file in the folder. Returns {guide name: guide text}."""
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(Path(folder).glob("*.md"))}


def best_guide(ticket_text, guides):
    """Return (name, text) of the guide sharing the most words with the ticket, or (None, "")."""
    ticket_words = words(ticket_text)
    best_name, best_score = None, 0
    for name, text in guides.items():
        score = len(ticket_words & words(text))
        if score > best_score:
            best_name, best_score = name, score
    if best_name is None:
        return None, ""
    return best_name, guides[best_name]