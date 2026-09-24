"""add is_active to users

Revision ID: eae815c03161
Revises:
Create Date: 2026-09-24 11:31:49.264188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eae815c03161'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        )
    )


def downgrade():
    op.drop_column('users', 'is_active')