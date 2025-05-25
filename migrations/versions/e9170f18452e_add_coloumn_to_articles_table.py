"""Add coloumn to Articles table

Revision ID: e9170f18452e
Revises: 071fc779181a
Create Date: 2025-04-12 12:14:05.542939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9170f18452e'
down_revision: Union[str, None] = '071fc779181a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the 'processed' column to the 'articles' table
    op.add_column(
        'articles',
        sa.Column(
            'processed',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false')
        )
    )

def downgrade():
    # Remove the 'processed' column if you downgrade
    op.drop_column('articles', 'processed')
