from sqlalchemy import text
from sqlalchemy.orm import Session

MATERIALIZED_VIEWS = [
    "mv_diagnostico_reputacion",
    "mv_diagnostico_finanzas",
    "mv_diagnostico_publicaciones",
    "mv_diagnostico_ads",
    "mv_diagnostico_stock",
]

def refresh_materialized_views(db: Session) -> list[str]:
    for view in MATERIALIZED_VIEWS:
        db.execute(text(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view}"))
    db.commit()
    return MATERIALIZED_VIEWS
