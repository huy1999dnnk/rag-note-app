"""update enum text for embedding table

Revision ID: f64fbb0e7207
Revises: d8768c0cd202
Create Date: 2025-05-11 10:30:42.438095

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f64fbb0e7207"
down_revision: Union[str, None] = "d8768c0cd202"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create a new enum type with uppercase values
    op.execute(
        "CREATE TYPE embeddingsource_new AS ENUM ('NOTE_TEXT', 'PDF_ATTACHMENT')"
    )

    op.execute("ALTER TABLE document_embeddings ALTER COLUMN source_type TYPE text")

    # Update existing records to use the new uppercase values
    op.execute(
        "UPDATE document_embeddings SET source_type = 'NOTE_TEXT' WHERE source_type = 'note_text'"
    )
    op.execute(
        "UPDATE document_embeddings SET source_type = 'PDF_ATTACHMENT' WHERE source_type = 'pdf_attachment'"
    )

    # Temporarily allow NULL values
    op.execute("ALTER TABLE document_embeddings ALTER COLUMN source_type DROP NOT NULL")

    # Change column type to use new enum
    op.execute(
        "ALTER TABLE document_embeddings ALTER COLUMN source_type TYPE embeddingsource_new USING source_type::text::embeddingsource_new"
    )

    # Restore NOT NULL constraint
    op.execute("ALTER TABLE document_embeddings ALTER COLUMN source_type SET NOT NULL")

    # Drop old enum type
    op.execute("DROP TYPE embeddingsource")

    # Rename new enum type to match old name
    op.execute("ALTER TYPE embeddingsource_new RENAME TO embeddingsource")


def downgrade():
    # Create a new enum type with lowercase values
    op.execute(
        "CREATE TYPE embeddingsource_old AS ENUM ('note_text', 'pdf_attachment')"
    )

    # Update existing records to use the lowercase values
    op.execute(
        "UPDATE document_embeddings SET source_type = 'note_text' WHERE source_type = 'NOTE_TEXT'"
    )
    op.execute(
        "UPDATE document_embeddings SET source_type = 'pdf_attachment' WHERE source_type = 'PDF_ATTACHMENT'"
    )

    # Temporarily allow NULL values
    op.execute("ALTER TABLE document_embeddings ALTER COLUMN source_type DROP NOT NULL")

    # Change column type to use old enum
    op.execute(
        "ALTER TABLE document_embeddings ALTER COLUMN source_type TYPE embeddingsource_old USING source_type::text::embeddingsource_old"
    )

    # Restore NOT NULL constraint
    op.execute("ALTER TABLE document_embeddings ALTER COLUMN source_type SET NOT NULL")

    # Drop new enum type
    op.execute("DROP TYPE embeddingsource")

    # Rename old enum type to match expected name
    op.execute("ALTER TYPE embeddingsource_old RENAME TO embeddingsource")
