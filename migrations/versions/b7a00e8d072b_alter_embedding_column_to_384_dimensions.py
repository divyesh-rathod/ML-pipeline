"""Alter embedding column to 384 dimensions

Revision ID: b7a00e8d072b
Revises: 46e3bab3a488
Create Date: 2025-04-16 12:20:28.465164

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b7a00e8d072b'
down_revision = '46e3bab3a488'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Ensure the pgvector extension is enabled
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    # Alter the column type on processed_articles to vector(384)
    op.execute(
        "ALTER TABLE processed_articles ALTER COLUMN embedding TYPE vector(384) USING embedding::vector(384)"
    )

def downgrade() -> None:
    # Revert the column type back to vector(768)
    op.execute(
        "ALTER TABLE processed_articles ALTER COLUMN embedding TYPE vector(768) USING embedding::vector(768)"
    )

    # ### end Alembic commands ###
