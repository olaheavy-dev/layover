// The Aspire app host: starts PostgreSQL, runs the migrations, then starts the backend and the
// website, and shows their traces in the Aspire dashboard. `make dev-all` runs it (`aspire run`).
// Local development only: `make check` and CI never need it.
import { createBuilder, OtlpProtocol, refExpr } from "./.aspire/modules/aspire.mjs";

const builder = await createBuilder();

// The same image, tag and digest as backend/compose/db/compose.yaml (it has the pgvector extension
// the first migration enables). tools/check_apphost_image.py fails `make check` when they differ.
const postgres = await builder
  .addPostgres("postgres")
  .withImage("pgvector/pgvector")
  .withImageTag("0.8.7-pg18-trixie")
  .withImageSHA256("5895949dfcdf308eb0cd31c950c93c14895c77f33fbedfecf1fa511ab1d4bcd2");
const database = await postgres.addDatabase("app");

// The URL in the form the backend's settings read (psycopg 3 through SQLAlchemy).
const databaseUrl = refExpr`postgresql+psycopg://${await database.getConnectionProperty("Username")}:${await database.getConnectionProperty("Password")}@${await database.getConnectionProperty("Host")}:${await database.getConnectionProperty("Port")}/${await database.getConnectionProperty("DatabaseName")}`;

// The tables, before the backend starts.
const migrate = await builder
  .addExecutable("migrate", "uv", "../backend", [
    "run", "--locked", "--extra", "db", "alembic", "upgrade", "heads",
  ])
  .withEnvironment("DATABASE_URL", databaseUrl)
  .waitFor(database);

// FastAPI's built-in OpenTelemetry sends the traces: it needs the HTTP/protobuf form of OTLP.
const backend = await builder
  .addUvicornApp("backend", "../backend", "app.main:app")
  // The installer must keep the database extra, or `uv sync` would remove psycopg.
  .withUv({ args: ["sync", "--locked", "--extra", "db"] })
  .withHttpEndpoint({ env: "PORT" })
  .withHttpHealthCheck({ path: "/health/live" })
  .withOtlpExporter({ protocol: OtlpProtocol.HttpProtobuf })
  .withEnvironment("FASTAPI_OTEL_AUTO_CONFIGURE", "true")
  .withEnvironment("DATABASE_URL", databaseUrl)
  .waitForCompletion(migrate);

// The website reads the samples from the backend; its server-side calls carry the trace on.
await builder
  .addJavaScriptApp("web", "../frontend")
  .withPnpm({ install: false })
  .withHttpEndpoint({ env: "PORT" })
  .withExternalHttpEndpoints()
  .withOtlpExporter({ protocol: OtlpProtocol.HttpProtobuf })
  .withEnvironment("API_BASE_URL", await backend.getEndpoint("http"))
  .waitFor(backend);

await builder.build().run();
