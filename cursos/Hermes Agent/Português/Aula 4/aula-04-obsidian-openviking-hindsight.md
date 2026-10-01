# Aula 04 — Obsidian com OpenViking e Hindsight no Hermes

## Objetivo da aula

Usar o mesmo Vault do Obsidian como base de conhecimento para comparar o OpenViking e o Hindsight no Hermes.

Ao final, será possível:

- importar o conteúdo do Vault para o OpenViking;
- importar o mesmo conteúdo para o Hindsight;
- validar a ingestão nos dois provedores;
- testar o Profile `aluno` com OpenViking;
- testar o Profile `lois` com Hindsight;
- comparar a recuperação usando exatamente a mesma base.

## Pré-requisitos

- Hermes Agent funcionando.
- Profile `aluno` configurado com OpenViking.
- Profile `lois` configurado com Hindsight.
- OpenViking já configurado na Aula 3.
- Hindsight já configurado no Profile `lois`.
- Obsidian instalado.
- Um Vault do Obsidian já existente com arquivos Markdown.

## Conceito central

O Obsidian organiza os arquivos Markdown no Vault. OpenViking e Hindsight não passam a conhecer esse conteúdo automaticamente apenas porque o Vault existe.

Nesta aula, o Vault já está pronto. O objetivo é somente integrar a pasta existente aos dois provedores.

No ambiente usado na gravação, o Obsidian está no Windows e o Hermes está no WSL2. O Vault está em:

```text
K:\Onedrive\material estudo\machine_learning
```

No WSL2, o mesmo diretório é acessado por:

```text
/mnt/k/Onedrive/material estudo/machine_learning
```

---

# OpenViking

## Iniciar o servidor local do OpenViking

Abrir um terminal:

```bash
openviking-server
```

Manter esse terminal aberto durante toda a parte do OpenViking.

Em outro terminal, conferir a saúde do servidor:

```bash
curl http://127.0.0.1:1933/health
```

Resultado esperado:

```text
{"status":"ok","healthy":true,...}
```

Não iniciar uma segunda instância do `openviking-server` enquanto a primeira estiver ativa.

---

## Validar o cliente OpenViking

No segundo terminal:

```bash
ov config validate
```

O esperado é:

```text
Config file   valid
Server        reachable
Auth          accepted
Health        healthy
```

Se a configuração do cliente ainda não existir ou precisar ser refeita:

```bash
ov config
```

Depois repetir:

```bash
ov config validate
```

No ambiente local da aula, o servidor usado pelo CLI é:

```text
http://127.0.0.1:1933
```

---

## Confirmar o VLM antes da ingestão

Antes de importar o Vault:

```bash
ov observer models
```

Nesta aula, o VLM usado pelo OpenViking é o Codex com o modelo Terra.

Esse comando é usado para conferir o modelo de geração ativo. O embedding local configurado no `ov.conf` não precisa aparecer nessa listagem.

---

## Conferir o OpenViking no Hermes

Conferir o Profile `aluno`:

```bash
hermes -p aluno memory status
```

O provider ativo deve ser:

```text
openviking
```

---

## Importar o Vault para o OpenViking

Executar:

```bash
ov add-resource "/mnt/k/Onedrive/material estudo/machine_learning" \
  --to viking://resources/machine-learning-vault
```

Nesta gravação o Vault é importado uma única vez, já com Codex + Terra configurado desde o início.

---

## Acompanhar o processamento

Durante a ingestão, em outro terminal:

```bash
ov observer queue
```

A fila `Semantic-Nodes` pode mostrar itens em `Pending` e `In Progress` durante o processamento semântico do conteúdo.

Antes de seguir, aguardar:

```text
Pending      0
In Progress  0
Errors       0
```

Também é possível conferir novamente os modelos:

```bash
ov observer models
```

Não reiniciar o servidor enquanto houver processamento em andamento.

---

## Confirmar a importação no OpenViking

Exibir a árvore:

```bash
ov tree viking://resources/machine-learning-vault
```

Exibir o overview:

```bash
ov overview viking://resources/machine-learning-vault
```


Se o overview ainda não estiver disponível, conferir primeiro:

```bash
ov observer queue
```

e aguardar o término do processamento semântico antes de concluir que houve falha.

---

## Testar buscas diretamente no OpenViking

Busca direta:

```bash
ov find "Qual é a diferença entre IA e Machine Learning?" \
  --uri viking://resources/machine-learning-vault
```

Busca relacionando conceitos:

```bash
ov find "Qual é a relação entre overfitting, validação e regularização?" \
  --uri viking://resources/machine-learning-vault
```

Se os resultados retornarem conteúdo do Vault, a ingestão está funcionando.

---

## Testar pelo Hermes com OpenViking

Abrir:

```bash
hermes -p aluno chat
```

Perguntar:

```text
Qual é a diferença entre IA e Machine Learning?
```

Depois:

```text
Por que KNN e K-Means são sensíveis à escala, embora resolvam problemas diferentes?
```

Depois:

```text
Relacione overfitting, validação e regularização.
```


---



# Hindsight

## Atualização importante antes de continuar

Antes de importar o Vault, vale registrar uma mudança importante em relação à Aula 3.

Em **24 de setembro de 2026**, o Hindsight deixou de ser tratado como provider interno do Hermes e passou a ser distribuído pelo **plugin catalog** do Hermes.

Durante essa transição, houve uma limitação conhecida do modo `local_embedded` em instalações gerenciadas pelo package manager do Hermes.

Em **29 de setembro de 2026**, o catálogo do Hermes foi atualizado novamente para uma versão mais nova do Hindsight, com a indicação de que o modo embutido voltou a funcionar nesse tipo de instalação.

Por isso, dependendo da versão exata do Hermes e do plugin Hindsight instalada na máquina, o comportamento pode ser diferente do mostrado anteriormente no curso.

Nesta gravação, para partir de uma instalação limpa e atual do plugin no Profile `lois`, o Hindsight será removido e instalado novamente a partir do catálogo oficial do Hermes.

---

## Remover o Hindsight do Profile `lois`

Executar:

```bash
hermes -p lois plugins remove hindsight
```

Depois que o comando confirmar que o plugin foi removido e que o provider foi resetado, seguir diretamente para a reinstalação.

---

## Instalar novamente o Hindsight a partir do catálogo oficial

Executar:

```bash
hermes -p lois plugins install hindsight
```

Se o instalador perguntar se deseja habilitar o plugin no Profile, responder:

```text
y
```

Se perguntar se o Hermes deve preparar as dependências pelo package manager, responder:

```text
y
```

Depois validar:

```bash
hermes -p lois memory status
```

Se o plugin aparecer instalado, mas o status mostrar:

```text
Provider: (none - built-in only)
```

isso significa que o plugin foi instalado corretamente, mas ainda não foi selecionado como provider ativo do Profile `lois`.

Ativar manualmente:

```bash
hermes -p lois config set memory.provider hindsight
```

Depois conferir novamente:

```bash
hermes -p lois memory status
```

O esperado é:

```text
Provider: hindsight
Plugin: installed ✓
Status: available ✓
hindsight ← active
```

---

## Como o Hindsight será usado nesta aula

Nesta aula, o Hindsight será usado em modo `local_external`.

Isso significa que existem duas peças separadas:

1. o servidor local do Hindsight, executado em `http://127.0.0.1:8888`;
2. o CLI `hindsight`, usado para importar o Vault e executar `recall` / `reflect`.

O plugin do Hermes apenas conecta o Profile `lois` ao servidor Hindsight. Instalar o plugin do Hermes **não instala automaticamente o CLI `hindsight` no PATH**.

---


## Conferir se o servidor Hindsight está ativo

Testar:

```bash
curl -sS http://127.0.0.1:8888/health
```

Se o comando ficar travado sem retornar resposta, interromper com `Ctrl+C` e preparar novamente o servidor local com:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

Se o servidor encerrar na inicialização com erro de CUDA em GPU NVIDIA antiga, adicionar as duas configurações ao arquivo `~/.hindsight/server.env`:

```bash
cat >> ~/.hindsight/server.env <<'EOF'
HINDSIGHT_API_EMBEDDINGS_LOCAL_FORCE_CPU=1
HINDSIGHT_API_RERANKER_LOCAL_FORCE_CPU=1
EOF
```

Conferir o arquivo:

```bash
cat ~/.hindsight/server.env
```

Depois carregar novamente o arquivo e iniciar o servidor:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

E testar novamente:

```bash
curl -sS http://127.0.0.1:8888/health
```

Resultado esperado:

```json
{"status":"healthy","database":"connected",...}
```

Se a porta ainda não estiver ativa, carregar a configuração e iniciar o servidor:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

Na primeira inicialização, aguardar alguns segundos antes de testar o `/health`.

Se necessário, conferir:

```bash
tail -n 100 ~/.hindsight/daemon.log
```

---

## Instalar o CLI do Hindsight

O CLI é separado do servidor `hindsight-api` e também é separado do plugin do Hermes.

Verificar primeiro:

```bash
hindsight --help
```

Se aparecer:

```text
hindsight: command not found
```

instalar o CLI oficial:

```bash
curl -fsSL https://hindsight.vectorize.io/get-cli | bash
```

Depois recarregar o shell:

```bash
source ~/.bashrc
```

E confirmar:

```bash
hindsight --help
```

---

## Configurar o CLI para o servidor local

Depois que o servidor Hindsight estiver ativo e o teste de saúde responder corretamente, apontar o CLI `hindsight` para esse servidor.

Para a sessão atual do terminal:

```bash
export HINDSIGHT_API_URL=http://localhost:8888
```

Também é possível gravar a URL usando o próprio CLI:

```bash
hindsight configure --api-url http://127.0.0.1:8888
```

---

## Conectar o Profile `lois` ao Hindsight

Com o servidor ativo e o CLI já apontando para ele, ativar o Hindsight como provider do Profile `lois`:

```bash
hermes -p lois config set memory.provider hindsight
```

Validar:

```bash
hermes -p lois memory status
```

O esperado é:

```text
Provider: hindsight
Plugin: installed ✓
Status: available ✓
hindsight ← active
```

Assim, o CLI `hindsight` e o Profile `lois` passam a usar o mesmo servidor Hindsight em `127.0.0.1:8888`.

---

---

## Importar o Vault para o Hindsight

Usando o `bank_id` padrão:

```bash
hindsight bank create hermes

```

Criar o bank antes da importação é necessário porque o `retain-files` grava os arquivos dentro de um bank existente. Se o bank ainda não existir, o CLI retorna `404: Bank 'hermes' not found`.

Depois importar o Vault:

```bash
hindsight memory retain-files hermes "/mnt/k/Onedrive/material estudo/machine_learning/"
```

O comando `retain-files` aceita diretórios e processa os arquivos recursivamente.

Esse comando depende do CLI `hindsight` estar instalado e configurado para `http://127.0.0.1:8888`.

O Hindsight converte os arquivos em documentos e extrai memórias a partir do conteúdo.

---

## Confirmar a importação no Hindsight

Fazer uma recuperação direta:

```bash
hindsight memory recall hermes "Qual é a diferença entre IA e Machine Learning?"
```

Testar uma relação entre conceitos:

```bash
hindsight memory recall hermes "Qual é a relação entre overfitting, validação e regularização?"
```

Testar uma síntese:

```bash
hindsight memory reflect hermes "Monte um mapa relacionando IA, Machine Learning, Redes Neurais, Deep Learning e Transformers."
```

Se o conteúdo do Vault aparecer nos resultados, a ingestão está funcionando.

---

## Testar pelo Hermes com Hindsight

Abrir:

```bash
hermes -p lois chat
```

Repetir as mesmas perguntas usadas no Profile `aluno`:

```text
Qual é a diferença entre IA e Machine Learning?
```

```text
Por que KNN e K-Means são sensíveis à escala, embora resolvam problemas diferentes?
```

```text
Relacione overfitting, validação e regularização.
```

---

# Perguntas para comparar os dois provedores

## Recuperação direta

```text
Qual é a diferença entre IA e Machine Learning?
```

```text
O que caracteriza um problema de regressão?
```

```text
Qual é o papel de k no KNN?
```

```text
O que o bias faz em um neurônio artificial?
```

```text
O que significa uma época no treinamento de redes neurais?
```

## Relações entre conceitos

```text
Por que a preparação dos dados interfere na qualidade da avaliação de um modelo?
```

```text
Qual é a relação entre overfitting, validação e regularização?
```

```text
Por que KNN e K-Means são sensíveis à escala, embora resolvam problemas diferentes?
```

```text
Como o conceito de generalização aparece tanto em regressão quanto em redes neurais?
```

```text
Qual é a relação entre limiar de decisão e precisão/recall?
```

## Comparações

```text
Compare regressão e classificação.
```

```text
Compare bagging e boosting.
```

```text
Compare K-Means e DBSCAN.
```

```text
Compare RNN, LSTM/GRU e Transformer.
```

```text
Compare MAE e RMSE e diga em que situação um pode ser preferível ao outro.
```

## Perguntas que exigem cuidado

```text
R² de 0,90 significa 90% de previsões corretas?
```

```text
Uma acurácia de 99% garante que um classificador é excelente?
```

```text
PCA com 95% de variância explicada garante 95% de acurácia?
```

```text
Um cluster descoberto pelo algoritmo é automaticamente um perfil real?
```

```text
Um coeficiente de regressão prova causalidade?
```

## Síntese longa

```text
Descreva um pipeline completo de Machine Learning, da preparação dos dados à avaliação.
```

```text
Explique como um modelo pode ter ótimo resultado no treino e falhar em produção.
```

```text
Monte um mapa relacionando IA → Machine Learning → Redes Neurais → Deep Learning → Transformers.
```

```text
Explique por que o melhor modelo depende do problema, da métrica e do custo dos erros.
```

```text
Quais conceitos aparecem repetidamente ao longo dos temas?
```

---

## Apagar um Vault importado do OpenViking

Caso queira remover um Vault já importado do OpenViking, use:

```bash
ov rm -r viking://resources/machine-learning-vault
```

Depois, se quiser confirmar que ele foi removido:

```bash
ov tree viking://resources
```

Substitua `machine-learning-vault` pelo nome do recurso que deseja apagar.

---


# Diferença importante

## Obsidian

O Obsidian organiza os arquivos Markdown para leitura e edição humana.

## OpenViking

O OpenViking importa os arquivos como recursos dentro de uma hierarquia `viking://` e permite busca, leitura e navegação estruturada.

## Hindsight

O Hindsight importa arquivos como documentos e extrai memórias que podem ser recuperadas e relacionadas pelo mecanismo de memória.

Ter um arquivo dentro do Vault não significa que ele já está disponível em nenhum dos dois provedores.

Sempre executar a ingestão antes dos testes.

---

# Fontes oficiais

Hermes Agent — Memory Providers:

https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers

OpenViking — Resource Management:

https://docs.openviking.ai/en/api/02-resources

OpenViking — Quick Start:

https://docs.openviking.ai/en/getting-started/02-quickstart

OpenViking — CLI Setup:

https://docs.openviking.ai/en/getting-started/05-cli-setup

OpenViking — Configuration Guide (VLM, timeout, retries e concorrência):

https://github.com/volcengine/OpenViking/blob/main/docs/en/guides/01-configuration.md

Hindsight — CLI Reference:

https://github.com/vectorize-io/hindsight/blob/main/skills/hindsight-docs/references/sdks/cli.md

Hindsight — Retain Files:

https://github.com/vectorize-io/hindsight/blob/main/skills/hindsight-docs/references/developer/api/retain.md


OpenViking — discussão recente sobre configuração do cliente:

https://github.com/volcengine/OpenViking/issues/3650

OpenViking — discussão recente sobre `ov.conf` e `ovcli.conf`:

https://github.com/volcengine/OpenViking/issues/3125


Hindsight — integração com Hermes:

https://github.com/NousResearch/hermes-agent/blob/main/plugins/memory/hindsight/README.md



---

# Se o Hindsight der problema após atualização do Hermes

> Use esta seção apenas se o Profile continuar apontando para `hindsight`, mas o modo local embutido deixar de ficar disponível ou entrar em ciclo de atualização. No ambiente desta aula, a solução foi executar o Hindsight como servidor local externo e fazer o Profile `lois` apontar para ele.

## 1. Confirmar o estado do Profile

```bash
hermes -p lois memory status
```

Se o plugin estiver instalado, mas o Hindsight não estiver disponível no modo local embutido, siga os passos abaixo.

## 2. Preparar o Hindsight local externo

O servidor será executado localmente em:

```text
http://127.0.0.1:8888
```

Criar a pasta de configuração:

```bash
mkdir -p ~/.hindsight
umask 077
```

Cadastrar a chave da MiniMax sem exibi-la na tela:

```bash
read -s -p "Cole a NOVA chave MiniMax: " MM_KEY
echo
```

Criar o arquivo de ambiente usando MiniMax-M3:

```bash
cat > ~/.hindsight/server.env <<EOF
HINDSIGHT_API_LLM_PROVIDER=minimax
HINDSIGHT_API_LLM_MODEL=MiniMax-M3
HINDSIGHT_API_LLM_API_KEY=$MM_KEY
EOF
unset MM_KEY
chmod 600 ~/.hindsight/server.env
```

Conferir apenas provider e modelo, sem mostrar a chave:

```bash
grep -E 'HINDSIGHT_API_LLM_PROVIDER|HINDSIGHT_API_LLM_MODEL' ~/.hindsight/server.env
```

Resultado esperado:

```text
HINDSIGHT_API_LLM_PROVIDER=minimax
HINDSIGHT_API_LLM_MODEL=MiniMax-M3
```

## 3. Subir o servidor Hindsight

Antes, conferir se a porta 8888 já está sendo usada:

```bash
ss -ltnp | grep 8888
```

Se não houver nenhum processo na porta, carregar o ambiente e iniciar:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

Na primeira inicialização, o Hindsight pode levar alguns segundos para carregar os modelos locais e o PostgreSQL embutido.

Testar:

```bash
curl -sS http://127.0.0.1:8888/health
```

Resultado esperado:

```json
{"status":"healthy","database":"connected",...}
```

Se o teste for executado cedo demais e falhar, conferir o log:

```bash
tail -n 100 ~/.hindsight/daemon.log
```

Procure por:

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8888
```

## 4. Trocar o Profile `lois` para `local_external`

Fazer backup da configuração:

```bash
cp ~/.hermes/profiles/lois/hindsight/config.json ~/.hermes/profiles/lois/hindsight/config.json.bak
```

Alterar apenas o modo e a URL:

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

Resultado esperado:

```text
mode: local_external
api_url: http://127.0.0.1:8888
```

## 5. Validar no Hermes

```bash
hermes -p lois memory status
```

O resultado correto deve mostrar:

```text
Provider: hindsight
Plugin: installed ✓
Status: available ✓
hindsight ← active
```

A partir desse ponto, o Hermes usa o Hindsight local pela API em `127.0.0.1:8888`, sem depender do modo `local_embedded`.

> Segurança: nunca coloque a chave da MiniMax diretamente em documentação, GitHub, print ou vídeo. Se uma chave for exibida acidentalmente, revogue-a e gere outra.
