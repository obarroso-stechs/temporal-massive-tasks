"""add_parameter_set_task_type

Revision ID: 7d3f2a91c4be
Revises: 5a2c0f6e9b3d
Create Date: 2026-03-29 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "7d3f2a91c4be"
down_revision: Union[str, None] = "5a2c0f6e9b3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("ALTER TYPE task_type_enum ADD VALUE IF NOT EXISTS 'PARAMETER_SET'")


def downgrade() -> None:
    # PostgreSQL enums do not support dropping values safely in-place.
    pass
