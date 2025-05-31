"""Make pub_date a timestamptz

Revision ID: e16bb48b1880
Revises: f2414444155f
Create Date: 2025-05-30 19:43:19.262391
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e16bb48b1880'
down_revision: Union[str, None] = 'f2414444155f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # convert existing TEXT pub_dates into timestamptz
    op.alter_column(
        'articles', 'pub_date',
        existing_type=sa.TEXT(),
        type_=sa.TIMESTAMP(timezone=True),
        nullable=False,
        postgresql_using="pub_date::timestamptz"
    )
    op.create_index('ix_articles_pub_date', 'articles', ['pub_date'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_articles_pub_date', table_name='articles')
    # cast back to text if you ever roll back
    op.alter_column(
        'articles', 'pub_date',
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.TEXT(),
        nullable=True,
        postgresql_using="pub_date::text"
    )
