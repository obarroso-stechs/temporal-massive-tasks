"""reports_unique_per_format

Revision ID: a1b2c3d4e5f6
Revises: 7d3f2a91c4be
Create Date: 2026-03-30 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "7d3f2a91c4be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if bind.dialect.name == "postgresql":
        # SQLAlchemy crea unique=True como un índice (no constraint nombrado).
        # Dropeamos tanto el índice como cualquier constraint nombrado sobre task_id.
        existing_indexes = {idx["name"] for idx in inspector.get_indexes("reports")}
        if "ix_reports_task_id" in existing_indexes:
            op.drop_index("ix_reports_task_id", table_name="reports")

        unique_constraints = inspector.get_unique_constraints("reports")
        for constraint in unique_constraints:
            if (constraint.get("column_names") or []) == ["task_id"]:
                op.drop_constraint(constraint["name"], "reports", type_="unique")

    # Crear el nuevo índice no-único sobre task_id (para FK lookups).
    existing_indexes = {idx["name"] for idx in inspector.get_indexes("reports")}
    if "ix_reports_task_id" not in existing_indexes:
        op.create_index("ix_reports_task_id", "reports", ["task_id"])

    # Agregar el unique compuesto (task_id, report_format).
    unique_constraints = inspector.get_unique_constraints("reports")
    has_composite = any(
        (c.get("column_names") or []) == ["task_id", "report_format"]
        for c in unique_constraints
    )
    if not has_composite:
        op.create_unique_constraint("uq_report_task_format", "reports", ["task_id", "report_format"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    unique_constraints = inspector.get_unique_constraints("reports")
    for constraint in unique_constraints:
        if (constraint.get("column_names") or []) == ["task_id", "report_format"]:
            op.drop_constraint(constraint["name"], "reports", type_="unique")

    # Restore the old single-column unique on task_id.
    unique_constraints = inspector.get_unique_constraints("reports")
    has_single_unique = any(
        (constraint.get("column_names") or []) == ["task_id"]
        for constraint in unique_constraints
    )
    if not has_single_unique:
        op.create_unique_constraint("uq_reports_task_id", "reports", ["task_id"])
