"""add default value to content column in note table

Revision ID: 2cbb25420513
Revises: e3912dafb4b1
Create Date: 2025-04-21 06:45:42.732382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import json
default_content = {"type": "doc", "content": []}

# revision identifiers, used by Alembic.
revision: str = '2cbb25420513'
down_revision: Union[str, None] = 'e3912dafb4b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('notes', 'content',
                    existing_type=sa.JSON(),
                      server_default=sa.text(f"'{json.dumps(default_content)}'::jsonb"))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'notes',
        'content',
        existing_type=sa.JSON(),
        server_default=None
    )
