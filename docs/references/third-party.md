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
| WCAG 2.2 | https://www.w3.org/TR/WCAG22/ | Accessibility target (AA); contrast formulas used by `tools/check_contrast.py` |

Data sources and their terms are in [data sources](data-sources.md).
