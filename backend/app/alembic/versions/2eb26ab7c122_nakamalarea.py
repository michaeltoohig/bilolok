"""NakamalArea

Revision ID: 2eb26ab7c122
Revises: a3ccb4a64c10
Create Date: 2021-12-26 20:18:01.517765

"""
import uuid

from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = '2eb26ab7c122'
down_revision = 'a3ccb4a64c10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nakamal_area',
    sa.Column('id', fastapi_users_db_sqlalchemy.GUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    # Add initial row to nakamal_area that handles undefined area / initial default value since database has nakamals already
    nakamal_area_id = uuid.uuid4()
    op.execute(f"INSERT INTO nakamal_area(id, name) VALUES('{str(nakamal_area_id)}', 'UNDEFINED')")

    # Add column with default value set temporarily
    op.add_column('nakamal', sa.Column('area_id', fastapi_users_db_sqlalchemy.GUID(), nullable=False, server_default=str(nakamal_area_id)))
    # Remove column default value
    op.alter_column('nakamal', 'area_id', server_default=None)

    op.create_foreign_key(None, 'nakamal', 'nakamal_area', ['area_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'nakamal', type_='foreignkey')
    op.drop_column('nakamal', 'area_id')
    op.drop_table('nakamal_area')
    # ### end Alembic commands ###
