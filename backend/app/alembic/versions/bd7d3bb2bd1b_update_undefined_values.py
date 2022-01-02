"""Update Undefined Values

Revision ID: bd7d3bb2bd1b
Revises: 02d698935816
Create Date: 2022-01-02 10:29:54.395535

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = 'bd7d3bb2bd1b'
down_revision = '02d698935816'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    # Update nakamal undefined light value
    res = conn.execute("SELECT id FROM nakamal WHERE light = 'Undefined'")
    results = res.fetchall()
    for res in results:
        conn.execute(f"UPDATE nakamal SET light = 'UNDEFINED' WHERE id = '{str(res[0])}'")
    # Update nakamal_area undefined value
    res = conn.execute("SELECT id FROM nakamal_area WHERE name = 'Undefined'")
    results = res.fetchall()
    for res in results:
        conn.execute(f"UPDATE nakamal_area SET name = 'UNDEFINED' WHERE id = '{str(res[0])}'")


def downgrade():
    pass
