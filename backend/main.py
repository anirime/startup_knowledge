from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from database import get_conn, init_db


class StartupIn(BaseModel):
    company_name: str = Field(..., min_length=1)
    industry: Optional[str] = None
    founded_year: Optional[int] = None
    location: Optional[str] = None
    investment_stage: Optional[str] = None
    total_funding: Optional[float] = None
    vcs: list[str] = Field(default_factory=list)
    ceo: Optional[str] = None
    employee_count: Optional[int] = None
    key_members: list[str] = Field(default_factory=list)
    description: Optional[str] = None
    website: Optional[str] = None
    tags: list[str] = Field(default_factory=list)


class Startup(StartupIn):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


def row_to_startup(row) -> dict:
    return {
        "id": row["id"],
        "company_name": row["company_name"],
        "industry": row["industry"],
        "founded_year": row["founded_year"],
        "location": row["location"],
        "investment_stage": row["investment_stage"],
        "total_funding": row["total_funding"],
        "vcs": json.loads(row["vcs"] or "[]"),
        "ceo": row["ceo"],
        "employee_count": row["employee_count"],
        "key_members": json.loads(row["key_members"] or "[]"),
        "description": row["description"],
        "website": row["website"],
        "tags": json.loads(row["tags"] or "[]"),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


init_db()

app = FastAPI(title="Startup Knowledge Base")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/startups", response_model=list[Startup])
def list_startups(
    q: Optional[str] = None,
    name: Optional[str] = None,
    industry: Optional[str] = None,
    stage: Optional[str] = None,
    location: Optional[str] = None,
    tag: Optional[str] = None,
):
    sql = "SELECT * FROM startups WHERE 1=1"
    params: list = []

    if name:
        sql += " AND company_name LIKE ?"
        params.append(f"%{name}%")
    if industry:
        sql += " AND industry = ?"
        params.append(industry)
    if stage:
        sql += " AND investment_stage = ?"
        params.append(stage)
    if location:
        sql += " AND location LIKE ?"
        params.append(f"%{location}%")
    if tag:
        sql += " AND tags LIKE ?"
        params.append(f'%"{tag}"%')
    if q:
        sql += (
            " AND (company_name LIKE ? OR description LIKE ? OR industry LIKE ?"
            " OR location LIKE ? OR ceo LIKE ? OR vcs LIKE ? OR key_members LIKE ?"
            " OR tags LIKE ?)"
        )
        like = f"%{q}%"
        params.extend([like] * 8)

    sql += " ORDER BY updated_at DESC, id DESC"

    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [row_to_startup(r) for r in rows]


@app.get("/api/startups/{startup_id}", response_model=Startup)
def get_startup(startup_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM startups WHERE id = ?", (startup_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Startup not found")
    return row_to_startup(row)


@app.post("/api/startups", response_model=Startup, status_code=201)
def create_startup(payload: StartupIn):
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO startups (
                company_name, industry, founded_year, location,
                investment_stage, total_funding, vcs,
                ceo, employee_count, key_members,
                description, website, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.company_name,
                payload.industry,
                payload.founded_year,
                payload.location,
                payload.investment_stage,
                payload.total_funding,
                json.dumps(payload.vcs, ensure_ascii=False),
                payload.ceo,
                payload.employee_count,
                json.dumps(payload.key_members, ensure_ascii=False),
                payload.description,
                payload.website,
                json.dumps(payload.tags, ensure_ascii=False),
            ),
        )
        new_id = cur.lastrowid
        row = conn.execute("SELECT * FROM startups WHERE id = ?", (new_id,)).fetchone()
    return row_to_startup(row)


@app.put("/api/startups/{startup_id}", response_model=Startup)
def update_startup(startup_id: int, payload: StartupIn):
    with get_conn() as conn:
        existing = conn.execute("SELECT id FROM startups WHERE id = ?", (startup_id,)).fetchone()
        if not existing:
            raise HTTPException(404, "Startup not found")
        conn.execute(
            """
            UPDATE startups SET
                company_name = ?, industry = ?, founded_year = ?, location = ?,
                investment_stage = ?, total_funding = ?, vcs = ?,
                ceo = ?, employee_count = ?, key_members = ?,
                description = ?, website = ?, tags = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                payload.company_name,
                payload.industry,
                payload.founded_year,
                payload.location,
                payload.investment_stage,
                payload.total_funding,
                json.dumps(payload.vcs, ensure_ascii=False),
                payload.ceo,
                payload.employee_count,
                json.dumps(payload.key_members, ensure_ascii=False),
                payload.description,
                payload.website,
                json.dumps(payload.tags, ensure_ascii=False),
                startup_id,
            ),
        )
        row = conn.execute("SELECT * FROM startups WHERE id = ?", (startup_id,)).fetchone()
    return row_to_startup(row)


@app.delete("/api/startups/{startup_id}", status_code=204)
def delete_startup(startup_id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM startups WHERE id = ?", (startup_id,))
        if cur.rowcount == 0:
            raise HTTPException(404, "Startup not found")


@app.get("/api/facets")
def facets():
    with get_conn() as conn:
        industries = [r[0] for r in conn.execute(
            "SELECT DISTINCT industry FROM startups WHERE industry IS NOT NULL AND industry != '' ORDER BY industry"
        ).fetchall()]
        stages = [r[0] for r in conn.execute(
            "SELECT DISTINCT investment_stage FROM startups WHERE investment_stage IS NOT NULL AND investment_stage != '' ORDER BY investment_stage"
        ).fetchall()]
        locations = [r[0] for r in conn.execute(
            "SELECT DISTINCT location FROM startups WHERE location IS NOT NULL AND location != '' ORDER BY location"
        ).fetchall()]
        tag_rows = conn.execute(
            "SELECT tags FROM startups WHERE tags IS NOT NULL AND tags != '[]'"
        ).fetchall()
    tag_set: set[str] = set()
    for r in tag_rows:
        try:
            for t in json.loads(r[0]):
                if t:
                    tag_set.add(t)
        except json.JSONDecodeError:
            continue
    return {
        "industries": industries,
        "stages": stages,
        "locations": locations,
        "tags": sorted(tag_set),
    }


_FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
if _FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=_FRONTEND_DIST, html=True), name="frontend")
