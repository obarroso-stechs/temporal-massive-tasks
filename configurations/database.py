from configurations.env import env

# Async URL for FastAPI routes (asyncpg driver)
DATABASE_URL: str = env.str(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:1234@localhost:5432/temporal_tasks",
)

# Sync URL for Temporal activities (psycopg2 driver, runs in ThreadPoolExecutor)
SYNC_DATABASE_URL: str = env.str(
    "SYNC_DATABASE_URL",
    "postgresql+psycopg2://postgres:1234@localhost:5432/temporal_tasks",
)
