"""Add new table to store processed Articles

Revision ID: 83bb296564d6
Revises: e9170f18452e
Create Date: 2025-04-12 13:54:28.803036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '83bb296564d6'
down_revision: Union[str, None] = 'e9170f18452e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Example: no pgvector column yet, since you're deferring embeddings.
    # If you need the extension or a vector column later, you can add it
    # in a future migration.
    
    op.create_table(
        'processed_articles',
        # We use article_id as the primary key and foreign key.
        sa.Column(
            'article_id',
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey(
                'articles.id',
                ondelete='CASCADE'  # so if an article is deleted, the processed row goes too
            ),
            primary_key=True,
            nullable=False
        ),
        # Example columns
        sa.Column('cleaned_text', sa.Text, nullable=True),
        sa.Column('category_1', sa.Text, nullable=True),   # from the original raw category, if desired
        sa.Column('category_2', sa.Text, nullable=True),   # your ML-generated category
        sa.Column(
            'processed_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        )
        # Add more columns here if needed (e.g., sentiment_score, language, etc.)
    )

def downgrade():
    op.drop_table('processed_articles')
