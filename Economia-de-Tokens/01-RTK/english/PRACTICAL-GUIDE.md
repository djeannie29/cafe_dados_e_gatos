# RTK in Ubuntu/WSL2 — Practical Guide and Lab Results

**Café com Dados & Gatos · Token Savings Series · Episode 01 · November 2026**

This guide documents a practical experiment using RTK (Rust Token Killer) with **Codex CLI (GPT-6.1 Sol, Medium reasoning)** and **Claude Code (MiniMax M3.1 Flash)**. Each coding agent was asked to build the same four-page demonstration website twice: once without RTK and once with RTK.

**Important:** One run per condition means these findings are exploratory. A reported percentage from `rtk gain` reflects compression of selected **command outputs**, not the percentage of tokens saved across an entire agent session or a confirmed reduction in costs.

## Official references

- [RTK repository](https://github.com/rtk-ai/rtk)
- [RTK installation](https://www.rtk-ai.app/docs/getting-started/installation/)
- [Supported agents](https://www.rtk-ai.app/docs/getting-started/supported-agents/)
- [RTK gain analytics](https://www.rtk-ai.app/docs/analytics/gain/)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [VS Code + WSL](https://code.visualstudio.com/docs/remote/wsl)
- [Codex CLI](https://github.com/openai/codex)
- [Claude Code installation](https://docs.anthropic.com/en/docs/claude-code/getting-started)
- [MiniMax / Claude Code integration](https://platform.minimax.io/docs/m-plan/claude-code)

## Environment and experimental design

| Component | Configuration |
|---|---|
| Operating system | Ubuntu under WSL2 (exact Ubuntu release not consolidated) |
| Editor | VS Code connected to WSL |
| RTK | 1.2.1 |
| Codex CLI | 0.170.0; GPT-6.1 Sol, Medium |
| Claude Code | MiniMax M3.1 Flash via MiniMax (exact Claude Code version not consolidated) |
| Project | "Cafeteria Aurora": a four-page institutional website |
| Stack | Vite + React + TypeScript, no backend |
| Comparison | One run without RTK and one with RTK for each agent |

Use separate directories and new agent sessions. Keep the prompt, model, permissions, acceptance criteria and tooling stable **within each agent pair**. Do not interpret a Codex-versus-Claude difference as a model benchmark.

## Prepare VS Code and Ubuntu/WSL2

In VS Code on Windows, install Microsoft's **WSL** extension, then use the Command Palette (`F1`) and select **WSL: Connect to WSL**.

In the Ubuntu terminal:

```bash
mkdir -p ~/testes-economia-tokens
cd ~/testes-economia-tokens
code .
```

Check the remote indicator and the integrated terminal:

```bash
uname -s
pwd
cat /etc/os-release
code --version
codex --version
claude --version
command -v rtk
```

`uname -s` should print `Linux`. Working inside `$HOME` rather than `/mnt/c` is recommended. Native Ubuntu users can open VS Code directly from Linux and do not need the WSL extension.

## Install RTK

Check the current official installation instructions. Download and **inspect** the installer before executing it:

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh -o /tmp/rtk-install.sh
less /tmp/rtk-install.sh
```

If the script matches the official instructions:

```bash
sh /tmp/rtk-install.sh
export PATH="$HOME/.local/bin:$PATH"
rtk --version
rtk gain
```

Do not assume `rtk gain` is a whole-session usage counter.

## Install Codex CLI and Claude Code, if necessary

The Codex CLI's official installer was one documented option:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
codex --version
command -v codex
```

An alternative is `npm install -g @openai/codex`; choose **one** installation method. For Claude Code, the video used Anthropic's native installer:

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
command -v claude
```

An alternative is `npm install -g @anthropic-ai/claude-code`. Avoid `sudo npm install -g` and do not upgrade agents halfway through an A/B comparison.

For Claude Code with MiniMax M Plan / Token Plan, use MiniMax's configuration helper when applicable:

```bash
npx -y mmx-cli@latest agent setup
```

Choose Claude Code, set the proper MiniMax subscription key and endpoint/region, and restart the agent. **Never publish API keys or subscription keys**. The M Plan key is different from an ordinary prepaid API key.

## Execute the four runs

Before sending the main task, record the relevant status counters; record them again at the end. Perform hook verification *before* the baseline snapshot.

### A — Codex without RTK

```bash
mkdir -p ~/testes-economia-tokens/rtk/codex-sem-rtk
cd ~/testes-economia-tokens/rtk/codex-sem-rtk
codex
```

Inside Codex, run `/status`, send the **complete website brief below**, inspect the result/build/tests and then run `/status` again. Confirm no RTK hooks were configured for this project.

### B — Codex with a project-local RTK hook

```bash
mkdir -p ~/testes-economia-tokens/rtk/codex-com-rtk
cd ~/testes-economia-tokens/rtk/codex-com-rtk
rtk init --codex --dry-run
```

Inspect the preview. If it is correct:

```bash
rtk init --codex
cat .codex/hooks.json
codex
```

The expected hook is `PreToolUse` on `Bash`, calling `rtk hook codex`. During the recorded experiment, a Codex-requested `ls -la .codex` reached Bash as `rtk ls -la .codex`, demonstrating actual rewriting **for that command**. Repeat the same prompt, take initial/final `/status` snapshots and record errors. Outside Codex:

```bash
rtk gain
```

### C — Claude Code without RTK

```bash
mkdir -p ~/testes-economia-tokens/rtk/claude-sem-rtk
cd ~/testes-economia-tokens/rtk/claude-sem-rtk
rtk init --show
claude
```

Check there is no RTK hook in the global or local Claude settings. Select MiniMax M3.1 Flash. Use `/usage` before and after the unchanged website prompt. Keep track of input/output, cache reads/writes, requests, times and intervention.

### D — Claude Code with a **local** RTK hook

Avoid `rtk init -g` during these tests, because a global hook may interfere with the control.

```bash
mkdir -p ~/testes-economia-tokens/rtk/claude-com-rtk
cd ~/testes-economia-tokens/rtk/claude-com-rtk
rtk init
```

Plain `rtk init` alone does **not** install the automatic Claude hook. In a **new empty directory**, create the local hook:

```bash
mkdir -p .claude
if [ -e .claude/settings.local.json ]; then
  echo "Existing settings: inspect and merge them; do not overwrite."
else
  cat > .claude/settings.local.json <<'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "rtk hook claude"
          }
        ]
      }
    ]
  }
}
EOF
fi
python3 -m json.tool .claude/settings.local.json >/dev/null
rtk rewrite 'git status'
```

Open `claude` and inspect `/hooks`: it should show `PreToolUse` with local `rtk hook claude`. A menu entry is not proof that every command is intercepted. Test it first. Preserve RTK analytics if needed before resetting them:

```bash
mkdir -p ~/testes-economia-tokens/rtk/backups
rtk gain --all --format json > ~/testes-economia-tokens/rtk/backups/rtk-gain-before-claude.json
rtk gain --reset
rtk gain
```

Resetting the RTK **statistics** does not uninstall RTK or the hook. Do not reset a report you still need without exporting it first. Start a fresh Claude session in the same project, record the initial `/usage`, run the identical prompt, record final `/usage` and then `rtk gain` in the shell.

## Complete benchmark prompt — Cafeteria Aurora

**Use the exact same text in all four runs of a repeated experiment.**

> Build from scratch a four-page institutional website, without a backend, using Vite + React + TypeScript. Include a header and footer, functional navigation, responsive layout, basic accessibility, three offer cards, two calls to action, and a contact page with a validated form and local-only feedback. Create four pages: Home, About, Services/Products and Contact. The fictional company is "Cafeteria Aurora", an artisanal café offering specialty coffee, homemade sweets and a comfortable city-center break. Use a cohesive visual identity; the pages must be complete rather than placeholders. Add a README with installation, development and build commands. Run the build and report which checks succeeded and which did not. Do not add a backend, database or real data submission.

> **Reproducibility note:** this English-language rendering is for readers. The recorded video used a Portuguese-language briefing. For a strict replication, keep the chosen prompt language **unchanged** between all four conditions.

## Results — session totals after subtracting initial baseline

The screenshots display **raw end counters**, which are not necessarily the token usage of the website task. For the comparisons below, deduct the initial baseline. K/M abbreviations mean estimates are rounded.

### Codex / GPT-6.1 Sol Medium

| Metric | No RTK | With RTK | Change |
|---|---:|---:|---:|
| Initial `used` | ~4,270 | ~4,310 | — |
| Final `used` | 65,734 | 69,336 | — |
| **Task-only `used`** | **~61,464** | **~65,026** | **+5.8%** |
| Task-only uncached input | ~48,582 | ~51,990 | +7.0% |
| Task-only output | ~12,882 | ~13,036 | +1.2% |
| Estimated task cache read | ~856,156 | ~817,796 | −4.5% |

Codex's `used` counter is **uncached input + output**; the `in` status-line value includes cached input. See the [Codex implementation](https://github.com/openai/codex/blob/main/codex-rs/tui/src/token_usage.rs). The initial `used` values were rounded on screen, hence the approximate task totals.

**RTK report:** 1 command, 33 → 10 estimated output tokens, **23 saved (69.7%) locally**. This did **not** produce a reduction in task-only `used`: the test with RTK had ~3,562 additional tokens (+5.8%).

### Claude Code / MiniMax M3.1 Flash

| Metric | No RTK | With RTK | Change |
|---|---:|---:|---:|
| Task-only input | ~66,600 | 73,700 | +10.7% |
| Task-only output | ~30,118 | 25,500 | −15.3% |
| **Task-only input + output** | **~96,718** | **99,200** | **+2.6%** |
| Cache read displayed at end* | ~2.5 M | ~1.6 M | ~−36% |
| Requests | 76 | 62 | −18.4% |
| UI-recorded duration | 12m10s | 10m49s | −1m21s |

The no-RTK session initially displayed ~12,900 input and 82 output, before the task. With RTK, input/output started at zero. ***Cache values here are final UI readings; an equivalent initial cache baseline was not demonstrably deducted.** Therefore the ~36% cache difference is indicative, not an audited task-only delta.

**RTK report:** 17 commands, 747 → 406 estimated output tokens, **341 saved (45.6%) locally**. The with-RTK site looked simpler; the run involved a pause/resumption. These observations do **not** prove RTK caused lower quality or interruptions. The UI-recorded duration is not necessarily the full human/recording time.

## Hypothetical API pricing — not actual billing

Rates used for this educational estimate (USD per 1 million tokens):

| Model | Uncached input | Output | Cache read |
|---|---:|---:|---:|
| GPT-6.1 Sol | $2.00 | $10.00 | $0.10 |
| MiniMax M3.1 Flash | $0.15 | $0.60 | $0.015 |

Sources: [OpenAI model pricing](https://developers.openai.com/api/docs/models/gpt-6.1-sol); [MiniMax model pricing](https://www.minimax.io/blog/minimax-m31f). Rates may change; check current official pages.

Assuming the three token categories in the recorded counters are billed **separately**:

```text
estimated USD = (uncached_input * input_rate
               + output * output_rate
               + cache_read * cache_rate) / 1_000_000
```

| Simulated result | No RTK | With RTK | Estimated difference |
|---|---:|---:|---:|
| Codex, baseline deducted | ~$0.3116 | ~$0.3161 | **+1.5%** |
| Claude Code, approximate final cache | ~$0.0656 | ~$0.0504 | **−23.2%** |

The Claude estimate is **conditional** on approximate end-of-session cache readings, rather than verified task-only cache data. These are *not* Codex/Claude subscription charges or actual MiniMax invoices. Cache writes, other billable tools, long-context rules and other pricing factors are excluded. **A session can use more tokens but cost less if its mix of output and cached tokens changes.**

## Hook warning and troubleshooting

- The Claude Code run showed `No hook installed` in RTK even though Claude’s `/hooks` menu displayed a project-local `PreToolUse / Bash / rtk hook claude` hook. [RTK issue #2024](https://github.com/rtk-ai/rtk/issues/2024) describes a similar global-versus-local detection symptom. This is a **plausible hypothesis**, not a confirmed diagnosis of this run.
- An earlier preparation attempt reported `API Error: The response stream was malformed` through the MiniMax external gateway; do not assume it happened in every final test.
- The external gateway can display an Auto safety-check warning; confirm approval behavior manually.
- Running `rtk init --global --dry-run` does not install the global hook.
- Never overwrite an existing `.claude/settings.local.json`; merge only the specific hook after inspection.
- For cleanup, inspect the local project configurations. In Codex, preview `rtk init --codex --uninstall --dry-run` before applying the uninstall if supported by the installed RTK version. For Claude, remove **only the RTK hook** from the local settings, preserving unrelated settings.

## Conclusion

RTK compressed output in the commands it recorded, **but task-only uncached input + output was larger** in both A/B comparisons. The Codex API-cost simulation rose slightly; the Claude Code simulation fell **under its stated assumptions**, while the generated website appeared visually simpler. With one run per condition, none of these differences proves causality. Repeat runs, capture **initial and final cache counters**, and validate build/tests and visual quality before drawing broad conclusions.

The presentation PDF for this episode is intentionally **Portuguese-only** and will be placed in the **episode root**, not in a translated-language folder.
