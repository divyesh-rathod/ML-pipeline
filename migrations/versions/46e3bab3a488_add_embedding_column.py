"""add embedding column

Revision ID: 46e3bab3a488
Revises: 83bb296564d6
Create Date: 2025-04-16 09:15:17.787725

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector  # Import the Vector column type

# revision identifiers, used by Alembic.
revision = '46e3bab3a488'
down_revision = '83bb296564d6'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Ensure the pgvector extension is created (only needed once per DB).
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Add the new embedding column to the processed_articles table.
    op.add_column('processed_articles', sa.Column('embedding', Vector(384), nullable=True))

def downgrade() -> None:
    # Remove the embedding column if downgrading.
    op.drop_column('processed_articles', 'embedding')
