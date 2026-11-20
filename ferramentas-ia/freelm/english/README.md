# freelm in English — complete, beginner-friendly guide

> **Independent explanatory translation and adaptation** for the Café com Dados & Gatos community, based on the [official freelm README](https://github.com/shihabshahrier/freelm) and the source material reviewed on November 20, 2026. This is **not official documentation** or an endorsement by the maintainers. Commands, API names and environment variables are preserved; explanations and prompts have been adapted to English.
>
> **Original project license:** MIT, © Shahriar Labs. See the [official repository](https://github.com/shihabshahrier/freelm) and [LICENSE](https://github.com/shihabshahrier/freelm/blob/main/LICENSE).
>
> **Test status:** some CLI and integration tests were completed on Ubuntu/WSL2 on November 20, 2026. The observed results are recorded at the end; an actual error-triggered failover has **not** been demonstrated.

## Table of contents

- [What is freelm?](#what-is-freelm)
- [Quick start without Python](#quick-start-without-python)
- [Obtaining and configuring free API keys](#obtaining-and-configuring-free-api-keys)
- [Main CLI commands](#main-cli-commands)
- [Using freelm with OpenAI-compatible tools](#using-freelm-with-openai-compatible-tools)
- [Free providers and their limitations](#free-providers-and-their-limitations)
- [How failover works](#how-failover-works)
- [Choosing models](#choosing-models)
- [Configuration options](#configuration-options)
- [Python and JavaScript examples](#python-and-javascript-examples)
- [Comparison with other tools](#comparison-with-other-tools)
- [FAQ and troubleshooting](#faq-and-troubleshooting)
- [Security, costs and limits](#security-costs-and-limits)
- [Sources and real test results](#sources-and-real-test-results)

## What is freelm?

**freelm** is a library and command-line tool (CLI) that combines **free usage allowances from multiple language-model providers**. A single call can select models offered through Gemini, Groq, OpenRouter, Cloudflare Workers AI, Z.ai, Cohere, Mistral, NVIDIA NIM, Kilo Gateway and other supported providers.

Instead of writing different integration code for every service, you can send requests through an OpenAI-compatible interface. According to its developer, freelm can:

- Discover currently available free models.
- Switch models, keys or providers when an attempt fails (**failover**).
- Account for request limits and free-tier quotas.
- Start a competing attempt when a provider responds too slowly.
- Run as a Python or JavaScript/TypeScript library, a CLI or an optional local `/v1` API.

**What freelm is NOT:** it is not an AI model, it does not automatically download large model weights, it does not perform model inference locally, and it does not provide unlimited free usage. **External providers** process your prompts.

**Key terminology:**
- **Provider:** the service that offers access to a model (for example, Groq).
- **Model:** the particular AI system that processes a request.
- **API key:** a secret credential used to access your account at a provider.
- **Routing:** deciding where each request should go.
- **Failover:** switching to another option when the first one cannot handle a request.
- **429:** an HTTP error indicating a rate limit was exceeded.
- **Endpoint:** an address other applications use to communicate with a service.

## Quick start without Python

This is the simplest path for our **Ubuntu/WSL2** lab. The JavaScript package requires **Node.js 20 or later**.

### Check Node.js

```bash
node --version
npm --version
```

These are standard Node.js/npm version-check commands, not freelm-specific commands.

### Try it without a key or a global installation

```bash
npx freelm chat "Hello! In one sentence, what is a language model?"
```

The official README documents `npx freelm chat "hello"`. With no keys configured, freelm reports that it may use anonymous public routes from Kilo Gateway and OVHcloud. **Their limits are low and these services may log prompts. Never send private or sensitive information.**

### Install locally, using the developer's documented method

```bash
mkdir -p ~/testes-freelm
cd ~/testes-freelm
npm install freelm
```

The README specifies `npm install freelm`. It does **not** present `npm install -g freelm` as its installation procedure. We therefore use `npx freelm` to run the locally installed CLI.

### Check commands and models

```bash
npx freelm --help
npx freelm models
npx freelm chat "Explain failover in one sentence." --model chat:fast --stream
```

## Obtaining and configuring free API keys

You do not need a personal API key to test anonymous routes, but keys are recommended for more predictable access and to test switching between **different providers**.

Official portals:
- **Gemini / Google AI Studio:** https://aistudio.google.com/apikey
- **Groq:** https://console.groq.com/keys
- **OpenRouter:** https://openrouter.ai/keys

**Before creating a key, confirm that your account has a free tier and check which models remain free.** Limits shown in the README may have changed.

### Set Gemini key in Ubuntu

Pause the screen recording first:

```bash
read -rsp "Gemini key: " GEMINI_API_KEY; echo
export GEMINI_API_KEY
```

### Set Groq key

```bash
read -rsp "Groq key: " GROQ_API_KEY; echo
export GROQ_API_KEY
```

### Set OpenRouter key

```bash
read -rsp "OpenRouter key: " OPENROUTER_API_KEY; echo
export OPENROUTER_API_KEY
```

`read -s` suppresses echo while entering a secret. Exported variables are available in the current shell and processes started from it. **Never commit keys to GitHub, include them in shared scripts or display them in a recording.**

### Check connections and models

```bash
npx freelm doctor
npx freelm models
npx freelm chat "Explain the difference between a provider and a model." --model chat:fast --stream
```

`doctor` makes a small real request to check each configured key. The original README shows both successful checks and authentication failures, including HTTP 401.

## Main CLI commands

| Command on Ubuntu with local installation | Purpose |
|---|---|
| `npx freelm chat "Hello"` | Ask a question in the terminal |
| `npx freelm chat "Hello" --model chat:fast --stream` | Prefer speed and stream the response |
| `npx freelm doctor` | Check keys and diagnose problems |
| `npx freelm doctor --json` | Request diagnostic output in JSON |
| `npx freelm models` | List available models |
| `npx freelm models --provider groq` | Filter models by provider |
| `npx freelm health` | Inspect key state in the process |
| `npx freelm serve` | Start the local API |
| `npx freelm serve --port 4000` | Specify the server port |

Using `npx` adapts the `freelm ...` commands in the README to a local package installation. See `npx freelm --help` for other options.

## Using freelm with OpenAI-compatible tools

Server mode is **optional**. It allows another application to use freelm through a local API.

On Ubuntu:

```bash
cd ~/testes-freelm
npx freelm serve
```

According to the project, the default address is:

```text
http://127.0.0.1:4000/v1
```

The general model alias is `auto`.

In **another terminal**, list models:

```bash
curl -s http://127.0.0.1:4000/v1/models
```

Send a request:

```bash
curl -s http://127.0.0.1:4000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Say: the local connection works."}]
  }'
```

### Integrations mentioned in the original README

| Tool | Configuration described by the project |
|---|---|
| **OpenAI SDK** | `base_url="http://127.0.0.1:4000/v1"` and `api_key="freelm"` (local example) |
| **LangChain** | `ChatOpenAI(base_url="http://127.0.0.1:4000/v1", api_key="freelm", model="auto")` |
| **LlamaIndex** | `OpenAILike(api_base="http://127.0.0.1:4000/v1", api_key="freelm", model="auto", is_chat_model=True)` |
| **Vercel AI SDK** | `createOpenAICompatible({ name: "freelm", baseURL: "http://127.0.0.1:4000/v1" })("auto")` |
| **Continue** | `openai` provider with the local `apiBase` and model `auto` |
| **Cline / Roo Code** | "OpenAI Compatible" provider, local base URL and model `auto` |
| **OpenCode** | `@ai-sdk/openai-compatible` provider pointing at the local base URL |
| **OpenClaw** | `models.providers.freelm`, `openai-completions` API and allow-listed `freelm/auto` |
| **Hermes Agent** | `hermes model` → custom endpoint; local base URL and model `auto` |
| **Aider** | `aider --openai-api-base http://127.0.0.1:4000/v1 --openai-api-key freelm --model openai/auto` |
| **Open WebUI** | Docker example at `http://host.docker.internal:4000/v1` |
| **n8n** | OpenAI credential with the local base URL |

**Documented compatibility is not proof of a successful test.** Not every free model offers enough context, tool calling, vision or coding capabilities for every application. The README notes that Hermes may require a long-context model. The older Roo Code is mentioned by the README; our actual editor test used **Zoo Code**, as documented in the results section.

### OpenCode configuration shown in the README

```json
{
  "provider": {
    "freelm": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "http://127.0.0.1:4000/v1"
      },
      "models": {
        "auto": {}
      }
    }
  }
}
```

This is a **configuration fragment**, not necessarily a full replacement for an existing configuration file.

### Docker (official alternative)

The developer also provides:

```bash
docker run --rm -p 4000:4000 -e GEMINI_API_KEY=... -e FREELM_SERVER_KEY=change-me ghcr.io/shihabshahrier/freelm
```

Those values are placeholders from the README, **not a ready-to-run command with real secrets**. Published Docker ports may expose the service beyond localhost; require proper authentication and network restrictions. **We did not need Docker for this lab.**

## Free providers and their limitations

This table summarizes the source material. **Plans, model availability and quotas can change: verify them with each provider.**

| Service | Environment variable | Developer's notes |
|---|---|---|
| Google AI Studio (Gemini) | `GEMINI_API_KEY` | Free tier with model-specific limits; Pro models may not have free quotas |
| Groq | `GROQ_API_KEY` | Free limits vary by model; do not confuse **Groq** and **Grok** |
| OpenRouter | `OPENROUTER_API_KEY` | Use routes ending in `:free` or `openrouter/free` |
| Cloudflare Workers AI (beta) | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | Free allowance measured in Neurons; token permissions matter |
| Z.ai / GLM (beta) | `ZAI_API_KEY` | Some Flash models are described as free; others may be paid |
| Cohere (beta) | `COHERE_API_KEY` | Trial keys; non-commercial-use restrictions |
| Kilo Gateway | `KILO_API_KEY` (optional) | Anonymous public routes exist, with low quotas and limits |
| OVHcloud AI Endpoints | None for anonymous routes | Low-limit anonymous fallback |
| Cerebras | `CEREBRAS_API_KEY` | README says it is no longer permanently free; trial credits/card may be required |
| Mistral | `MISTRAL_API_KEY` | "Experiment" plan with low limits |
| NVIDIA NIM | `NVIDIA_API_KEY` | Free build credits that can run out |

Some providers added in version 0.5.0 are marked **beta** because their live-key behavior had not all been verified at the time of the README. The author says built-in fallback model lists were checked again on **October 9, 2026**.

### Multiple keys for one provider

According to the README, you can separate keys with commas in a variable such as `GROQ_API_KEY` or use variables following `FREELM_<PROVIDER>_KEYS`. This does not remove limits or allow violations of provider policies.

### Keyless routes

The library documents:
- `keyless=True`: include anonymous routes as a last resort;
- `keyless="auto"`: use them when no keys are configured;
- `FREELM_KEYLESS=1|auto|0`: equivalent environment control.

## How failover works

Failover is intended to prevent a single provider error from making an entire request fail. According to the README:

| Situation | Described behavior |
|---|---|
| **429** — rate limit reached | Switch key, model or provider while respecting quotas |
| **401/402** — credential/authorization or billing issue | Disable the problematic key |
| **5xx** — provider-side failure | Backoff and circuit-breaker behavior |
| **Timeout / slow response** | Start a competing attempt after an adaptive delay |
| **404/410** — retired model | Temporarily bench that model |
| **Unsupported parameter** | Try another provider when appropriate |
| **Every route unavailable** | Return an explanatory error such as `NoProvidersAvailable` |

### Smart selection

The default `smart` strategy considers priorities and observed latency. Timing observations expire so routing does not rely indefinitely on old measurements. The competing-request mechanism (a **hedge**) may reduce delays when a provider stalls.

The original project describes approximately **3 seconds for a stalled stream and 6 seconds for a slow provider**, based on its own simulated benchmarks. **These are not guarantees in every environment.** See [the project's benchmarks](https://github.com/shihabshahrier/freelm/tree/main/benchmarks).

### How to prove failover in a video

Receiving a response alone does **not** prove failover. To demonstrate it, capture:
- which provider was attempted first;
- what error or delay occurred;
- which subsequent provider completed the request.

The README describes `attempt`, `hedge`, `success`, `error`, `wait` and `discovery` callback events in the library. It does **not** describe the CLI as a complete audit log for all attempts. If the CLI omits the relevant details, record that limitation or design a separate instrumented Node.js test.

## Choosing models

| Identifier | Meaning |
|---|---|
| `auto` or `chat` | Automatically choose a chat model |
| `chat:fast` | Prefer faster models |
| `chat:large` | Prefer larger models |
| `chat:small` | Prefer smaller models |
| `chat:tools` | Select models with tool-call capabilities |
| `vision` | Select vision-capable models |
| `reasoning` | Prefer reasoning models |
| `vendor/model-id` | Target a specific model |
| `["vendor/id", "chat:fast"]` | Specify an ordered fallback chain |

The README also mentions `prefer=[...]`, model/provider priorities and differences between ordinary and reasoning models. A very small `max_tokens` budget can result in empty responses from reasoning models; the project suggests **128 tokens or more** in those cases, or using `auto`.

## Configuration options

Options described in the original README for the library:

| Option | Default | Controls |
|---|---|---|
| `strategy` | `smart` | `smart`, `priority`, `round_robin`, `quota_aware` or `latency` |
| `hedge` | `True` | Competing attempts when a response is slow |
| `max_attempts` | `12` | Maximum attempts per request |
| `timeout` | `60` | Overall timeout in seconds |
| `wait` | `False` | Wait for quota instead of failing immediately |
| `max_wait` | `20` | Maximum wait in the example |
| `on_event` | Not configured | Routing event callback |
| `persist` | `False` | Preserve quota and cooldown state between runs |

Other listed options: `tier`, `priority`, `prefer`, `models`, `rpm`, `rpd`, `discover`, `free_only` and `cache_ttl`.

The README describes `FREELM_PERSIST=1` and a cache file at `~/.cache/freelm/state.json` with restricted file permissions and key hashes rather than raw keys. Verify exact behavior on the target runtime before enabling persistence.

**Warning:** do not disable `free_only` or enable paid tiers without understanding the provider's billing rules.

## Python and JavaScript examples

This section preserves the advanced concepts of the original reference. **The simple video installation does not require any of this code.**

### JavaScript / TypeScript

According to the README, the Node.js package has no runtime dependencies and supports `FreeLLM.fromEnv()`:

```javascript
import { FreeLLM } from "freelm";

const llm = FreeLLM.fromEnv();
console.log(await llm.text("Explain failover in one sentence."));

for await (const chunk of llm.stream("Count from one to five.", {
  signal: AbortSignal.timeout(30_000)
})) {
  process.stdout.write(chunk);
}
```

The original material reports ESM and CommonJS support in several JavaScript environments. See the [JavaScript documentation](https://github.com/shihabshahrier/freelm/tree/main/js).

### Python

The Python package requires **Python 3.9 or later**, with documented installation:

```bash
pip install freelm
```

Basic example:

```python
import freelm

llm = freelm.FreeLLM.from_env()
print(llm.text("Explain failover in one sentence."))
```

Explicit provider configuration, as shown by the developer:

```python
from freelm import FreeLLM, GoogleAIStudio, Groq, OpenRouter

llm = FreeLLM(
    [GoogleAIStudio("GEMINI-KEY"), Groq("GROQ-KEY"), OpenRouter("OPENROUTER-KEY")],
    strategy="smart",
)

response = llm.chat(
    [{"role": "user", "content": "Explain failover in one sentence."}],
    model="chat:fast",
)
print(response.text, "via", response.provider, response.model)
```

**The keys above are illustrative placeholders. Never include real secrets in shared source code.**

The README also shows:
- `llm.stream(...)` for incremental output;
- `llm.chat(..., tools=[...], tool_choice="auto")` and `r.tool_calls` for tool calling;
- `response_format={"type": "json_object"}` for JSON responses;
- `AsyncFreeLLM` and `astream(...)` for asynchronous use;
- `stream_chunks()` and `astream_chunks()` for OpenAI-compatible chunks.

### OpenAI SDK compatibility in Python

The project documents a replacement import:

```python
from freelm.compat import OpenAI

client = OpenAI()
r = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(r.choices[0].message.content)
```

According to the author, objects resemble OpenAI SDK responses, including `model_dump()` and streaming. **Actual compatibility depends on the installed version and the selected model's capabilities.**

## Comparison with other tools

**This table summarizes how freelm describes itself**, rather than an independent product benchmark.

| Tool/category | Difference described in the README |
|---|---|
| OmniRoute, 9Router, FreeLLMAPI, free-claude-code | Often self-hosted gateways; freelm can be used as a library alone |
| freellmpool | Another library/proxy; freelm highlights its dependency-free TypeScript package |
| LiteLLM | Broader scope, including paid services; freelm focuses on free tiers |
| any-llm, aisuite, llm | Unify provider APIs; freelm emphasizes quotas, switching and free-model discovery |
| OpenRouter | A hosted aggregator that can itself be one of freelm's provider pools |
| gpt4free | Reverse-engineered endpoints; freelm says it prioritizes official free tiers |
| LangChain / LlamaIndex | Orchestration frameworks that can use freelm via its server/API |

## FAQ and troubleshooting

### Is freelm really free?

The **library is open source and MIT-licensed**, but provider usage depends on your account and plan. The README describes protections around paid OpenRouter, Kilo and Z.ai models and warns that settings such as `tier="tier1"` or `free_only=False` can change billing behavior. Paid Cloudflare plans, Cohere production keys and other services may incur charges.

### Can freelm respond without an API key?

According to the developer, yes, using Kilo Gateway and OVHcloud anonymous routes. These can be unavailable, have lower quotas and **may log prompts**.

### Why did a free model stop working?

It might have been retired, your quota might be exhausted, your key may have expired, or the service might be down. The README says freelm attempts to reroute the request and temporarily benches removed or overloaded models.

### How do I avoid HTTP 429?

There is no legitimate way to eliminate provider quotas. The project proposes distributing calls across allowed keys and providers while respecting per-minute and per-day limits. Follow each provider's rules.

### Does a successful response prove failover?

No. It only shows that **some route responded**. Proving failover requires evidence that one attempt failed or stalled and another succeeded.

### Does freelm receive my prompts?

The project says requests go to the configured external providers and that freelm itself has no telemetry. This **does not eliminate processing, logging or retention policies at those providers**.

### What if the local API does not respond?

Check that `npx freelm serve` is still running, the correct terminal has the exported keys, and port 4000 is available. Do not make the service internet-accessible as a quick workaround.

### Can Windows use freelm running in WSL2?

With the Ubuntu server active, try this in PowerShell:

```powershell
curl.exe http://127.0.0.1:4000/v1/models
```

Localhost access is supported by WSL2 in compatible networking configurations. This depends on WSL networking mode and does not by itself make the server reachable from other devices.

### How do I stop or remove freelm?

Press **Ctrl+C** in the terminal running the server. To uninstall the local package:

```bash
cd ~/testes-freelm
npm uninstall freelm
```

### Where can I find specific error explanations?

The README links to the developer's [error reference](https://shahriarlabs.com/products/freelm/errors/), covering examples such as:
- Gemini 429 `RESOURCE_EXHAUSTED`;
- Gemini "User location is not supported";
- Gemini "API key not valid";
- Gemini 503;
- OpenRouter free-model quotas;
- OpenRouter endpoints that do not support tool use;
- Groq rate limits;
- Mistral 429;
- Z.ai 1302;
- Empty responses from reasoning models.

## Security, costs and limits

- **Never reveal API keys**, including in error logs.
- Anonymous endpoints and external providers are not appropriate places for private secrets.
- Before invoking a "free" model, verify your **account, the specific model and its billing terms**.
- Keep `freelm serve` available only locally. If exposing `--host 0.0.0.0`, configure `--api-key`, a firewall and appropriate security controls.
- When connecting coding agents, verify context size, tool-call support and the actual selected model's capabilities.
- Do not treat developer benchmarks as results independently reproduced by this guide.
- Do not treat `free_only` as a universal guarantee against charges on billing-enabled provider accounts.

## Sources and real test results

**Original material:** [freelm — official English README](https://github.com/shihabshahrier/freelm), reviewed on November 20, 2026.

**References:**
- [Original repository](https://github.com/shihabshahrier/freelm)
- [MIT license](https://github.com/shihabshahrier/freelm/blob/main/LICENSE)
- [JavaScript README](https://github.com/shihabshahrier/freelm/tree/main/js#readme)
- [Developer benchmarks](https://github.com/shihabshahrier/freelm/tree/main/benchmarks)
- [Developer error reference](https://shahriarlabs.com/products/freelm/errors/)
- [npm package](https://www.npmjs.com/package/freelm)
- [PyPI package](https://pypi.org/project/freelm/)

### Café com Dados & Gatos lab observations (November 20, 2026)

These observations come from screenshots of the user's **Ubuntu/WSL2** session, not from independent benchmarking.

| Test | Observed status |
|---|---|
| Node.js and npm | **Worked** — Node.js 22.23.2; npm 12.0.2 |
| freelm | **Worked** — version 0.5.2 via `npx` |
| Chat without an API key | **Worked** — a Kilo Gateway free model returned a Portuguese answer |
| Model discovery | **Worked** — several models listed by provider |
| `doctor` with configured keys | **Worked** — eventually 3 of 3 keys validated (Gemini, Groq, OpenRouter) |
| Anonymous routes | **Worked during diagnostics** — Kilo Gateway and OVHcloud |
| Local OpenAI-compatible API | **Worked** — server reported requests to `/v1/chat/completions` with HTTP 200 |
| Zoo Code integration | **Worked** — agent created an `index.html` Hello World page shown in VS Code |
| Different models used across requests | **Observed** — Nemotron and Gemini responses appeared in server logs |
| Error-triggered automatic failover | **Not demonstrated** — logs showed successful requests, not a failed first attempt |

**Attribution:** independent translation, reorganization and extra explanations to make the material accessible. Original freelm software and documentation: Shahriar Labs. Before public release, recheck commands, model availability, provider terms and the current upstream README.
