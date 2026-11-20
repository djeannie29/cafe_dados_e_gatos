# freelm em português (Brasil) — guia completo e acessível

> **Tradução explicativa independente**, preparada para a comunidade Café com Dados & Gatos a partir do [README oficial do freelm](https://github.com/shihabshahrier/freelm) e do material disponibilizado em 20/11/2026. Não é documentação oficial nem endosso do mantenedor. Comandos, nomes de variáveis e APIs foram preservados; explicações e exemplos foram adaptados ao português. **Parte dos testes de CLI e integração já foi executada no Ubuntu/WSL2 em 20/11/2026; os resultados reais estão registrados ao final. O failover provocado por falha ainda não foi demonstrado.**
>
> **Licença do projeto original:** MIT, © Shahriar Labs. Fonte e licença: [repositório oficial](https://github.com/shihabshahrier/freelm) · [LICENSE](https://github.com/shihabshahrier/freelm/blob/main/LICENSE).

## Índice

- [O que é o freelm](#o-que-é-o-freelm)
- [Comece aqui: sem Python](#comece-aqui-sem-python)
- [Como obter e configurar chaves gratuitas](#como-obter-e-configurar-chaves-gratuitas)
- [Comandos principais da CLI](#comandos-principais-da-cli)
- [Utilizar em ferramentas compatíveis com OpenAI](#utilizar-em-ferramentas-compatíveis-com-openai)
- [Provedores gratuitos e restrições](#provedores-gratuitos-e-restrições)
- [Como funciona o failover](#como-funciona-o-failover)
- [Como escolher modelos](#como-escolher-modelos)
- [Opções de configuração](#opções-de-configuração)
- [Exemplos com Python e JavaScript](#exemplos-com-python-e-javascript)
- [Comparação com outras ferramentas](#comparação-com-outras-ferramentas)
- [Perguntas frequentes e problemas comuns](#perguntas-frequentes-e-problemas-comuns)
- [Segurança, custos e limites](#segurança-custos-e-limites)
- [Fontes e estado dos testes](#fontes-e-estado-dos-testes)

## O que é o freelm

O **freelm** é uma biblioteca e ferramenta de linha de comando (CLI) que combina **cotas gratuitas de diferentes serviços de modelos de linguagem**. Uma única chamada pode selecionar modelos do Gemini, Groq, OpenRouter, Cloudflare Workers AI, Z.ai, Cohere, Mistral, NVIDIA NIM, Kilo Gateway ou outros provedores suportados.

Em vez de manter um código separado para cada serviço, o freelm oferece um modo de chamar modelos usando uma interface compatível com OpenAI. Segundo o autor, a biblioteca:

- Descobre modelos gratuitos disponíveis no momento.
- Alterna para outro modelo, chave ou provedor quando uma chamada falha (*failover*).
- Considera limites de requisições e cotas das chaves.
- Pode iniciar uma segunda tentativa quando um provedor está demorando demais.
- Funciona em Python, JavaScript/TypeScript e, opcionalmente, como API local `/v1`.

**O que ele NÃO é:** não é um modelo de IA, não baixa automaticamente pesos de modelos grandes, não faz inferência local e não garante uso gratuito ilimitado. O processamento da pergunta acontece nos **provedores externos** escolhidos.

**Explicação dos termos:**
- **Provedor:** empresa ou serviço que disponibiliza acesso ao modelo (por exemplo, Groq).
- **Modelo:** IA específica que recebe a pergunta.
- **Chave de API:** credencial secreta que autoriza o acesso à conta no provedor.
- **Roteamento:** escolha de onde enviar cada solicitação.
- **Failover:** troca para outra opção quando a primeira não funciona.
- **429:** resposta de limite de requisições excedido.
- **Endpoint:** endereço de rede pelo qual outro programa conversa com o serviço.

## Comece aqui: sem Python

Este é o caminho mais simples para o nosso laboratório no **Ubuntu/WSL2**. O pacote Node.js requer **Node 20 ou superior**.

### Conferir Node.js

```bash
node --version
npm --version
```

Esses são comandos do ecossistema Node.js para consultar versões; não são comandos específicos do freelm.

### Experimentar sem chave, sem instalação global

```bash
npx freelm chat "Olá! Responda em português: o que é um modelo de linguagem?"
```

O README oficial documenta o uso de `npx freelm chat "hello"`. O projeto afirma conseguir recorrer a rotas públicas anônimas do Kilo Gateway e OVHcloud quando não há chaves. **Limites são baixos e os serviços podem registrar as perguntas. Nunca use dados pessoais ou sigilosos nesse teste.**

### Instalar o pacote localmente, como documentado pelo autor

```bash
mkdir -p ~/testes-freelm
cd ~/testes-freelm
npm install freelm
```

**Atenção à distinção:** o README especifica `npm install freelm`; não apresenta `npm install -g freelm` como caminho de instalação. Por isso usamos `npx freelm` para executar os comandos em uma instalação local.

### Consultar os comandos

```bash
npx freelm --help
npx freelm models
npx freelm chat "Explique o que significa failover em uma frase." --model chat:fast --stream
```

## Como obter e configurar chaves gratuitas

Uma chave própria não é obrigatória para experimentar a rota pública anônima, mas é recomendada para uso mais previsível e para testar a troca entre **provedores distintos**.

Links oficiais:
- **Gemini / Google AI Studio:** https://aistudio.google.com/apikey
- **Groq:** https://console.groq.com/keys
- **OpenRouter:** https://openrouter.ai/keys

**Antes de gerar uma chave, verifique se sua conta está no plano gratuito e quais modelos são gratuitos naquele momento.** Os limites informados pelo README podem ter mudado.

### Configurar Gemini no terminal Ubuntu

Com a gravação pausada:

```bash
read -rsp "Chave Gemini: " GEMINI_API_KEY; echo
export GEMINI_API_KEY
```

### Configurar Groq

```bash
read -rsp "Chave Groq: " GROQ_API_KEY; echo
export GROQ_API_KEY
```

### Configurar OpenRouter

```bash
read -rsp "Chave OpenRouter: " OPENROUTER_API_KEY; echo
export OPENROUTER_API_KEY
```

A entrada com `read -s` evita ecoar a chave enquanto é digitada. As variáveis exportadas valem para a sessão atual e os processos iniciados por ela. **Não coloque chaves no GitHub, em scripts compartilhados ou na gravação.**

### Verificar conexão e modelos

```bash
npx freelm doctor
npx freelm models
npx freelm chat "Explique a diferença entre provedor e modelo." --model chat:fast --stream
```

O comando `doctor` realiza uma pequena chamada real para verificar as chaves; o exemplo do README mostra mensagens de sucesso e falha, inclusive erro 401 para chaves inválidas.

## Comandos principais da CLI

| Comando no Ubuntu com instalação local | Para que serve |
|---|---|
| `npx freelm chat "Olá"` | Perguntar pelo terminal |
| `npx freelm chat "Olá" --model chat:fast --stream` | Pedir modelo orientado à velocidade, exibindo resposta em fluxo |
| `npx freelm doctor` | Verificar chaves e diagnosticar problemas |
| `npx freelm doctor --json` | Solicitar resultado do diagnóstico em JSON |
| `npx freelm models` | Consultar modelos disponíveis |
| `npx freelm models --provider groq` | Filtrar modelos por provedor |
| `npx freelm health` | Consultar estado de chaves no processo |
| `npx freelm serve` | Iniciar API local |
| `npx freelm serve --port 4000` | Informar porta do serviço |

As formas com `npx` adaptam ao pacote local os comandos `freelm ...` apresentados no README. Para mais detalhes sobre parâmetros, consulte `npx freelm --help`.

## Utilizar em ferramentas compatíveis com OpenAI

O modo servidor é **opcional**. Ele é útil quando um aplicativo externo precisa consumir a API do freelm.

No Ubuntu:

```bash
cd ~/testes-freelm
npx freelm serve
```

Segundo o autor, o endereço padrão é:

```text
http://127.0.0.1:4000/v1
```

O identificador geral do modelo é `auto`.

Em **outro terminal**, consultar modelos:

```bash
curl -s http://127.0.0.1:4000/v1/models
```

Enviar uma pergunta:

```bash
curl -s http://127.0.0.1:4000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Diga em português: conexão funcionando."}]
  }'
```

### Exemplos de integração citados no README

| Ferramenta | Configuração descrita pelo projeto |
|---|---|
| **OpenAI SDK** | `base_url="http://127.0.0.1:4000/v1"` e `api_key="freelm"` (exemplo local) |
| **LangChain** | `ChatOpenAI(base_url="http://127.0.0.1:4000/v1", api_key="freelm", model="auto")` |
| **LlamaIndex** | `OpenAILike(api_base="http://127.0.0.1:4000/v1", api_key="freelm", model="auto", is_chat_model=True)` |
| **Vercel AI SDK** | `createOpenAICompatible({ name: "freelm", baseURL: "http://127.0.0.1:4000/v1" })("auto")` |
| **Continue** | Provedor `openai`, `apiBase` local e modelo `auto` |
| **Cline / Roo Code** | Provedor “OpenAI Compatible”, URL local e modelo `auto` |
| **OpenCode** | Provedor `@ai-sdk/openai-compatible` apontando para URL local |
| **OpenClaw** | `models.providers.freelm`, API `openai-completions` e modelo `freelm/auto` autorizado |
| **Hermes Agent** | `hermes model` → endpoint personalizado; URL local e modelo `auto` |
| **Aider** | `aider --openai-api-base http://127.0.0.1:4000/v1 --openai-api-key freelm --model openai/auto` |
| **Open WebUI** | Em Docker, exemplo do autor com `http://host.docker.internal:4000/v1` |
| **n8n** | Credencial OpenAI com URL-base do serviço |

**Compatibilidade declarada não equivale a teste realizado.** Nem todos os modelos gratuitos têm janela de contexto, chamadas de ferramentas, visão ou capacidade de programação adequadas à aplicação. O README alerta, por exemplo, que o Hermes pode precisar de um modelo de contexto longo.

### Configuração publicada no README para OpenCode

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

Isso é um **trecho de configuração**, não necessariamente um arquivo completo para substituir as demais configurações do usuário.

### Docker (alternativa oficial)

O autor também apresenta:

```bash
docker run --rm -p 4000:4000 -e GEMINI_API_KEY=... -e FREELM_SERVER_KEY=change-me ghcr.io/shihabshahrier/freelm
```

Os valores acima são marcadores ilustrativos do README, **não comandos prontos para executar com segredos reais**. Em Docker, a publicação da porta pode disponibilizar o serviço além do localhost; proteger a API com chave e regras de rede. Para este laboratório, preferimos **não usar Docker**.

## Provedores gratuitos e restrições

A tabela resume o material original. **Planos, modelos e cotas estão sujeitos a mudanças; confirmar no painel do provedor.**

| Serviço | Variável de ambiente | Observação do autor |
|---|---|---|
| Google AI Studio (Gemini) | `GEMINI_API_KEY` | Plano gratuito com limites específicos por modelo; modelos Pro podem não ter cota gratuita |
| Groq | `GROQ_API_KEY` | Plano gratuito com limites por modelo; não confundir **Groq** com **Grok** |
| OpenRouter | `OPENROUTER_API_KEY` | Utilizar rotas identificadas como `:free` ou `openrouter/free` |
| Cloudflare Workers AI (beta) | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | Cota grátis medida em Neurons; verificar permissões do token |
| Z.ai / GLM (beta) | `ZAI_API_KEY` | Alguns modelos Flash são citados como gratuitos; demais podem ser pagos |
| Cohere (beta) | `COHERE_API_KEY` | Chaves de teste; restrições de uso não comercial |
| Kilo Gateway | `KILO_API_KEY` (opcional) | Há rotas públicas sem chave, com cotas e limites |
| OVHcloud AI Endpoints | Nenhuma na rota anônima | Rota anônima de contingência com limites baixos |
| Cerebras | `CEREBRAS_API_KEY` | Segundo o README, não é mais permanentemente gratuito; pode exigir cartão/créditos experimentais |
| Mistral | `MISTRAL_API_KEY` | Plano Experiment; limites baixos |
| NVIDIA NIM | `NVIDIA_API_KEY` | Créditos gratuitos de teste, sujeitos a esgotamento |

O autor identifica como **beta** alguns provedores adicionados na versão 0.5.0, ainda sem verificação real completa das chaves na data da documentação. Segundo o texto original, listas internas de modelos de fallback foram reconferidas em **09/10/2026**.

### Múltiplas chaves do mesmo provedor

O README descreve a possibilidade de informar chaves separadas por vírgula, por exemplo na variável `GROQ_API_KEY`, ou usar variáveis com o padrão `FREELM_<PROVIDER>_KEYS`. Isso não elimina limites nem autoriza descumprir as regras dos serviços.

### Uso de rotas sem chave

Na API da biblioteca, o autor informa:
- `keyless=True`: incluir essas rotas como último recurso;
- `keyless="auto"`: usar quando nenhuma chave estiver configurada;
- `FREELM_KEYLESS=1|auto|0`: controle correspondente por variável de ambiente.

## Como funciona o failover

O objetivo do failover é evitar que uma falha isolada torne a solicitação inutilizável. Segundo o README:

| Situação | Comportamento descrito |
|---|---|
| **429** — limite de requisições | Trocar chave, modelo ou provedor, respeitando cotas |
| **401/402** — credencial/autorização ou cobrança | Desabilitar a chave problemática |
| **5xx** — falha do serviço | Aplicar recuo (*backoff*) e proteção de circuito (*circuit breaker*) |
| **Timeout / lentidão** | Iniciar tentativa concorrente após um atraso adaptativo |
| **404/410** — modelo removido | Suspender temporariamente aquele modelo |
| **Parâmetro incompatível** | Tentar outro provedor quando fizer sentido |
| **Todos indisponíveis** | Informar a situação por meio de erro como `NoProvidersAvailable` |

### Seleção inteligente

Por padrão, a estratégia `smart` considera prioridade e latência observada. As medidas envelhecem para evitar decisões baseadas em desempenho antigo. A tentativa concorrente (*hedge*) pode reduzir a espera quando um provedor fica lento.

O texto original apresenta exemplos de cerca de **3 segundos para fluxo travado e 6 segundos para provedor lento**, baseados em simulações do próprio projeto. **Não são garantias para todos os ambientes.** Fonte de referência: [benchmarks](https://github.com/shihabshahrier/freelm/tree/main/benchmarks).

### Como comprovar a troca no vídeo

Não basta mostrar uma resposta chegando. Para afirmar “houve failover”, precisamos evidenciar:
- qual provedor foi tentado primeiro;
- qual erro ou atraso ocorreu;
- qual provedor efetivamente respondeu.

O README documenta eventos `attempt`, `hedge`, `success`, `error`, `wait` e `discovery` por callback na biblioteca. **A CLI não é descrita no material como um painel de auditoria completo dessas tentativas.** Se o CLI não exibir os detalhes, registrar essa limitação e planejar um teste instrumentado em Node.js.

## Como escolher modelos

| Identificador | Significado |
|---|---|
| `auto` ou `chat` | Escolher automaticamente um modelo para conversa |
| `chat:fast` | Preferir velocidade |
| `chat:large` | Preferir modelos maiores |
| `chat:small` | Preferir modelos menores |
| `chat:tools` | Selecionar modelos compatíveis com ferramentas |
| `vision` | Selecionar modelos com capacidade visual |
| `reasoning` | Preferir modelos com raciocínio |
| `vendor/model-id` | Solicitar um modelo específico |
| `["vendor/id", "chat:fast"]` | Sequência de fallback definida na chamada |

O README também cita `prefer=[...]`, prioridades de modelos/provedores e diferenças entre modelos comuns e modelos com raciocínio. Um orçamento `max_tokens` muito baixo pode gerar resposta vazia em modelos que consomem tokens no raciocínio interno; o projeto sugere utilizar **128 tokens ou mais** nesses casos ou optar por `auto`.

## Opções de configuração

Opções apresentadas pelo README para a biblioteca:

| Opção | Padrão | O que controla |
|---|---|---|
| `strategy` | `smart` | Estratégia: `smart`, `priority`, `round_robin`, `quota_aware` ou `latency` |
| `hedge` | `True` | Tentativa concorrente quando uma resposta demora |
| `max_attempts` | `12` | Número máximo de tentativas em uma solicitação |
| `timeout` | `60` | Prazo total, em segundos |
| `wait` | `False` | Aguardar temporariamente por cota, em vez de falhar |
| `max_wait` | `20` | Espera máxima indicada no exemplo |
| `on_event` | Não configurado | Callback dos eventos de roteamento |
| `persist` | `False` | Persistir estado de cotas e indisponibilidade entre execuções |

Também são citados: `tier`, `priority`, `prefer`, `models`, `rpm`, `rpd`, `discover`, `free_only` e `cache_ttl`.

O README descreve `FREELM_PERSIST=1` para ativar persistência de estado, em `~/.cache/freelm/state.json` com permissões restritas e hashes de chaves, não os valores de chaves. A implementação e o comportamento em cada ambiente devem ser verificados antes de ativar isso.

**Atenção:** não desativar `free_only` nem habilitar tiers pagos sem entender a cobrança do provedor.

## Exemplos com Python e JavaScript

Esta seção traduz a referência técnica original. **Para a instalação simples do vídeo, não é necessário usar esses exemplos.**

### JavaScript / TypeScript

Segundo o README, o pacote Node.js não tem dependências de runtime e oferece uso por `FreeLLM.fromEnv()`:

```javascript
import { FreeLLM } from "freelm";

const llm = FreeLLM.fromEnv();
console.log(await llm.text("Explique failover em uma frase."));

for await (const parte of llm.stream("Conte de um até cinco.", {
  signal: AbortSignal.timeout(30_000)
})) {
  process.stdout.write(parte);
}
```

O texto original informa suporte a ESM e CommonJS e a execução em diferentes ambientes JavaScript. [Documentação JavaScript](https://github.com/shihabshahrier/freelm/tree/main/js).

### Python

O pacote Python é indicado para Python **3.9 ou superior**, com instalação documentada por:

```bash
pip install freelm
```

Exemplo básico traduzido:

```python
import freelm

llm = freelm.FreeLLM.from_env()
print(llm.text("Explique failover em uma frase."))
```

Configuração explícita de provedores, segundo o autor:

```python
from freelm import FreeLLM, GoogleAIStudio, Groq, OpenRouter

llm = FreeLLM(
    [GoogleAIStudio("CHAVE-GEMINI"), Groq("CHAVE-GROQ"), OpenRouter("CHAVE-OPENROUTER")],
    strategy="smart",
)

resposta = llm.chat(
    [{"role": "user", "content": "Explique failover em uma frase."}],
    model="chat:fast",
)
print(resposta.text, "via", resposta.provider, resposta.model)
```

**Os valores das chaves acima são marcadores de demonstração; não colocar credenciais reais diretamente em código compartilhado.**

O README também exemplifica:
- `llm.stream(...)` para resposta incremental;
- `llm.chat(..., tools=[...], tool_choice="auto")` e `r.tool_calls` para chamadas de ferramenta;
- `response_format={"type": "json_object"}` para resposta JSON;
- `AsyncFreeLLM` e `astream(...)` para uso assíncrono;
- `stream_chunks()` e `astream_chunks()` para chunks compatíveis com OpenAI.

### Compatibilidade com o SDK OpenAI no Python

O projeto documenta uma alternativa que troca a importação do cliente OpenAI:

```python
from freelm.compat import OpenAI

client = OpenAI()
r = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Olá!"}],
)
print(r.choices[0].message.content)
```

Segundo o autor, a biblioteca fornece objetos de resposta semelhantes aos do SDK OpenAI, inclusive métodos como `model_dump()` e streaming. **Compatibilidade prática depende da versão usada e dos recursos do modelo selecionado.**

## Comparação com outras ferramentas

Essa comparação **resume a descrição feita pelo autor do freelm**, não uma avaliação independente.

| Ferramenta/categoria | Diferença apresentada no README |
|---|---|
| OmniRoute, 9Router, FreeLLMAPI, free-claude-code | Gateways normalmente executados como serviço; freelm pode funcionar só como biblioteca |
| freellmpool | Outra biblioteca/proxy; freelm destaca pacote TypeScript sem dependências |
| LiteLLM | Escopo mais amplo, inclusive serviços pagos; freelm concentra-se em cotas gratuitas |
| any-llm, aisuite, llm | Unificam provedores; freelm enfatiza cotas, alternância e descobertas de modelos gratuitos |
| OpenRouter | Agregador hospedado que pode ser um dos provedores acessados pelo freelm |
| gpt4free | Abordagem de endpoints por engenharia reversa; o freelm afirma priorizar tiers oficiais |
| LangChain / LlamaIndex | Frameworks de orquestração que podem usar o freelm por meio do servidor ou compatibilidade API |

## Perguntas frequentes e problemas comuns

### O freelm é grátis mesmo?

A **biblioteca é open source e MIT**, mas o uso depende da conta e dos planos dos provedores. O README descreve proteções para modelos pagos de OpenRouter, Kilo e Z.ai e adverte que habilitar opções como `tier="tier1"` ou `free_only=False` pode mudar as condições. Cloudflare em plano pago, chaves de produção da Cohere e outros serviços podem cobrar.

### O freelm consegue responder sem chave?

Segundo o autor, sim, por rotas anônimas Kilo Gateway e OVHcloud. Elas podem estar indisponíveis, oferecem menos cota e **podem registrar os prompts**.

### Por que um modelo gratuito parou de funcionar?

O modelo pode ter sido removido, a conta pode estar sem cota, a chave pode ter expirado ou o serviço pode estar fora do ar. O README afirma que o freelm tenta redirecionar a chamada, marcando temporariamente modelos removidos ou sobrecarregados.

### Como evitar erro 429?

Não existe maneira legítima de eliminar as cotas. O projeto propõe distribuir chamadas entre provedores/chaves e respeitar limites por minuto/dia. Sempre observar as regras de cada conta.

### Uma resposta prova que o failover funciona?

Não. Prova apenas que **alguma rota respondeu**. Para comprovar failover é necessário evidenciar erro/lentidão na primeira tentativa e sucesso em outra.

### A ferramenta recebe minhas perguntas?

O projeto informa que as chamadas vão aos serviços externos configurados, sem telemetria própria. Isso **não elimina o processamento, registro ou políticas de retenção dos provedores**.

### O que fazer se a API local não responde?

Conferir se `npx freelm serve` continua em execução, se o terminal correto tem as chaves exportadas e se a porta 4000 está disponível. Não abrir a API na internet como solução rápida.

### Como usar no Windows se está no WSL2?

Com o serviço no Ubuntu, testar no PowerShell:

```powershell
curl.exe http://127.0.0.1:4000/v1/models
```

A comunicação por localhost é uma característica do WSL2 em configurações suportadas; o resultado depende do modo de rede do WSL e não equivale a disponibilizar o serviço para outros equipamentos.

### Como encerrar ou remover?

No terminal em que o servidor está ativo, usar **Ctrl+C**. Para desinstalar o pacote localmente, no diretório de testes:

```bash
cd ~/testes-freelm
npm uninstall freelm
```

### Onde consultar erros específicos?

O README original remete à [referência de erros do autor](https://shahriarlabs.com/products/freelm/errors/), com exemplos para:
- Gemini 429 `RESOURCE_EXHAUSTED`;
- Gemini “User location is not supported”;
- Gemini “API key not valid”;
- Gemini 503;
- Limites de modelos gratuitos no OpenRouter;
- OpenRouter sem endpoint compatível com *tool use*;
- Limites do Groq;
- Mistral 429;
- Z.ai 1302;
- Respostas vazias de modelos de raciocínio.

## Segurança, custos e limites

- **Nunca divulgue chaves de API**, mesmo nos logs de erro.
- Testes anônimos e com provedores externos não são ambientes adequados para segredos pessoais.
- Para modelos “grátis”, confira a conta e o modelo **antes** de enviar a pergunta.
- Mantenha `freelm serve` acessível só localmente. Se precisar publicar `--host 0.0.0.0`, proteja com `--api-key`, firewall e controles adequados.
- Em integrações com agentes, confirme tamanho de contexto, suporte a ferramentas e capacidades reais do modelo usado.
- Não interprete números de benchmarks do autor como resultados testados por nós.
- Não trate proteção `free_only` como garantia universal de ausência de custos em contas configuradas com faturamento.

## Fontes e estado dos testes

**Material original:** [freelm — README oficial em inglês](https://github.com/shihabshahrier/freelm), material compartilhado pela comunidade em 20/11/2026.

**Referências:**
- [Repositório original](https://github.com/shihabshahrier/freelm)
- [Licença MIT](https://github.com/shihabshahrier/freelm/blob/main/LICENSE)
- [README JavaScript](https://github.com/shihabshahrier/freelm/tree/main/js#readme)
- [Benchmarks do autor](https://github.com/shihabshahrier/freelm/tree/main/benchmarks)
- [Referência de erros do autor](https://shahriarlabs.com/products/freelm/errors/)
- [Pacote npm](https://www.npmjs.com/package/freelm)
- [Pacote PyPI](https://pypi.org/project/freelm/)

**Situação do laboratório Café com Dados & Gatos:**

| Teste | Situação observada |
|---|---|
| Node.js e npm | **Funcionou** — Node.js 22.23.2; npm 12.0.2 |
| freelm | **Funcionou** — versão 0.5.2 pelo `npx` |
| Chat anônimo sem chave | **Funcionou** — modelo gratuito do Kilo Gateway respondeu em português |
| Descoberta de modelos | **Funcionou** — listagem de diversos modelos e provedores |
| Comando `doctor` e chaves | **Funcionou** — após correção, três de três chaves válidas: Gemini, Groq e OpenRouter |
| Rotas públicas sem chave | **Funcionaram no diagnóstico** — Kilo Gateway e OVHcloud |
| API local compatível com OpenAI | **Funcionou** — requisições a `/v1/chat/completions` retornaram HTTP 200 |
| Integração com Zoo Code | **Funcionou** — o agente criou `index.html` com a página Hello World, exibida no VS Code |
| Alternância entre modelos nas requisições | **Observada** — logs com Nemotron e Gemini |
| Acesso do Windows por `curl.exe` | **Ainda não testado diretamente** |
| Failover provocado por erro | **Não comprovado** — logs visíveis apenas com requisições bem-sucedidas |

**Atribuição:** tradução, reorganização e explicações adicionais independentes feitas para facilitar o estudo em português; o autor do projeto é Shahriar Labs. Antes de publicar em repositório público, revisar comandos, nomes de modelos, disponibilidade e condições de uso no projeto original.
