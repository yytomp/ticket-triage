from db import connect, load_tickets


def test_load_tickets_into_database(tmp_path):
    csv_file = tmp_path / "tickets.csv"
    csv_file.write_text(
        'id,subject,body,true_category,true_urgency\n1,Locked out,"Too many attempts, help",account_access,high\n',
        encoding="utf-8",
    )
    conn = connect(tmp_path / "test.db")
    assert load_tickets(conn, csv_file) == 1
    row = conn.execute("SELECT * FROM tickets").fetchone()
    assert row["subject"] == "Locked out"
    assert row["body"] == "Too many attempts, help"