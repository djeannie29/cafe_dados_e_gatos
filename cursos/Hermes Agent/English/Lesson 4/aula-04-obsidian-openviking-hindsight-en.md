# Lesson 04 — Obsidian with OpenViking and Hindsight in Hermes

## Lesson objective

Use the same Obsidian Vault as a knowledge base to compare OpenViking and Hindsight in Hermes.

By the end, it will be possible to:

- import the Vault content into OpenViking;
- import the same content into Hindsight;
- validate ingestion in both providers;
- test the `aluno` Profile with OpenViking;
- test the `lois` Profile with Hindsight;
- compare retrieval using exactly the same base.

## Prerequisites

- Hermes Agent working.
- `aluno` Profile configured with OpenViking.
- `lois` Profile configured with Hindsight.
- OpenViking already configured in Lesson 3.
- Hindsight already configured in the `lois` Profile.
- Obsidian installed.
- An existing Obsidian Vault with Markdown files.

## Core concept

Obsidian organizes Markdown files in the Vault. OpenViking and Hindsight do not automatically know this content just because the Vault exists.

In this lesson, the Vault is already ready. The goal is only to integrate the existing folder with both providers.

In the environment used in the recording, Obsidian is on Windows and Hermes is on WSL2. The Vault is located at:

```text
K:\Onedrive\material estudo\machine_learning
```

In WSL2, the same directory is accessed through:

```text
/mnt/k/Onedrive/material estudo/machine_learning
```

---

# OpenViking

## Start the local OpenViking server

Open a terminal:

```bash
openviking-server
```

Keep this terminal open throughout the entire OpenViking section.

In another terminal, check the server health:

```bash
curl http://127.0.0.1:1933/health
```

Expected result:

```text
{"status":"ok","healthy":true,...}
```

Do not start a second instance of `openviking-server` while the first one is active.

---

## Validate the OpenViking client

In the second terminal:

```bash
ov config validate
```

The expected result is:

```text
Config file   valid
Server        reachable
Auth          accepted
Health        healthy
```

If the client configuration does not exist yet or needs to be redone:

```bash
ov config
```

Then repeat:

```bash
ov config validate
```

In the local environment used in the lesson, the server used by the CLI is:

```text
http://127.0.0.1:1933
```

---

## Confirm the VLM before ingestion

Before importing the Vault:

```bash
ov observer models
```

In this lesson, the VLM used by OpenViking is Codex with the Terra model.

This command is used to check the active generation model. The local embedding configured in `ov.conf` does not need to appear in this listing.

---

## Check OpenViking in Hermes

Check the `aluno` Profile:

```bash
hermes -p aluno memory status
```

The active provider should be:

```text
openviking
```

---

## Import the Vault into OpenViking

Run:

```bash
ov add-resource "/mnt/k/Onedrive/material estudo/machine_learning" \
  --to viking://resources/machine-learning-vault
```

In this recording, the Vault is imported only once, with Codex + Terra already configured from the beginning.

---

## Monitor processing

During ingestion, in another terminal:

```bash
ov observer queue
```

The `Semantic-Nodes` queue may show items in `Pending` and `In Progress` during semantic processing of the content.

Before continuing, wait for:

```text
Pending      0
In Progress  0
Errors       0
```

It is also possible to check the models again:

```bash
ov observer models
```

Do not restart the server while processing is in progress.

---

## Confirm the import in OpenViking

Display the tree:

```bash
ov tree viking://resources/machine-learning-vault
```

Display the overview:

```bash
ov overview viking://resources/machine-learning-vault
```


If the overview is not available yet, first check:

```bash
ov observer queue
```

and wait for semantic processing to finish before concluding that there was a failure.

---

## Test searches directly in OpenViking

Direct search:

```bash
ov find "What is the difference between AI and Machine Learning?" \
  --uri viking://resources/machine-learning-vault
```

Search relating concepts:

```bash
ov find "What is the relationship between overfitting, validation, and regularization?" \
  --uri viking://resources/machine-learning-vault
```

If the results return Vault content, ingestion is working.

---

## Test through Hermes with OpenViking

Open:

```bash
hermes -p aluno chat
```

Ask:

```text
What is the difference between AI and Machine Learning?
```

Then:

```text
Why are KNN and K-Means sensitive to scale, even though they solve different problems?
```

Then:

```text
Relate overfitting, validation, and regularization.
```


---



# Hindsight

## Important update before continuing

Before importing the Vault, it is worth noting an important change compared with Lesson 3.

On **September 24, 2026**, Hindsight stopped being treated as an internal Hermes provider and began being distributed through the Hermes **plugin catalog**.

During this transition, there was a known limitation in `local_embedded` mode in installations managed by the Hermes package manager.

On **September 29, 2026**, the Hermes catalog was updated again to a newer version of Hindsight, indicating that embedded mode was working again in this type of installation.

Because of this, depending on the exact Hermes version and the Hindsight plugin version installed on the machine, behavior may differ from what was shown earlier in the course.

In this recording, to start from a clean and current plugin installation in the `lois` Profile, Hindsight will be removed and installed again from the official Hermes catalog.

---

## Remove Hindsight from the `lois` Profile

Run:

```bash
hermes -p lois plugins remove hindsight
```

After the command confirms that the plugin was removed and that the provider was reset, proceed directly to reinstallation.

---

## Install Hindsight again from the official catalog

Run:

```bash
hermes -p lois plugins install hindsight
```

If the installer asks whether you want to enable the plugin in the Profile, answer:

```text
y
```

If it asks whether Hermes should prepare dependencies through the package manager, answer:

```text
y
```

Then validate:

```bash
hermes -p lois memory status
```

If the plugin appears installed, but the status shows:

```text
Provider: (none - built-in only)
```

this means the plugin was installed correctly, but it has not yet been selected as the active provider for the `lois` Profile.

Activate it manually:

```bash
hermes -p lois config set memory.provider hindsight
```

Then check again:

```bash
hermes -p lois memory status
```

The expected result is:

```text
Provider: hindsight
Plugin: installed ✓
Status: available ✓
hindsight ← active
```

---

## How Hindsight will be used in this lesson

In this lesson, Hindsight will be used in `local_external` mode.

This means there are two separate pieces:

1. the local Hindsight server, running at `http://127.0.0.1:8888`;
2. the `hindsight` CLI, used to import the Vault and run `recall` / `reflect`.

The Hermes plugin only connects the `lois` Profile to the Hindsight server. Installing the Hermes plugin **does not automatically install the `hindsight` CLI in the PATH**.

---


## Check whether the Hindsight server is active

Test:

```bash
curl -sS http://127.0.0.1:8888/health
```

If the command hangs without returning a response, stop it with `Ctrl+C` and prepare the local server again with:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

If the server exits on startup with a CUDA error on an older NVIDIA GPU, add the two settings to the `~/.hindsight/server.env` file:

```bash
cat >> ~/.hindsight/server.env <<'EOF'
HINDSIGHT_API_EMBEDDINGS_LOCAL_FORCE_CPU=1
HINDSIGHT_API_RERANKER_LOCAL_FORCE_CPU=1
EOF
```

Check the file:

```bash
cat ~/.hindsight/server.env
```

Then load the file again and start the server:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

And test again:

```bash
curl -sS http://127.0.0.1:8888/health
```

Expected result:

```json
{"status":"healthy","database":"connected",...}
```

If the port is still not active, load the configuration and start the server:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

On the first startup, wait a few seconds before testing `/health`.

If necessary, check:

```bash
tail -n 100 ~/.hindsight/daemon.log
```

---

## Install the Hindsight CLI

The CLI is separate from the `hindsight-api` server and is also separate from the Hermes plugin.

Check first:

```bash
hindsight --help
```

If this appears:

```text
hindsight: command not found
```

install the official CLI:

```bash
curl -fsSL https://hindsight.vectorize.io/get-cli | bash
```

Then reload the shell:

```bash
source ~/.bashrc
```

And confirm:

```bash
hindsight --help
```

---

## Configure the CLI for the local server

After the Hindsight server is active and the health check responds correctly, point the `hindsight` CLI to that server.

For the current terminal session:

```bash
export HINDSIGHT_API_URL=http://localhost:8888
```

It is also possible to save the URL using the CLI itself:

```bash
hindsight configure --api-url http://127.0.0.1:8888
```

---

## Connect the `lois` Profile to Hindsight

With the server active and the CLI already pointing to it, activate Hindsight as the provider for the `lois` Profile:

```bash
hermes -p lois config set memory.provider hindsight
```

Validate:

```bash
hermes -p lois memory status
```

The expected result is:

```text
Provider: hindsight
Plugin: installed ✓
Status: available ✓
hindsight ← active
```

This way, the `hindsight` CLI and the `lois` Profile start using the same Hindsight server at `127.0.0.1:8888`.

---

---

## Import the Vault into Hindsight

Using the default `bank_id`:

```bash
hindsight bank create hermes

```

Creating the bank before import is necessary because `retain-files` writes the files inside an existing bank. If the bank does not exist yet, the CLI returns `404: Bank 'hermes' not found`.

Then import the Vault:

```bash
hindsight memory retain-files hermes "/mnt/k/Onedrive/material estudo/machine_learning/"
```

The `retain-files` command accepts directories and processes files recursively.

This command depends on the `hindsight` CLI being installed and configured for `http://127.0.0.1:8888`.

Hindsight converts the files into documents and extracts memories from the content.

---

## Confirm the import in Hindsight

Perform a direct retrieval:

```bash
hindsight memory recall hermes "What is the difference between AI and Machine Learning?"
```

Test a relationship between concepts:

```bash
hindsight memory recall hermes "What is the relationship between overfitting, validation, and regularization?"
```

Test a synthesis:

```bash
hindsight memory reflect hermes "Create a map relating AI, Machine Learning, Neural Networks, Deep Learning, and Transformers."
```

If Vault content appears in the results, ingestion is working.

---

## Test through Hermes with Hindsight

Open:

```bash
hermes -p lois chat
```

Repeat the same questions used in the `aluno` Profile:

```text
What is the difference between AI and Machine Learning?
```

```text
Why are KNN and K-Means sensitive to scale, even though they solve different problems?
```

```text
Relate overfitting, validation, and regularization.
```

---

# Questions to compare the two providers

## Direct retrieval

```text
What is the difference between AI and Machine Learning?
```

```text
What characterizes a regression problem?
```

```text
What is the role of k in KNN?
```

```text
What does the bias do in an artificial neuron?
```

```text
What does an epoch mean in neural network training?
```

## Relationships between concepts

```text
Why does data preparation affect the quality of a model's evaluation?
```

```text
What is the relationship between overfitting, validation, and regularization?
```

```text
Why are KNN and K-Means sensitive to scale, even though they solve different problems?
```

```text
How does the concept of generalization appear in both regression and neural networks?
```

```text
What is the relationship between the decision threshold and precision/recall?
```

## Comparisons

```text
Compare regression and classification.
```

```text
Compare bagging and boosting.
```

```text
Compare K-Means and DBSCAN.
```

```text
Compare RNN, LSTM/GRU, and Transformer.
```

```text
Compare MAE and RMSE and say in which situation one may be preferable to the other.
```

## Questions that require care

```text
Does R² of 0.90 mean 90% correct predictions?
```

```text
Does 99% accuracy guarantee that a classifier is excellent?
```

```text
Does PCA with 95% explained variance guarantee 95% accuracy?
```

```text
Is a cluster discovered by the algorithm automatically a real profile?
```

```text
Does a regression coefficient prove causality?
```

## Long synthesis

```text
Describe a complete Machine Learning pipeline, from data preparation to evaluation.
```

```text
Explain how a model can achieve excellent training results and fail in production.
```

```text
Create a map relating AI → Machine Learning → Neural Networks → Deep Learning → Transformers.
```

```text
Explain why the best model depends on the problem, the metric, and the cost of errors.
```

```text
Which concepts appear repeatedly throughout the topics?
```

---

## Delete an imported Vault from OpenViking

If you want to remove a Vault already imported into OpenViking, use:

```bash
ov rm -r viking://resources/machine-learning-vault
```

Then, if you want to confirm that it was removed:

```bash
ov tree viking://resources
```

Replace `machine-learning-vault` with the name of the resource you want to delete.

---


# Important difference

## Obsidian

Obsidian organizes Markdown files for human reading and editing.

## OpenViking

OpenViking imports files as resources inside a `viking://` hierarchy and allows structured search, reading, and navigation.

## Hindsight

Hindsight imports files as documents and extracts memories that can be retrieved and related by the memory mechanism.

Having a file inside the Vault does not mean it is already available in either provider.

Always perform ingestion before testing.

---

# Official sources

Hermes Agent — Memory Providers:

https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers

OpenViking — Resource Management:

https://docs.openviking.ai/en/api/02-resources

OpenViking — Quick Start:

https://docs.openviking.ai/en/getting-started/02-quickstart

OpenViking — CLI Setup:

https://docs.openviking.ai/en/getting-started/05-cli-setup

OpenViking — Configuration Guide (VLM, timeout, retries, and concurrency):

https://github.com/volcengine/OpenViking/blob/main/docs/en/guides/01-configuration.md

Hindsight — CLI Reference:

https://github.com/vectorize-io/hindsight/blob/main/skills/hindsight-docs/references/sdks/cli.md

Hindsight — Retain Files:

https://github.com/vectorize-io/hindsight/blob/main/skills/hindsight-docs/references/developer/api/retain.md


OpenViking — recent discussion about client configuration:

https://github.com/volcengine/OpenViking/issues/3650

OpenViking — recent discussion about `ov.conf` and `ovcli.conf`:

https://github.com/volcengine/OpenViking/issues/3125


Hindsight — integration with Hermes:

https://github.com/NousResearch/hermes-agent/blob/main/plugins/memory/hindsight/README.md



---

# If Hindsight has problems after a Hermes update

> Use this section only if the Profile continues pointing to `hindsight`, but the local embedded mode stops being available or enters an update loop. In the environment used for this lesson, the solution was to run Hindsight as an external local server and make the `lois` Profile point to it.

## 1. Confirm the Profile status

```bash
hermes -p lois memory status
```

If the plugin is installed, but Hindsight is not available in local embedded mode, follow the steps below.

## 2. Prepare external local Hindsight

The server will run locally at:

```text
http://127.0.0.1:8888
```

Create the configuration folder:

```bash
mkdir -p ~/.hindsight
umask 077
```

Register the MiniMax key without displaying it on screen:

```bash
read -s -p "Paste the NEW MiniMax key: " MM_KEY
echo
```

Create the environment file using MiniMax-M3:

```bash
cat > ~/.hindsight/server.env <<EOF
HINDSIGHT_API_LLM_PROVIDER=minimax
HINDSIGHT_API_LLM_MODEL=MiniMax-M3
HINDSIGHT_API_LLM_API_KEY=$MM_KEY
EOF
unset MM_KEY
chmod 600 ~/.hindsight/server.env
```

Check only the provider and model, without showing the key:

```bash
grep -E 'HINDSIGHT_API_LLM_PROVIDER|HINDSIGHT_API_LLM_MODEL' ~/.hindsight/server.env
```

Expected result:

```text
HINDSIGHT_API_LLM_PROVIDER=minimax
HINDSIGHT_API_LLM_MODEL=MiniMax-M3
```

## 3. Start the Hindsight server

First, check whether port 8888 is already in use:

```bash
ss -ltnp | grep 8888
```

If there is no process on the port, load the environment and start:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

On first startup, Hindsight may take a few seconds to load the local models and embedded PostgreSQL.

Test:

```bash
curl -sS http://127.0.0.1:8888/health
```

Expected result:

```json
{"status":"healthy","database":"connected",...}
```

If the test is run too early and fails, check the log:

```bash
tail -n 100 ~/.hindsight/daemon.log
```

Look for:

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8888
```

## 4. Switch the `lois` Profile to `local_external`

Back up the configuration:

```bash
cp ~/.hermes/profiles/lois/hindsight/config.json ~/.hermes/profiles/lois/hindsight/config.json.bak
```

Change only the mode and URL:

```bash
python3 - <<'PY'
import json
from pathlib import Path

p = Path.home() / ".hermes/profiles/lois/hindsight/config.json"
data = json.loads(p.read_text())

data["mode"] = "local_external"
data["api_url"] = "http://127.0.0.1:8888"

p.write_text(json.dumps(data, indent=2) + "\n")

print("mode:", data["mode"])
print("api_url:", data["api_url"])
PY
```

Expected result:

```text
mode: local_external
api_url: http://127.0.0.1:8888
```

## 5. Validate in Hermes

```bash
hermes -p lois memory status
```

The correct result should show:

```text
Provider: hindsight
Plugin: installed ✓
Status: available ✓
hindsight ← active
```

From this point on, Hermes uses local Hindsight through the API at `127.0.0.1:8888`, without depending on `local_embedded` mode.

> Security: never place the MiniMax key directly in documentation, GitHub, screenshots, or video. If a key is accidentally displayed, revoke it and generate another one.
