"""NakamalResource table

Revision ID: a3ccb4a64c10
Revises: 2da4602ae513
Create Date: 2021-12-10 14:57:35.558562

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy
import sqlalchemy_utc
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a3ccb4a64c10'
down_revision = '2da4602ae513'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nakamal_resource',
    sa.Column('id', fastapi_users_db_sqlalchemy.GUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nakamal_resource_assocation',
    sa.Column('nakamal_id', fastapi_users_db_sqlalchemy.GUID(), nullable=False),
    sa.Column('resource_id', fastapi_users_db_sqlalchemy.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['nakamal_id'], ['nakamal.id'], ),
    sa.ForeignKeyConstraint(['resource_id'], ['nakamal_resource.id'], ),
    sa.PrimaryKeyConstraint('nakamal_id', 'resource_id')
    )
    op.add_column('nakamal', sa.Column('aliases', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('nakamal', sa.Column('windows', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('nakamal', 'windows')
    op.drop_column('nakamal', 'aliases')
    op.drop_table('nakamal_resource_assocation')
    op.drop_table('nakamal_resource')
    # ### end Alembic commands ###
