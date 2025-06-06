"""Create user_reads table

Revision ID: a928f5afc686
Revises: e16bb48b1880
Create Date: 2025-05-31 12:36:51.058705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a928f5afc686'
down_revision: Union[str, None] = 'e16bb48b1880'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_reads',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('read_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'article_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_reads')
    # ### end Alembic commands ###
