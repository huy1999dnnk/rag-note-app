"""add source type and source file to document embedding table

Revision ID: 83de7166bcab
Revises: bd7ac7384ee0
Create Date: 2025-05-09 08:10:31.506553

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "83de7166bcab"
down_revision: Union[str, None] = "bd7ac7384ee0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type
    op.execute("DROP TYPE IF EXISTS embeddingsource")
    op.execute("CREATE TYPE embeddingsource AS ENUM ('note_text', 'pdf_attachment')")

    # 1. Add source_type column as NULLABLE first
    op.add_column(
        "document_embeddings",
        sa.Column(
            "source_type",
            sa.Enum("note_text", "pdf_attachment", name="embeddingsource"),
            nullable=True,
        ),  # Start as nullable
    )

    # 2. Add source_file column
    op.add_column(
        "document_embeddings", sa.Column("source_file", sa.String(), nullable=True)
    )

    # 3. Update existing records to have the default value
    op.execute("UPDATE document_embeddings SET source_type = 'note_text'")

    # 4. Now make the column NOT NULL
    op.alter_column("document_embeddings", "source_type", nullable=False)


def downgrade() -> None:
    # Remove columns
    op.drop_column("document_embeddings", "source_file")
    op.drop_column("document_embeddings", "source_type")

    # Drop enum type
    op.execute("DROP TYPE embeddingsource")
