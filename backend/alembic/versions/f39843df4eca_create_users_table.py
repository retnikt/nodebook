"""create users table

Revision ID: f39843df4eca
Revises:
Create Date: 2020-05-01 14:38:38.240709

"""
from alembic import op
import sqlalchemy


# revision identifiers, used by Alembic.
revision = "f39843df4eca"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("email", sqlalchemy.String),
        sqlalchemy.Column("password", sqlalchemy.String),
    )


def downgrade():
    op.drop_table("users")
