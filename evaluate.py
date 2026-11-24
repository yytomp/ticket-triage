"""Compare the AI's answers with your own labels and print the accuracy."""
from db import connect


def main():
    conn = connect()
    rows = conn.execute(
        """
        SELECT t.id, t.subject, t.true_category, r.category, t.true_urgency, r.urgency
        FROM tickets t
        JOIN results r ON r.ticket_id = t.id
        ORDER BY t.id
        """
    ).fetchall()
    if not rows:
        print("No results yet - run triage.py first.")
        return

    total = len(rows)
    right_category = sum(r["true_category"] == r["category"] for r in rows)
    right_urgency = sum(r["true_urgency"] == r["urgency"] for r in rows)
    print(f"Category correct: {right_category}/{total} ({right_category / total:.0%})")
    print(f"Urgency correct:  {right_urgency}/{total} ({right_urgency / total:.0%})")

    print("\nMisses:")
    for r in rows:
        if r["true_category"] != r["category"] or r["true_urgency"] != r["urgency"]:
            print(f"  #{r['id']} {r['subject']}: expected {r['true_category']}/{r['true_urgency']}, "
                  f"got {r['category']}/{r['urgency']}")


if __name__ == "__main__":
    main()