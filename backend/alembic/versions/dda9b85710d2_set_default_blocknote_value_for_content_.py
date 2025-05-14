"""set default blocknote value for content column in notes table

Revision ID: dda9b85710d2
Revises: 116b2fb59f6f
Create Date: 2025-04-22 06:38:19.836305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import json


# revision identifiers, used by Alembic.
revision: str = 'dda9b85710d2'
down_revision: Union[str, None] = '116b2fb59f6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


new_default = [
    {
        "id": "1",
        "type": "paragraph",
        "props": {},
        "content": []
    }
]

old_default = [{}]  # or whatever your previous default was

def upgrade():
    op.alter_column(
        'notes',
        'content',
        server_default=sa.text(f"'{json.dumps(new_default)}'::json")
    )


def downgrade():
    op.alter_column(
        'notes',
        'content',
        server_default=sa.text(f"'{json.dumps(old_default)}'::json")
    )
