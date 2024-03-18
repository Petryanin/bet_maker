"""Create bet table.

Revision ID: 610124ea82c4
Revises:
Create Date: 2024-03-16 20:59:24.203902
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "610124ea82c4"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade the database to a later version."""
    op.create_table(
        "bet",
        sa.Column("bet_id", sa.INTEGER(), nullable=False),
        sa.Column("event_id", sa.INTEGER(), nullable=False),
        sa.Column("amount", sa.NUMERIC(), nullable=False),
        sa.Column("state", sa.SMALLINT(), nullable=False),
        sa.PrimaryKeyConstraint("bet_id", name=op.f("bet_pkey")),
    )


def downgrade() -> None:
    """Downgrade the database to a previous version."""
    op.drop_table("bet")
