"""initial_schema

Revision ID: ebbd6e9253c0
Revises:
Create Date: 2026-03-24 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "ebbd6e9253c0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Enums ─────────────────────────────────────────────────────────────────
    task_type_enum = sa.Enum(
        "FIRMWARE_UPDATE", "PARAMETER_UPDATE",
        name="task_type_enum",
    )
    device_task_status_enum = sa.Enum(
        "SCHEDULED", "PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELED", "TIMED_OUT",
        name="device_task_status_enum",
    )
    report_format_enum = sa.Enum(
        "PDF", "WORD", "EXCEL", "CSV",
        name="report_format_enum",
    )

    # ── devices ───────────────────────────────────────────────────────────────
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("serial_number", sa.String(100), nullable=False),
        sa.Column("description", sa.String(255), nullable=True),
        sa.Column("manufacturer", sa.String(100), nullable=True),
        sa.Column("model", sa.String(100), nullable=True),
        sa.Column("software_version", sa.String(100), nullable=True),
        sa.Column("firmware_version", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_devices_serial_number", "devices", ["serial_number"], unique=True)

    # ── device_groups ─────────────────────────────────────────────────────────
    op.create_table(
        "device_groups",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("description", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("name", name="uq_device_groups_name"),
    )

    # ── device_group_memberships ──────────────────────────────────────────────
    op.create_table(
        "device_group_memberships",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("group_id", sa.Integer(), sa.ForeignKey("device_groups.id", ondelete="CASCADE"), nullable=False),
        sa.Column("device_id", sa.Integer(), sa.ForeignKey("devices.id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("group_id", "device_id", name="uq_group_device"),
    )

    # ── tasks ─────────────────────────────────────────────────────────────────
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("workflow_id", sa.String(200), nullable=False),
        sa.Column("task_type", task_type_enum, nullable=False),
        sa.Column("task_name", sa.String(300), nullable=False),
        sa.Column("group_id", sa.Integer(), sa.ForeignKey("device_groups.id", ondelete="SET NULL"), nullable=True),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_tasks_workflow_id", "tasks", ["workflow_id"], unique=True)

    # ── task_device_statuses ──────────────────────────────────────────────────
    op.create_table(
        "task_device_statuses",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("serial_number", sa.String(100), nullable=False),
        sa.Column("device_id", sa.Integer(), sa.ForeignKey("devices.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", device_task_status_enum, nullable=False),
        sa.Column("detail", sa.String(500), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("task_id", "serial_number", name="uq_task_serial"),
    )
    op.create_index("ix_task_device_statuses_task_id", "task_device_statuses", ["task_id"])

    # ── reports ───────────────────────────────────────────────────────────────
    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("generate_report", sa.Boolean(), nullable=False, default=False),
        sa.Column("report_format", report_format_enum, nullable=True),
        sa.Column("report_path", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("task_id", name="uq_reports_task_id"),
    )
    op.create_index("ix_reports_task_id", "reports", ["task_id"])


def downgrade() -> None:
    op.drop_table("reports")
    op.drop_table("task_device_statuses")
    op.drop_table("tasks")
    op.drop_table("device_group_memberships")
    op.drop_table("device_groups")
    op.drop_table("devices")

    op.execute("DROP TYPE IF EXISTS report_format_enum")
    op.execute("DROP TYPE IF EXISTS device_task_status_enum")
    op.execute("DROP TYPE IF EXISTS task_type_enum")
