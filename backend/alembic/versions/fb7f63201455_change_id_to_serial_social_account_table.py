"""change id to serial social account table

Revision ID: fb7f63201455
Revises: 9c8fb06e2e6c
Create Date: 2025-04-26 03:38:26.097790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb7f63201455'
down_revision: Union[str, None] = '9c8fb06e2e6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the primary key constraint first
    op.execute('ALTER TABLE social_accounts DROP CONSTRAINT IF EXISTS social_accounts_pkey')
    
    # Drop the column and recreate it as SERIAL
    op.execute('ALTER TABLE social_accounts DROP COLUMN id')
    op.execute('ALTER TABLE social_accounts ADD COLUMN id SERIAL PRIMARY KEY')

def downgrade() -> None:
    op.execute('ALTER TABLE social_accounts DROP COLUMN id')
    op.execute('ALTER TABLE social_accounts ADD COLUMN id VARCHAR PRIMARY KEY')
