"""added user_feed_table

Revision ID: 7bc44e97fcbe
Revises: a928f5afc686
Create Date: 2025-05-31 22:58:35.277644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7bc44e97fcbe'
down_revision: Union[str, None] = 'a928f5afc686'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_feed_position',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('last_read_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('cursor', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_feed_position')
    # ### end Alembic commands ###
