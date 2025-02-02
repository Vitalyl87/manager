"""test migration

Revision ID: 7e5c15f08b0f
Revises:
Create Date: 2024-12-31 14:11:53.158705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7e5c15f08b0f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('projects',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('status', sa.Enum('new', 'in_progress', 'completed', name='status'), server_default='new', nullable=False),
    sa.Column('deadline', sa.Date(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('tasks')
    op.drop_table('projects')
