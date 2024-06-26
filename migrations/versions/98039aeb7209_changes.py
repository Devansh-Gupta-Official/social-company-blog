"""changes

Revision ID: 98039aeb7209
Revises: ad6c11efd3e7
Create Date: 2024-05-11 08:28:27.611333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98039aeb7209'
down_revision = 'ad6c11efd3e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=140),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.String(length=140),
               type_=sa.VARCHAR(length=40),
               existing_nullable=False)

    # ### end Alembic commands ###
