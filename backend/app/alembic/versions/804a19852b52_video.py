"""Video

Revision ID: 804a19852b52
Revises: 4a7fed5c8cf2
Create Date: 2022-04-24 19:02:28.848495

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy
import sqlalchemy_utc
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '804a19852b52'
down_revision = '4a7fed5c8cf2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video',
    sa.Column('id', fastapi_users_db_sqlalchemy.guid.GUID(), nullable=False),
    sa.Column('created_at', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=True),
    sa.Column('file_id', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=True),
    sa.Column('filetype', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'PROGRESS', 'COMPLETE', 'ERROR', name='videoprocessingstatus'), nullable=False),
    sa.Column('user_id', fastapi_users_db_sqlalchemy.guid.GUID(), nullable=False),
    sa.Column('nakamal_id', fastapi_users_db_sqlalchemy.guid.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['nakamal_id'], ['nakamal.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('file_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    # ### end Alembic commands ###