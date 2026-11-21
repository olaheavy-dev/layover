"""Settings from the environment (and backend/.env locally), read once per process.

Names are the upper-case field names with no prefix (APP_ENV, LOG_LEVEL, DATABASE_URL, ...).
Secrets are SecretStr so they never print in logs or tracebacks; .env.example lists every setting
with a safe value.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# The local development values (backend/compose/); production must set its own.
LOCAL_DATABASE_URL = "postgresql+psycopg://app:app@localhost:5432/app"


class Settings(BaseSettings):
    # ENV_FILE="" turns the file off: the tests set it before any app code loads, so a
    # developer's backend/.env (real keys included) never reaches them.
    # hide_input_in_errors: a validation error must never echo the raw input, which may hold a key.
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE", ".env") or None,
        extra="ignore",
        frozen=True,
        hide_input_in_errors=True,
    )

    app_env: Literal["local", "test", "production"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    # JSON logs in production; readable console logs everywhere else.
    log_json: bool = False
    # Largest request body the API reads, in bytes; larger ones get a 413.
    # Large files should not come through the API.
    max_request_bytes: int = Field(default=1_048_576, gt=0)
    # Interactive API docs at /docs. Unset means on everywhere except production.
    docs_enabled: bool | None = None

    # SQLAlchemy URL with the psycopg 3 driver. The default matches the local db in
    # backend/compose/db/compose.yaml.
    database_url: SecretStr = SecretStr(LOCAL_DATABASE_URL)
    # Connections per process: keep pool_size + max_overflow times the worker count under
    # Postgres's max_connections.
    db_pool_size: int = 5
    db_max_overflow: int = 10
    # Server-side limits on every connection: a runaway query, or a transaction left open while
    # the request waits on something else, is cut off instead of holding a connection (and its
    # locks) indefinitely. Milliseconds.
    db_statement_timeout_ms: int = Field(default=30_000, gt=0)
    db_idle_in_transaction_timeout_ms: int = Field(default=60_000, gt=0)

    # Browser origins allowed to call the API (CORS), e.g. ["https://app.example.com"]. Empty
    # means none: same-origin and server-to-server calls only.
    cors_origins: list[str] = []
    # Host headers the API answers to, e.g. ["api.example.com"]; ["*"] accepts any.
    allowed_hosts: list[str] = ["*"]

    @model_validator(mode="after")
    def no_local_defaults_in_production(self) -> Settings:
        """Refuse to start in production on the local development credentials: a missing secret
        would otherwise boot the app against localhost, or leave a known key live."""
        if self.app_env != "production":
            return self
        problems = []
        if self.database_url.get_secret_value() == LOCAL_DATABASE_URL:
            problems.append("DATABASE_URL is the local default")
        if problems:
            raise ValueError("production settings: " + "; ".join(problems))
        return self

    @property
    def docs_on(self) -> bool:
        return self.app_env != "production" if self.docs_enabled is None else self.docs_enabled


@lru_cache
def get_settings() -> Settings:
    return Settings()
