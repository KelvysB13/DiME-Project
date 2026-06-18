"""add soft_delete to reference tables

Revision ID: 001
Revises:
Create Date: 2026-06-16 00:00:00.000000
"""

from typing import Sequence
from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("pais", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("moneda", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("plan_saas", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("token_blacklist", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("token_blacklist", "deleted_at")
    op.drop_column("plan_saas", "deleted_at")
    op.drop_column("moneda", "deleted_at")
    op.drop_column("pais", "deleted_at")
