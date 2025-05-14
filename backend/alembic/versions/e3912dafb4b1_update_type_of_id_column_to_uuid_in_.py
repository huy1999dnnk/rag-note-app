"""Update type of id column to UUID in notes and workspace

Revision ID: e3912dafb4b1
Revises: 18a2d0d98861
Create Date: 2025-04-18 03:22:04.672226

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'e3912dafb4b1'
down_revision: Union[str, None] = '18a2d0d98861'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Enable uuid extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Add temporary UUID columns
    op.add_column('workspaces', sa.Column('id_tmp', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False))
    op.add_column('workspaces', sa.Column('parent_id_tmp', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('notes', sa.Column('id_tmp', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False))
    op.add_column('notes', sa.Column('workspace_id_tmp', postgresql.UUID(as_uuid=True), nullable=False))

    # Drop foreign key constraint on workspaces.parent_id (self-reference)
    op.drop_constraint('workspaces_parent_id_fkey', 'workspaces', type_='foreignkey')

    # Drop notes → workspaces FK constraint
    op.drop_constraint('notes_workspace_id_fkey', 'notes', type_='foreignkey')

    # Drop primary keys
    op.drop_constraint('notes_pkey', 'notes', type_='primary')
    op.drop_constraint('workspaces_pkey', 'workspaces', type_='primary')

    # Drop old columns
    op.drop_column('notes', 'id')
    op.drop_column('notes', 'workspace_id')
    op.drop_column('workspaces', 'id')
    op.drop_column('workspaces', 'parent_id')

    # Rename new columns to original names
    op.alter_column('notes', 'id_tmp', new_column_name='id')
    op.alter_column('notes', 'workspace_id_tmp', new_column_name='workspace_id')
    op.alter_column('workspaces', 'id_tmp', new_column_name='id')
    op.alter_column('workspaces', 'parent_id_tmp', new_column_name='parent_id')

    # Recreate primary keys
    op.create_primary_key('workspaces_pkey', 'workspaces', ['id'])
    op.create_primary_key('notes_pkey', 'notes', ['id'])

    # Recreate foreign key constraints
    op.create_foreign_key(
        'workspaces_parent_id_fkey',
        source_table='workspaces',
        referent_table='workspaces',
        local_cols=['parent_id'],
        remote_cols=['id'],
    )

    op.create_foreign_key(
        'notes_workspace_id_fkey',
        source_table='notes',
        referent_table='workspaces',
        local_cols=['workspace_id'],
        remote_cols=['id'],
    )


def downgrade():
    raise NotImplementedError("Downgrade not supported for UUID migration.")
