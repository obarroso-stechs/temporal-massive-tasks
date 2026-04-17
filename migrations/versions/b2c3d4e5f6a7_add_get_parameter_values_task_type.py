"""Add GET_PARAMETER_VALUES task type and expand detail column

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-04-17 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("ALTER TYPE task_type_enum ADD VALUE IF NOT EXISTS 'GET_PARAMETER_VALUES'")

    op.alter_column(
        "task_device_statuses",
        "detail",
        existing_type=sa.String(500),
        type_=sa.String(2000),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "task_device_statuses",
        "detail",
        existing_type=sa.String(2000),
        type_=sa.String(500),
        existing_nullable=True,
    )
