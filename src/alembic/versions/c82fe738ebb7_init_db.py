"""init_db

Revision ID: c82fe738ebb7
Revises: 
Create Date: 2020-03-15 15:48:01.151889

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c82fe738ebb7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # uuid_generate_v4() is not available by default
    connection = op.get_bind()
    connection.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scrape_task',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('scrape_text', sa.Boolean(), nullable=True),
    sa.Column('scrape_images', sa.Boolean(), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'RUNNING', 'DISPATCH', 'COMPLETED', 'FAILED', name='scrapetaskstatus'), nullable=False),
    sa.Column('error_message', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scrape_task_status'), 'scrape_task', ['status'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_scrape_task_status'), table_name='scrape_task')
    op.drop_table('scrape_task')
    # ### end Alembic commands ###
