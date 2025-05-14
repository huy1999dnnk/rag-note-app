"""change id to serial socialaccount table

Revision ID: 480d3ae15885
Revises: fb7f63201455
Create Date: 2025-04-26 03:40:34.909658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '480d3ae15885'
down_revision: Union[str, None] = 'fb7f63201455'
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
