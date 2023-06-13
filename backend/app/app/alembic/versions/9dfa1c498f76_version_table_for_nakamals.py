"""Version table for nakamals

Revision ID: 9dfa1c498f76
Revises: bc998ca58ebc
Create Date: 2022-03-06 18:31:13.783105

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy
import sqlalchemy_utc
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9dfa1c498f76'
down_revision = 'bc998ca58ebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nakamal_resource_assocation_version',
    sa.Column('nakamal_id', fastapi_users_db_sqlalchemy.guid.GUID(), autoincrement=False, nullable=False),
    sa.Column('resource_id', fastapi_users_db_sqlalchemy.guid.GUID(), autoincrement=False, nullable=False),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('nakamal_id', 'resource_id', 'transaction_id')
    )
    op.create_index(op.f('ix_nakamal_resource_assocation_version_end_transaction_id'), 'nakamal_resource_assocation_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_nakamal_resource_assocation_version_operation_type'), 'nakamal_resource_assocation_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_nakamal_resource_assocation_version_transaction_id'), 'nakamal_resource_assocation_version', ['transaction_id'], unique=False)
    op.create_table('nakamal_version',
    sa.Column('id', fastapi_users_db_sqlalchemy.guid.GUID(), autoincrement=False, nullable=False),
    sa.Column('created_at', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), autoincrement=False, nullable=True),
    sa.Column('updated_at', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), autoincrement=False, nullable=True),
    sa.Column('name', sa.String(), autoincrement=False, nullable=False),
    sa.Column('aliases', postgresql.ARRAY(sa.String()), autoincrement=False, nullable=False),
    sa.Column('lat', sa.Float(), autoincrement=False, nullable=False),
    sa.Column('lng', sa.Float(), autoincrement=False, nullable=False),
    sa.Column('light', sa.String(), autoincrement=False, nullable=True),
    sa.Column('owner', sa.String(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.String(), autoincrement=False, nullable=True),
    sa.Column('windows', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('kava_source_id', fastapi_users_db_sqlalchemy.guid.GUID(), autoincrement=False, nullable=False),
    sa.Column('area_id', fastapi_users_db_sqlalchemy.guid.GUID(), autoincrement=False, nullable=False),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.Column('created_at_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('updated_at_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('name_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('aliases_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('lat_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('lng_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('light_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('owner_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('phone_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('windows_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('kava_source_id_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('area_id_mod', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    op.create_index(op.f('ix_nakamal_version_end_transaction_id'), 'nakamal_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_nakamal_version_operation_type'), 'nakamal_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_nakamal_version_transaction_id'), 'nakamal_version', ['transaction_id'], unique=False)
    op.create_table('transaction',
    sa.Column('issued_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('remote_addr', sa.String(length=50), nullable=True),
    sa.Column('user_id', fastapi_users_db_sqlalchemy.guid.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_user_id'), 'transaction', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_user_id'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_index(op.f('ix_nakamal_version_transaction_id'), table_name='nakamal_version')
    op.drop_index(op.f('ix_nakamal_version_operation_type'), table_name='nakamal_version')
    op.drop_index(op.f('ix_nakamal_version_end_transaction_id'), table_name='nakamal_version')
    op.drop_table('nakamal_version')
    op.drop_index(op.f('ix_nakamal_resource_assocation_version_transaction_id'), table_name='nakamal_resource_assocation_version')
    op.drop_index(op.f('ix_nakamal_resource_assocation_version_operation_type'), table_name='nakamal_resource_assocation_version')
    op.drop_index(op.f('ix_nakamal_resource_assocation_version_end_transaction_id'), table_name='nakamal_resource_assocation_version')
    op.drop_table('nakamal_resource_assocation_version')
    # ### end Alembic commands ###