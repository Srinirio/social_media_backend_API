"""I this commit i added registration model,hashing,schemas

Revision ID: 1d879c0308e4
Revises: 797bbeb43932
Create Date: 2024-09-11 16:38:07.811500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d879c0308e4'
down_revision: Union[str, None] = '797bbeb43932'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('registration', sa.Column('name', sa.String(length=50), nullable=False))
    op.add_column('registration', sa.Column('email', sa.String(length=100), nullable=False))
    op.add_column('registration', sa.Column('password', sa.String(length=200), nullable=False))
    op.add_column('registration', sa.Column('secret_key', sa.String(length=200), nullable=False))
    op.add_column('registration', sa.Column('registration_date', sa.DateTime(), nullable=False))
    op.add_column('registration', sa.Column('otp', sa.Integer(), nullable=True))
    op.add_column('registration', sa.Column('otp_expiry_date', sa.DateTime(), nullable=True))
    op.add_column('registration', sa.Column('is_otp_verified', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'registration', ['secret_key'])
    op.create_unique_constraint(None, 'registration', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'registration', type_='unique')
    op.drop_constraint(None, 'registration', type_='unique')
    op.drop_column('registration', 'is_otp_verified')
    op.drop_column('registration', 'otp_expiry_date')
    op.drop_column('registration', 'otp')
    op.drop_column('registration', 'registration_date')
    op.drop_column('registration', 'secret_key')
    op.drop_column('registration', 'password')
    op.drop_column('registration', 'email')
    op.drop_column('registration', 'name')
    # ### end Alembic commands ###
