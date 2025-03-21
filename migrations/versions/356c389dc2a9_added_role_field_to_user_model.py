"""Added role field to User model

Revision ID: 356c389dc2a9
Revises: e8f09df1c10e
Create Date: 2025-03-17 12:20:04.705882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '356c389dc2a9'
down_revision = 'e8f09df1c10e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=10), nullable=True))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DATETIME(), nullable=True))
        batch_op.alter_column('password',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
        batch_op.drop_column('role')

    # ### end Alembic commands ###
