"""Main script: load tickets, match a guide, ask the AI, save results."""
import time

from dotenv import load_dotenv

from db import connect, load_tickets
from kb import best_guide, load_guides
from llm import ask_model, build_prompt, parse_response


def main():
    load_dotenv()  # also reads a .env file, if you have one
    conn = connect()
    print(f"Loaded {load_tickets(conn, 'data/tickets.csv')} tickets")
    guides = load_guides()

    for t in conn.execute("SELECT * FROM tickets ORDER BY id").fetchall():
        guide_name, guide_text = best_guide(t["subject"] + " " + t["body"], guides)
        answer = ask_model(build_prompt(t["subject"], t["body"], guide_text))
        result = parse_response(answer)
        conn.execute(
            "INSERT OR REPLACE INTO results (ticket_id, category, urgency, guide, reply) VALUES (?, ?, ?, ?, ?)",
            (t["id"], result["category"], result["urgency"], guide_name, result["reply"]),
        )
        conn.commit()
        print(f"#{t['id']:>3}  {result['category']:<15} {result['urgency']:<7} guide: {guide_name or '-'}")
        time.sleep(6)  # stay under the free tier's requests-per-minute limit


if __name__ == "__main__":
    main()