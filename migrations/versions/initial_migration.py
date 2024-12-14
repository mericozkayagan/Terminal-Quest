from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "initial_migration"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the players table
    op.create_table(
        "players",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.String),
        sa.Column("health", sa.Integer, nullable=False),
        sa.Column("max_health", sa.Integer, nullable=False),
        sa.Column("attack", sa.Integer, nullable=False),
        sa.Column("defense", sa.Integer, nullable=False),
        sa.Column("level", sa.Integer, nullable=False),
        sa.Column("mana", sa.Integer, nullable=False),
        sa.Column("max_mana", sa.Integer, nullable=False),
        sa.Column("exp", sa.Integer, nullable=False),
        sa.Column("exp_to_level", sa.Integer, nullable=False),
        sa.Column("inventory", sa.JSON, nullable=False),
        sa.Column("equipment", sa.JSON, nullable=False),
        sa.Column("skills", sa.JSON, nullable=False),
        sa.Column("session_id", sa.String),
    )

    # Create the enemies table
    op.create_table(
        "enemies",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.String),
        sa.Column("health", sa.Integer, nullable=False),
        sa.Column("max_health", sa.Integer, nullable=False),
        sa.Column("attack", sa.Integer, nullable=False),
        sa.Column("defense", sa.Integer, nullable=False),
        sa.Column("level", sa.Integer, nullable=False),
        sa.Column("exp_reward", sa.Integer, nullable=False),
        sa.Column("art", sa.String),
    )

    # Create the game_states table
    op.create_table(
        "game_states",
        sa.Column("player_id", sa.String, primary_key=True),
        sa.Column("game_state", sa.JSON, nullable=False),
    )

    # Create the sessions table
    op.create_table(
        "sessions",
        sa.Column("session_id", sa.String, primary_key=True),
        sa.Column("player_data", sa.JSON, nullable=False),
        sa.Column("expiration", sa.Integer, nullable=False),
    )

    # Create the shop_states table
    op.create_table(
        "shop_states",
        sa.Column("player_id", sa.String, primary_key=True),
        sa.Column("shop_state", sa.JSON, nullable=False),
    )


def downgrade():
    op.drop_table("shop_states")
    op.drop_table("sessions")
    op.drop_table("game_states")
    op.drop_table("enemies")
    op.drop_table("players")
