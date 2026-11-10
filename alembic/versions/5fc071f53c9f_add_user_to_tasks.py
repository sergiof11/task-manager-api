"""Add user to tasks

Revision ID: 5fc071f53c9f
Revises: 902afd450102
Create Date: 2026-11-10 12:32:34.865459
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "5fc071f53c9f"
down_revision: str | Sequence[str] | None = "902afd450102"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.alter_column(
        "tasks",
        "title",
        existing_type=sa.TEXT(),
        type_=sa.String(length=200),
        existing_nullable=False,
    )

    # Las tareas existentes no tienen propietario.
    # Son datos de desarrollo, por lo que se eliminan antes
    # de hacer user_id obligatorio.
    op.execute("DELETE FROM tasks")

    op.alter_column(
        "tasks",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.create_index(
        "ix_tasks_user_id",
        "tasks",
        ["user_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_tasks_user_id_users",
        "tasks",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_tasks_user_id_users",
        "tasks",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_tasks_user_id",
        table_name="tasks",
    )

    op.alter_column(
        "tasks",
        "title",
        existing_type=sa.String(length=200),
        type_=sa.TEXT(),
        existing_nullable=False,
    )

    op.drop_column(
        "tasks",
        "user_id",
    )
