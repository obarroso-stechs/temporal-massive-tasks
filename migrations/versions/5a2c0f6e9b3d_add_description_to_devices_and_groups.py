"""add_description_to_devices_and_groups

Revision ID: 5a2c0f6e9b3d
Revises: ebbd6e9253c0
Create Date: 2026-03-27 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "5a2c0f6e9b3d"
down_revision: Union[str, None] = "ebbd6e9253c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    device_columns = {column["name"] for column in inspector.get_columns("devices")}
    if "description" not in device_columns:
        op.add_column("devices", sa.Column("description", sa.String(length=255), nullable=True))

    group_columns = {column["name"] for column in inspector.get_columns("device_groups")}
    if "description" not in group_columns:
        op.add_column("device_groups", sa.Column("description", sa.String(length=255), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    group_columns = {column["name"] for column in inspector.get_columns("device_groups")}
    if "description" in group_columns:
        op.drop_column("device_groups", "description")

    device_columns = {column["name"] for column in inspector.get_columns("devices")}
    if "description" in device_columns:
        op.drop_column("devices", "description")
