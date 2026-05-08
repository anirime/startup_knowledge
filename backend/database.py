import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).parent / "startups.db"


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS startups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                industry TEXT,
                founded_year INTEGER,
                location TEXT,
                investment_stage TEXT,
                total_funding REAL,
                vcs TEXT,
                ceo TEXT,
                employee_count INTEGER,
                key_members TEXT,
                description TEXT,
                website TEXT,
                tags TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_company_name ON startups(company_name);
            CREATE INDEX IF NOT EXISTS idx_industry ON startups(industry);
            CREATE INDEX IF NOT EXISTS idx_stage ON startups(investment_stage);
            CREATE INDEX IF NOT EXISTS idx_location ON startups(location);
            """
        )


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
