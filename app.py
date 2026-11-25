"""A one-page website showing the triaged tickets, most urgent first."""
from flask import Flask, render_template_string

from db import connect

app = Flask(__name__)

PAGE = """<!doctype html>
<title>Ticket triage</title>
<style>
  body { font-family: sans-serif; margin: 2rem; }
  table { border-collapse: collapse; }
  th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; vertical-align: top; }
  .high { background: #fde2e2; }
</style>
<h1>Ticket triage</h1>
<table>
  <tr><th>#</th><th>Subject</th><th>Category</th><th>Urgency</th><th>Guide used</th><th>Suggested reply</th></tr>
  {% for r in rows %}
  <tr class="{{ r['urgency'] }}">
    <td>{{ r['id'] }}</td><td>{{ r['subject'] }}</td><td>{{ r['category'] or '-' }}</td>
    <td>{{ r['urgency'] or '-' }}</td><td>{{ r['guide'] or '-' }}</td><td>{{ r['reply'] or '' }}</td>
  </tr>
  {% endfor %}
</table>"""


@app.route("/")
def index():
    rows = connect().execute(
        """
        SELECT t.id, t.subject, r.category, r.urgency, r.guide, r.reply
        FROM tickets t
        LEFT JOIN results r ON r.ticket_id = t.id
        ORDER BY CASE r.urgency WHEN 'high' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END, t.id
        """
    ).fetchall()
    return render_template_string(PAGE, rows=rows)


if __name__ == "__main__":
    app.run(debug=True)