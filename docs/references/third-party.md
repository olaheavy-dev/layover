# Third-party documentation

Official documentation for the tools and services Layover uses. Pinned versions are added when each dependency is added (with the template layers at build start). Check the official page for the pinned version before using an API, not memory.

| Tool or service | Official documentation | Used for |
|---|---|---|
| Copier | https://copier.readthedocs.io/ | Applying and updating the house templates |
| LangGraph (Python) | https://docs.langchain.com/oss/python/langgraph/ | Agent graph, interrupts, checkpoints, `Send` |
| Model Context Protocol | https://modelcontextprotocol.io/ | Tool servers |
| LangChain MCP adapters | https://github.com/langchain-ai/langchain-mcp-adapters | Connecting MCP servers to LangGraph |
| FastAPI | https://fastapi.tiangolo.com/ | Backend API |
| Next.js | https://nextjs.org/docs | Frontend |
| Claude tool use | https://docs.anthropic.com/en/docs/build-with-claude/tool-use | Tool calling |
| Duffel API | https://duffel.com/docs | Sandbox booking |
| Travelpayouts API and data | https://support.travelpayouts.com/hc/en-us/categories/200358578-API-and-data | Cached fares |
| Source Serif 4 (font) | https://fonts.google.com/specimen/Source+Serif+4 | Display font: place names and headings ([design brief](../design/brief.md)). SIL Open Font License 1.1 ([OFL.txt](https://github.com/google/fonts/blob/main/ofl/sourceserif4/OFL.txt)) |
| Source Sans 3 (font) | https://fonts.google.com/specimen/Source+Sans+3 | Body font: text and figures. SIL Open Font License 1.1 ([OFL.txt](https://github.com/google/fonts/blob/main/ofl/sourcesans3/OFL.txt)) |
| Lucide (icons) | https://lucide.dev/ | Icons on every widget. ISC licence, with MIT for the icons derived from Feather: keep both notices ([LICENSE](https://github.com/lucide-icons/lucide/blob/main/LICENSE)). The package and its version are added with the frontend |
| Aspire | https://aspire.dev/ ([Python integration](https://aspire.dev/integrations/frameworks/python/), [prerequisites](https://aspire.dev/get-started/prerequisites/)) | Local orchestration and tracing, from build plan 1. Version pinned when added |
| Floorplan 0.11.0 (Claude Code plugin) | https://github.com/haydenschmitty/floorplan ([privacy and security](https://github.com/haydenschmitty/floorplan/blob/main/docs/privacy-and-security.md)) | Draws the map snapshot at each stage gate (`docs/floorplan/`). MIT licence. Reviewed before the Design gate (#39): it runs locally, and its only outside call is an opt-in waitlist, turned off with `FLOORPLAN_NO_PROMPTS=1`; the installed files matched the checksums published with the `floorplan--v0.11.0` tag on 20 Nov 2026. Not yet pinned ([agent-workflows#30](https://github.com/olaheavy-dev/agent-workflows/issues/30)) |
| Bundled in each Floorplan snapshot | elkjs 0.9.3 (https://github.com/kieler/elkjs), Inter (https://github.com/rsms/inter), JetBrains Mono (https://github.com/JetBrains/JetBrainsMono) | The map's layout engine (Eclipse Public License 2.0) and fonts (SIL Open Font License 1.1), copied into `docs/floorplan/design.html` by the export. Their licence texts are in [`docs/floorplan/licences/`](../floorplan/licences/) |
| WCAG 2.2 | https://www.w3.org/TR/WCAG22/ | Accessibility target (AA); contrast formulas used by `tools/check_contrast.py` |

## Approved with the template sets (owner, 21 Nov 2026)

The owner approved the packages that `house-template-fastapi` v0.11.1 and `house-template-nextjs` v0.3.0 bring, at those tagged versions, as a set. Versions are the ones in `backend/uv.lock` (Python) and the exact pins in `frontend/package.json` (npm). Each licence was read from the package's registry page (PyPI or npm) for that version on 21 Nov 2026; where PyPI has no licence field, the licence classifier is used. Rows marked "Locked in `uv.lock`, not installed" belong to extras that the answers `llm: none` and `storage: false` leave out. `psycopg`, `psycopg-pool` and `psycopg-binary` are LGPL-3.0-only, which the dependency review now allows by package name (`.github/workflows/dependency-review.yml`; owner's decision, 21 Nov 2026). `next` and `eslint-config-next` are 16.4.6, one step ahead of the template's 16.4.3 pin (security fixes; see the decision register).

| Package and version | Official documentation | Used for, group and licence |
|---|---|---|
| fastapi 0.162.0 | https://fastapi.tiangolo.com/ | Backend web framework (backend). MIT ([PyPI](https://pypi.org/project/fastapi/0.162.0/)) |
| pydantic-settings 2.16.3 | https://docs.pydantic.dev/latest/concepts/pydantic_settings/ | Backend settings read from the environment (backend). MIT ([PyPI](https://pypi.org/project/pydantic-settings/2.16.3/)) |
| structlog 26.1.0 | https://www.structlog.org/ | Structured logging (backend). MIT OR Apache-2.0 ([PyPI](https://pypi.org/project/structlog/26.1.0/)) |
| alembic 1.20.1 | https://alembic.sqlalchemy.org/en/latest/ | Database migrations (backend `db` extra). MIT ([PyPI](https://pypi.org/project/alembic/1.20.1/)) |
| pgvector 0.5.1 | https://github.com/pgvector/pgvector-python | Vector column type for SQLAlchemy. Installed, and the template's migration enables the `vector` extension, but not used until the vector database is chosen in step 3 (backend `db` extra). MIT ([PyPI](https://pypi.org/project/pgvector/0.5.1/)) |
| psycopg 3.3.6 | https://psycopg.org/psycopg3/docs/ | PostgreSQL driver (the `binary` and `pool` extras) (backend `db` extra). LGPL-3.0-only ([PyPI](https://pypi.org/project/psycopg/3.3.6/)) |
| psycopg-pool 3.3.3 | https://www.psycopg.org/psycopg3/docs/advanced/pool.html | PostgreSQL connection pool (backend `db` extra). LGPL-3.0-only ([PyPI](https://pypi.org/project/psycopg-pool/3.3.3/)) |
| psycopg-binary 3.3.6 | https://psycopg.org/psycopg3/docs/ | The compiled build of the psycopg driver that `psycopg[binary]` installs (backend `db` extra, pulled in by `psycopg`, not listed in `pyproject.toml`). Allowed in the dependency review under the owner's "Allow by package" answer, which named psycopg and psycopg-pool; it is the same driver. LGPL-3.0-only ([PyPI](https://pypi.org/project/psycopg-binary/3.3.6/)) |
| sqlalchemy 2.1.6 | https://docs.sqlalchemy.org | Database toolkit (async) (backend `db` extra). MIT ([PyPI](https://pypi.org/project/SQLAlchemy/2.1.6/)) |
| langchain 1.5.0 | https://reference.langchain.com/python/langchain/langchain/ | LangChain 1.x agents. **Locked in `uv.lock`, not installed** (`langchain` extra; the `llm` and `storage` answers are `none` and `false`) (backend `langchain` extra). MIT ([PyPI](https://pypi.org/project/langchain/1.5.0/)) |
| langchain-anthropic 1.7.10 | https://reference.langchain.com/python/integrations/langchain_anthropic/ | Claude models for LangChain. **Locked in `uv.lock`, not installed** (`langchain` extra; the `llm` and `storage` answers are `none` and `false`) (backend `langchain` extra). MIT ([PyPI](https://pypi.org/project/langchain-anthropic/1.7.10/)) |
| langchain-core 1.8.0 | https://reference.langchain.com/python/langchain_core/ | LangChain core types. **Locked in `uv.lock`, not installed** (`langchain` extra; the `llm` and `storage` answers are `none` and `false`) (backend `langchain` extra). MIT ([PyPI](https://pypi.org/project/langchain-core/1.8.0/)) |
| langchain-openai 1.8.0 | https://reference.langchain.com/python/integrations/langchain_openai/ | OpenAI models for LangChain. **Locked in `uv.lock`, not installed** (`langchain` extra; the `llm` and `storage` answers are `none` and `false`) (backend `langchain` extra). MIT ([PyPI](https://pypi.org/project/langchain-openai/1.8.0/)) |
| langgraph 1.2.22 | https://reference.langchain.com/python/langgraph/ | Agent graph, interrupts, checkpoints. **Locked in `uv.lock`, not installed** (`langchain` extra; the `llm` and `storage` answers are `none` and `false`) (backend `langchain` extra). MIT ([PyPI](https://pypi.org/project/langgraph/1.2.22/)) |
| langgraph-checkpoint-postgres 3.2.1 | https://pypi.org/project/langgraph-checkpoint-postgres/ | LangGraph checkpoints in PostgreSQL. **Locked in `uv.lock`, not installed** (`langchain` extra; the `llm` and `storage` answers are `none` and `false`) (backend `langchain` extra). MIT ([PyPI](https://pypi.org/project/langgraph-checkpoint-postgres/3.2.1/)) |
| langsmith 0.14.17 | https://github.com/langchain-ai/langsmith-python | Tracing and test evaluation (installed through the backend dev group with its `pytest` extra; also in the `langchain` extra). MIT ([PyPI](https://pypi.org/project/langsmith/0.14.17/)) |
| agent-framework-anthropic 1.0.0b261112 | https://pypi.org/project/agent-framework-anthropic/ | Microsoft Agent Framework: Claude provider (beta). **Locked in `uv.lock`, not installed** (`maf` extra; the `llm` and `storage` answers are `none` and `false`) (backend `maf` extra). MIT ([PyPI](https://pypi.org/project/agent-framework-anthropic/1.0.0b261112/)) |
| agent-framework-core 1.26.0 | https://pypi.org/project/agent-framework-core/ | Microsoft Agent Framework core. **Locked in `uv.lock`, not installed** (`maf` extra; the `llm` and `storage` answers are `none` and `false`) (backend `maf` extra). MIT ([PyPI](https://pypi.org/project/agent-framework-core/1.26.0/)) |
| agent-framework-openai 1.18.2 | https://pypi.org/project/agent-framework-openai/ | Microsoft Agent Framework: OpenAI provider. **Locked in `uv.lock`, not installed** (`maf` extra; the `llm` and `storage` answers are `none` and `false`) (backend `maf` extra). MIT ([PyPI](https://pypi.org/project/agent-framework-openai/1.18.2/)) |
| msgspec 0.22.0 | https://msgspec.dev | Serialisation used by the Agent Framework. **Locked in `uv.lock`, not installed** (`maf` extra; the `llm` and `storage` answers are `none` and `false`) (backend `maf` extra). BSD-3-Clause ([PyPI](https://pypi.org/project/msgspec/0.22.0/)) |
| boto3 1.44.3 | https://docs.aws.amazon.com/boto3/latest/ | AWS S3 client. **Locked in `uv.lock`, not installed** (`storage` extra; the `llm` and `storage` answers are `none` and `false`) (backend `storage` extra). Apache-2.0 ([PyPI](https://pypi.org/project/boto3/1.44.3/)) |
| asgi-lifespan 2.1.0 | https://github.com/florimondmanca/asgi-lifespan | Runs the app's start-up and shut-down in tests (backend dev). MIT ([PyPI](https://pypi.org/project/asgi-lifespan/2.1.0/)) |
| import-linter 2.16 | https://import-linter.readthedocs.io/ | Checks the import rules between modules (backend dev). BSD-2-Clause (PyPI's licence field reads "BSD 2-Clause License") ([PyPI](https://pypi.org/project/import-linter/2.16/)) |
| mypy 2.4.1 | https://mypy.readthedocs.io/en/stable/index.html | Type checking (backend dev). MIT ([PyPI](https://pypi.org/project/mypy/2.4.1/)) |
| pytest 9.2.0 | https://docs.pytest.org/en/latest/ | Backend tests (backend dev). MIT ([PyPI](https://pypi.org/project/pytest/9.2.0/)) |
| pytest-recording 0.14.1 | https://github.com/kiwicom/pytest-recording | Replays recorded HTTP responses in tests (backend dev). MIT ([PyPI](https://pypi.org/project/pytest-recording/0.14.1/)) |
| pyyaml 6.0.3 | https://pyyaml.org/wiki/PyYAMLDocumentation | Reads YAML in tests and tools (backend dev). MIT ([PyPI](https://pypi.org/project/PyYAML/6.0.3/)) |
| ruff 0.17.5 | https://docs.astral.sh/ruff/ | Linting and formatting (backend dev). MIT ([PyPI](https://pypi.org/project/ruff/0.17.5/)) |
| testcontainers 4.15.0 | https://github.com/testcontainers/testcontainers-python | Starts a real PostgreSQL for the database tests (backend dev). Apache-2.0 ([PyPI](https://pypi.org/project/testcontainers/4.15.0/)) |
| types-boto3 1.43.118 | https://youtype.github.io/types_boto3_docs/ | Type stubs for boto3. Installed (backend dev group; `boto3` itself is in the `storage` extra and is not installed). MIT ([PyPI](https://pypi.org/project/types-boto3/1.43.118/)) |
| types-pyyaml 6.0.12.20261113 | https://github.com/python/typeshed | Type stubs for PyYAML (backend dev). Apache-2.0 ([PyPI](https://pypi.org/project/types-PyYAML/6.0.12.20261103/)) |
| vcrpy 9.4.2 | https://github.com/kevin1024/vcrpy | Records and replays HTTP for tests (backend dev). MIT ([PyPI](https://pypi.org/project/vcrpy/9.4.2/)) |
| @opentelemetry/api 1.9.1 | https://github.com/open-telemetry/opentelemetry-js/tree/main/api | OpenTelemetry API (frontend). Apache-2.0 ([npm](https://www.npmjs.com/package/@opentelemetry/api/v/1.9.1)) |
| @opentelemetry/api-logs 0.223.0 | https://github.com/open-telemetry/opentelemetry-js/tree/main/experimental/packages/api-logs | OpenTelemetry logs API (frontend). Apache-2.0 ([npm](https://www.npmjs.com/package/@opentelemetry/api-logs/v/0.223.0)) |
| @opentelemetry/instrumentation 0.223.0 | https://github.com/open-telemetry/opentelemetry-js/tree/main/experimental/packages/opentelemetry-instrumentation | OpenTelemetry instrumentation (frontend). Apache-2.0 ([npm](https://www.npmjs.com/package/@opentelemetry/instrumentation/v/0.223.0)) |
| @opentelemetry/resources 2.12.0 | https://github.com/open-telemetry/opentelemetry-js/tree/main/packages/opentelemetry-resources | OpenTelemetry resources (frontend). Apache-2.0 ([npm](https://www.npmjs.com/package/@opentelemetry/resources/v/2.12.0)) |
| @opentelemetry/sdk-logs 0.223.0 | https://github.com/open-telemetry/opentelemetry-js/tree/main/experimental/packages/sdk-logs | OpenTelemetry logs SDK (frontend). Apache-2.0 ([npm](https://www.npmjs.com/package/@opentelemetry/sdk-logs/v/0.223.0)) |
| @opentelemetry/sdk-metrics 2.12.0 | https://github.com/open-telemetry/opentelemetry-js/tree/main/packages/sdk-metrics | OpenTelemetry metrics SDK (frontend). Apache-2.0 ([npm](https://www.npmjs.com/package/@opentelemetry/sdk-metrics/v/2.12.0)) |
| @opentelemetry/sdk-trace-base 2.12.0 | https://github.com/open-telemetry/opentelemetry-js/tree/main/packages/opentelemetry-sdk-trace-base | OpenTelemetry tracing SDK (frontend). Apache-2.0 ([npm](https://www.npmjs.com/package/@opentelemetry/sdk-trace-base/v/2.12.0)) |
| @vercel/otel 2.3.0 | https://github.com/vercel/otel#readme | OpenTelemetry set-up for Next.js (frontend). MIT ([npm](https://www.npmjs.com/package/@vercel/otel/v/2.3.0)) |
| next 16.4.6 | https://nextjs.org | Frontend framework (frontend). MIT ([npm](https://www.npmjs.com/package/next/v/16.4.6)) |
| openapi-fetch 0.17.0 | https://openapi-ts.dev | Typed API client generated from the backend's OpenAPI (frontend). MIT ([npm](https://www.npmjs.com/package/openapi-fetch/v/0.17.0)) |
| react 19.3.1 | https://react.dev/ | UI library (frontend). MIT ([npm](https://www.npmjs.com/package/react/v/19.3.1)) |
| react-dom 19.3.1 | https://react.dev/ | React for the browser (frontend). MIT ([npm](https://www.npmjs.com/package/react-dom/v/19.3.1)) |
| server-only 0.0.1 | https://react.dev/reference/rsc/server-components | Keeps server code out of browser bundles (frontend). MIT ([npm](https://www.npmjs.com/package/server-only/v/0.0.1)) |
| @axe-core/playwright 4.14.0 | https://github.com/dequelabs/axe-core-npm#readme | Accessibility checks in end-to-end tests (frontend dev). MPL-2.0 ([npm](https://www.npmjs.com/package/@axe-core/playwright/v/4.14.0)) |
| @playwright/test 1.65.1 | https://playwright.dev | End-to-end tests (frontend dev). Apache-2.0 ([npm](https://www.npmjs.com/package/@playwright/test/v/1.65.1)) |
| @tailwindcss/turbopack 4.3.5 | https://tailwindcss.com | Tailwind support in the Turbopack build (frontend dev). MIT ([npm](https://www.npmjs.com/package/@tailwindcss/turbopack/v/4.3.5)) |
| @testing-library/jest-dom 7.0.1 | https://github.com/testing-library/jest-dom#readme | DOM assertions for unit tests (frontend dev). MIT ([npm](https://www.npmjs.com/package/@testing-library/jest-dom/v/7.0.1)) |
| @testing-library/react 16.3.3 | https://github.com/testing-library/react-testing-library#readme | React component tests (frontend dev). MIT ([npm](https://www.npmjs.com/package/@testing-library/react/v/16.3.3)) |
| @types/node 26.6.6 | https://github.com/DefinitelyTyped/DefinitelyTyped/tree/master/types/node | Node.js types (frontend dev). MIT ([npm](https://www.npmjs.com/package/@types/node/v/26.6.6)) |
| @types/react 19.3.0 | https://github.com/DefinitelyTyped/DefinitelyTyped/tree/master/types/react | React types (frontend dev). MIT ([npm](https://www.npmjs.com/package/@types/react/v/19.3.0)) |
| @types/react-dom 19.3.0 | https://github.com/DefinitelyTyped/DefinitelyTyped/tree/master/types/react-dom | React DOM types (frontend dev). MIT ([npm](https://www.npmjs.com/package/@types/react-dom/v/19.3.0)) |
| @vitejs/plugin-react 6.3.0 | https://github.com/vitejs/vite-plugin-react/tree/main/packages/plugin-react#readme | React support in Vitest (frontend dev). MIT ([npm](https://www.npmjs.com/package/@vitejs/plugin-react/v/6.3.0)) |
| eslint 9.39.5 | https://eslint.org | Linting (frontend dev). MIT ([npm](https://www.npmjs.com/package/eslint/v/9.39.5)) |
| eslint-config-next 16.4.6 | https://nextjs.org/docs/app/api-reference/config/eslint | Next.js lint rules (frontend dev). MIT ([npm](https://www.npmjs.com/package/eslint-config-next/v/16.4.6)) |
| jsdom 30.1.3 | https://github.com/jsdom/jsdom#readme | Browser-like DOM for unit tests (frontend dev). MIT ([npm](https://www.npmjs.com/package/jsdom/v/30.1.3)) |
| openapi-typescript 7.13.0 | https://openapi-ts.dev | Generates API types from the OpenAPI file (frontend dev). MIT ([npm](https://www.npmjs.com/package/openapi-typescript/v/7.13.0)) |
| prettier 3.10.1 | https://prettier.io | Formatting (frontend dev). MIT ([npm](https://www.npmjs.com/package/prettier/v/3.10.1)) |
| prettier-plugin-tailwindcss 0.8.1 | https://github.com/tailwindlabs/prettier-plugin-tailwindcss#readme | Sorts Tailwind class names (frontend dev). MIT ([npm](https://www.npmjs.com/package/prettier-plugin-tailwindcss/v/0.8.1)) |
| tailwindcss 4.3.5 | https://tailwindcss.com | CSS utility framework (frontend dev). MIT ([npm](https://www.npmjs.com/package/tailwindcss/v/4.3.5)) |
| typescript 5.9.3 | https://www.typescriptlang.org/ | Type checking (frontend dev). Apache-2.0 ([npm](https://www.npmjs.com/package/typescript/v/5.9.3)) |
| vitest 5.1.0 | https://vitest.dev | Unit test runner (frontend dev). MIT ([npm](https://www.npmjs.com/package/vitest/v/5.1.0)) |
| next-devtools-mcp 0.4.0 | https://github.com/vercel/next-devtools-mcp ([Next.js MCP guide](https://nextjs.org/docs/app/guides/mcp)) | Coding agents read the Next.js dev server's routes, logs and errors through `.mcp.json`. Runs through `npx` on developer machines only, outside the lockfile; pinned to 0.4.0 and checked in the weekly review of pinned MCP servers. MIT ([npm](https://www.npmjs.com/package/next-devtools-mcp/v/0.4.0)) |

Data sources and their terms are in [data sources](data-sources.md).
