# No Hardcoded Configuration Values

This is an OSS project. Users must be able to configure behavior via environment variables or config files — never by editing source code.

## What MUST be configurable

- **LLM model names** — never hardcode `claude-sonnet-4-6` or any model ID as the only option. Use `get_settings().llm_model` or `ANTHROPIC_MODEL_MAP` from gateway.py.
- **API URLs and ports** — never hardcode `localhost:8321` or any URL. Read from env vars (`PUBLIC_CB_API_BASE`, `API_PORT`).
- **File paths** — never hardcode absolute paths or domain-specific paths like `healthcare-claims`. Use `CB_OUTPUT_DIR` env var with generic fallback discovery.
- **LLM parameters** — temperature, max_tokens, timeouts come from `Settings` in `config.py`, not inline constants.
- **Numeric thresholds** — confidence thresholds, batch sizes, top-k values belong in `Settings` with env var backing.
- **Token limits** — context windows, reserve tokens belong in `config.py` or `token_utils.py` with env var overrides.

## Where configuration lives

| What | Where | How users change it |
|------|-------|-------------------|
| Python settings | `context_blocks/config.py` (Settings class) | `.env` file or env vars |
| Model ID mappings | `context_blocks/infrastructure/llm/gateway.py` (ANTHROPIC_MODEL_MAP, GEMINI_MODEL_MAP) | Extend the dict or use model ID directly |
| Viewer settings | `viewer/.env` | Copy from `viewer/.env.example` |
| Entity type definitions | `viewer/src/config/meta-model.yaml` | Edit YAML |

## How to add a new configurable value

1. Add a field to `Settings` in `config.py` with a sensible default
2. Document it in `.env.example`
3. Reference it via `get_settings().field_name` in source code
4. For viewer: use `import.meta.env.PUBLIC_*` for client-side, `process.env.*` for build-time

## Smell test

Before committing, check: "If a user clones this repo and runs it without editing any `.py` or `.ts` file, does everything work?" If not, the missing piece should be an env var or config file, not a code change.
