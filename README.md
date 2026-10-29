# codemode-eval

Eval harness for **sandboxed code-orchestration** agents (Cloudflare Code Mode
and similar "write code, don't call tools" patterns).

v0.1 quantifies the core claim: describing tools as JSON schemas grows linearly
with tool count, while a single code tool with on-demand search is a
near-constant baseline.

## Usage

```bash
python -m codemode_eval token-budget tools.json
# tools=2500 schema_dump_tokens=... codemode_tokens=1000 reduction=99.x%
```

## Roadmap

- Network-isolation probe (assert generated code cannot `fetch()`)
- Cross-model code-generation reliability benchmark

## License

MIT.
