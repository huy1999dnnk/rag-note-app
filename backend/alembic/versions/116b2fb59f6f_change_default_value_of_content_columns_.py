"""Change default value of content columns in notes table

Revision ID: 116b2fb59f6f
Revises: 2cbb25420513
Create Date: 2025-04-22 04:08:45.344651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '116b2fb59f6f'
down_revision: Union[str, None] = '2cbb25420513'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Set default value of content column to [{}]
    op.alter_column(
        'notes',
        'content',
        server_default=sa.text("('[{}]'::jsonb)"),
        existing_type=sa.JSON()
    )

def downgrade() -> None:
    """Downgrade schema."""
    # Remove default value (or set to previous default, e.g., NULL)
    op.alter_column(
        'notes',
        'content',
        server_default=None,
        existing_type=sa.JSON()
    )
