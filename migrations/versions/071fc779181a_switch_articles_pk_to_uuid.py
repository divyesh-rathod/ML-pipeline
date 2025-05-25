"""Switch Articles PK to UUID

Revision ID: 071fc779181a
Revises: 073c7b43d5c2
Create Date: 2025-04-12 12:07:41.603074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '071fc779181a'
down_revision: Union[str, None] = '073c7b43d5c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   # 1) If needed, enable pgcrypto extension for gen_random_uuid()
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    # 2) Drop the existing 'articles' table
    op.drop_table('articles')

    # 3) Recreate 'articles' table with UUID as primary key
    op.create_table(
        'articles',
        sa.Column(
            'id',
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
            index=True
        ),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('link', sa.Text, nullable=False, unique=True),
        sa.Column('pub_date', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('categories', postgresql.ARRAY(sa.Text))
    )



def downgrade() -> None:
      # Dropping and recreating for the downgrade can revert to integer ID if needed.
    # This step is optional depending on how you handle downgrades.
    op.drop_table('articles')

    op.create_table(
        'articles',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('link', sa.Text, nullable=False, unique=True),
        sa.Column('pub_date', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('categories', postgresql.ARRAY(sa.Text))
    )
