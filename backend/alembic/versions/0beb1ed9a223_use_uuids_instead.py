"""use UUIDs instead of sequential IDs

Revision ID: 0beb1ed9a223
Revises: f39843df4eca
Create Date: 2020-05-02 12:00:59.121969

Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "0beb1ed9a223"
down_revision = "f39843df4eca"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    ALTER TABLE users
    -- we have to remove the default first because UUIDs can't be cast to the existing integer defaults
        ALTER COLUMN id DROP DEFAULT,
        ALTER COLUMN id SET DATA TYPE uuid USING uuid_generate_v4(),
        ALTER COLUMN id SET DEFAULT uuid_generate_v4();
    DROP SEQUENCE users_id_seq;"""
    )


def downgrade():
    op.execute(
        """CREATE SEQUENCE users_id_seq AS integer OWNED BY users.id;
    ALTER TABLE users
        ALTER COLUMN id DROP DEFAULT,
        ALTER COLUMN id SET DATA TYPE integer USING nextval('users_id_seq'::regclass),
        ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);
    DROP EXTENSION IF EXISTS "uuid-ossp";
    """
    )
