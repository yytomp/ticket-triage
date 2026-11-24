"""Everything to do with the SQLite database."""
import csv
import sqlite3
from pathlib import Path

DB_PATH = Path("triage.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    true_category TEXT,
    true_urgency TEXT
);
CREATE TABLE IF NOT EXISTS results (
    ticket_id INTEGER PRIMARY KEY REFERENCES tickets(id),
    category TEXT,
    urgency TEXT,
    guide TEXT,
    reply TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(path=DB_PATH):
    """Open the database (creating the tables if they don't exist yet)."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  # lets us read columns by name: row["subject"]
    conn.executescript(SCHEMA)
    return conn


def load_tickets(conn, csv_path):
    """Copy every row of the CSV into the tickets table. Returns how many rows."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = [
            (int(r["id"]), r["subject"], r["body"], r["true_category"], r["true_urgency"])
            for r in csv.DictReader(f)
        ]
    conn.executemany("INSERT OR REPLACE INTO tickets VALUES (?, ?, ?, ?, ?)", rows)
    conn.commit()
    return len(rows)