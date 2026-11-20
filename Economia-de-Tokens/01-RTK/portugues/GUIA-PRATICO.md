# Guia prático — RTK no Ubuntu/WSL2 com VS Code, Codex CLI e Claude Code

## Objetivo

**Material público de apoio ao vídeo da série Economia de Tokens do Café com Dados & Gatos.** Publicado com resultados observados e limitações explicitadas. O PDF dos slides será disponibilizado separadamente na pasta de português.

Demonstrar como preparar o VS Code conectado ao Ubuntu no WSL2, instalar e verificar o RTK (Rust Token Killer), integrar a ferramenta aos agentes compatíveis e medir o consumo durante a construção do site definido na ficha deste episódio.

O mesmo procedimento de conexão do VS Code também serve como orientação para quem usa Ubuntu instalado diretamente no computador: nesse caso, não precisa da extensão WSL; abre o VS Code no próprio Linux.

## Fontes oficiais

- RTK: https://github.com/rtk-ai/rtk
- Instalação: https://www.rtk-ai.app/docs/getting-started/installation/
- Agentes suportados: https://www.rtk-ai.app/docs/getting-started/supported-agents/
- Métricas do RTK: https://www.rtk-ai.app/docs/analytics/gain/
- Hooks do Claude Code: https://code.claude.com/docs/en/hooks
- VS Code no WSL: https://code.visualstudio.com/docs/remote/wsl

## Preparar o VS Code para trabalhar no WSL2

### No Windows

- Abrir o VS Code.
- Abrir Extensões com `Ctrl + Shift + X`.
- Procurar **WSL**, da Microsoft, e instalar se ainda não estiver instalada.
- Abrir a Paleta de Comandos com `F1`.
- Executar **WSL: Connect to WSL**.
- Aguardar a abertura da nova janela conectada ao Ubuntu.

### No Ubuntu/WSL2

Abrir o terminal Ubuntu criar a pasta "testes-economia-tokens" e entrar na pasta do projeto. Para abrir a pasta atual no VS Code conectado ao WSL:

```bash
mkdir -p ~/testes-economia-tokens
cd ~/testes-economia-tokens
code .
```

Na janela do VS Code, conferir o indicador remoto no canto inferior esquerdo: deve mostrar **WSL: Ubuntu** ou a distribuição instalada.

No terminal integrado do VS Code, executar:

```bash
uname -s
pwd
```

Resultado esperado para o sistema:

```text
Linux
```

O caminho exibido por `pwd` deve pertencer ao sistema de arquivos Linux, por exemplo, dentro de `/home/usuario/`, e não a uma pasta montada em `/mnt/c`.

> Em Ubuntu instalado diretamente no computador, abrir o terminal Linux, entrar na pasta do projeto e executar `code .`. A extensão WSL e o comando **WSL: Connect to WSL** não são necessários nesse caso.

## Conferir o ambiente

Todos os comandos desta seção devem ser executados no terminal Ubuntu integrado ao VS Code.

```bash
cat /etc/os-release
uname -a
code --version
codex --version
claude --version
command -v rtk
```

Se algum agente ainda não estiver instalado, registrar isso e seguir o guia oficial correspondente antes de iniciar as medições. Não instalar ou atualizar agentes no meio de um par A/B.

## Instalar e verificar RTK

Consultar a documentação oficial atual antes de executar. O procedimento abaixo é uma referência de preparação, não uma confirmação de que o instalador continua idêntico.

Baixar o instalador para inspeção:

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh -o /tmp/rtk-install.sh
less /tmp/rtk-install.sh
```

Depois de revisar o conteúdo e confirmar que corresponde à documentação oficial:

```bash
sh /tmp/rtk-install.sh
export PATH="$HOME/.local/bin:$PATH"
rtk --version
rtk gain
```

Se o executável não for encontrado, verificar o caminho de instalação indicado pela versão instalada e pela documentação oficial. Não alterar arquivos de inicialização do shell sem registrar a mudança.

**Interpretação:** `rtk gain` apresenta estimativas de saídas tratadas/comprimidas pelo RTK. Não equivale, por si só, ao total de tokens faturados pelo provedor nem à economia financeira final.

## Projeto do episódio

Usar o briefing completo do site **Cafeteria Aurora** descrito em [briefing completo neste documento](#briefing-integral--cafeteria-aurora).

O site deve ser criado do zero com quatro páginas: Início, Sobre, Serviços/Produtos e Contato. Manter o mesmo briefing, conteúdo, stack, dependências e critérios de aceite nas quatro execuções.

Antes de cada execução:
- criar uma pasta de projeto vazia e independente;
- iniciar uma sessão nova do agente;
- confirmar o modelo e o provedor;
- conferir que o RTK está desligado na rodada sem ferramenta e ativo na rodada com ferramenta;
- não reutilizar código, histórico de conversa ou cache de workspace entre as rodadas sem registrar a diferença.

## Medir o consumo no Codex CLI

Dentro do Codex CLI, consultar:

```text
/status
```

Registrar as informações disponíveis antes e depois da construção do site. A disponibilidade e o significado dos campos podem variar conforme a versão do Codex.

### Codex — Rodada A, sem RTK

No terminal Ubuntu:

```bash
mkdir -p ~/testes-economia-tokens/rtk/codex-sem-rtk
cd ~/testes-economia-tokens/rtk/codex-sem-rtk
```

Iniciar o Codex:

```bash
codex
```

Dentro do Codex:
- executar `/status` no início;
- enviar o briefing do site, sem alterações;
- aguardar a implementação;
- conferir o build, os testes e as quatro páginas;
- executar `/status` novamente no final;
- registrar tokens, duração, erros e intervenções.

### Codex — Rodada B, com RTK

Criar e entrar na pasta do projeto **antes** de inicializar: o hook do Codex é específico da pasta.

~~~bash
mkdir -p ~/testes-economia-tokens/rtk/codex-com-rtk
cd ~/testes-economia-tokens/rtk/codex-com-rtk
rtk init --codex --dry-run
~~~

Se a prévia estiver correta:

~~~bash
rtk init --codex
cat .codex/hooks.json
codex
~~~

A configuração esperada usa **PreToolUse**, matcher **Bash** e comando **rtk hook codex**. O arquivo configurado não prova, sozinho, que a reescrita ocorreu. Nos testes anteriores com Codex 0.170.0 e RTK 1.2.1, foi observada reescrita automática de **ls -la .codex** para **rtk ls -la .codex**, distinguindo hook ativo de uso voluntário de comandos RTK.

Dentro do Codex:
- executar `/status` no início;
- enviar exatamente o mesmo briefing usado na Rodada A;
- conferir build, testes e quatro páginas;
- executar `/status` no final;
- registrar tokens, duração, erros e intervenções.

Fora do Codex, registrar a estimativa do RTK:

```bash
rtk gain
```

## Medir o consumo no Claude Code com MiniMax

Dentro do Claude Code, consultar a tela de **Usage** com:

~~~text
/usage
~~~

Registrar os dados da sessão **antes de enviar o prompt principal** e novamente **ao concluir a tarefa**, na mesma sessão. Manter separados: tokens de entrada, tokens de saída, cache read, cache write, custo estimado e tempo total. Valores exibidos em K/M são arredondados.

Com MiniMax como provedor externo, o custo exibido pelo Claude Code pode estar incorreto: confirmar valores de cobrança no painel do provedor. Os tokens estimados pelo RTK em `rtk gain` medem a redução da saída de comandos, não o consumo total faturado pelo modelo.

**Protocolo A/B:** usar o mesmo modelo MiniMax, briefing, pastas de trabalho vazias, modo de permissões e critérios de aceite nas duas rodadas. Fazer testes do hook **antes** de registrar a linha de base. Evitar comandos ou pedidos adicionais em apenas uma das condições.

### Claude Code — Rodada A, sem RTK

No terminal Ubuntu/WSL2:

~~~bash
mkdir -p ~/testes-economia-tokens/rtk/claude-sem-rtk
cd ~/testes-economia-tokens/rtk/claude-sem-rtk
rtk init --show
~~~

Conferir que não há hook global do RTK ativo no Claude e que esta pasta não contém um hook RTK local em .claude/settings.json ou .claude/settings.local.json. Não executar `rtk init` nesta pasta. Em caso de configuração prévia, preservar backup e revisar antes de qualquer alteração.

Iniciar nova sessão:

~~~bash
claude
~~~

Dentro do Claude Code:

- confirmar o modelo e o provedor MiniMax;
- abrir `/usage` e registrar o consumo inicial;
- enviar o briefing integral da Cafeteria Aurora, sem adaptações;
- conferir build, testes e quatro páginas;
- abrir `/usage` de novo ao término e registrar o consumo final;
- anotar erros de API, interrupções, duração e eventuais pedidos extras.

### Claude Code — Rodada B, com RTK (hook local, sem afetar a Rodada A)

A documentação do RTK mostra `rtk init --global` como instalação **global** do hook do Claude (em ~/.claude/settings.json). **Não usar a opção global neste experimento**, porque ela também afetaria a condição sem RTK.

A opção `rtk init` sem `--global` cria as instruções locais do RTK, mas **não instala hook automático**. Para este laboratório, combinar a inicialização local do RTK com o hook de projeto suportado oficialmente pelo Claude Code.

No terminal Ubuntu/WSL2, entrar primeiro na pasta que receberá o RTK:

~~~bash
mkdir -p ~/testes-economia-tokens/rtk/claude-com-rtk
cd ~/testes-economia-tokens/rtk/claude-com-rtk
rtk --version
claude --version
rtk init
~~~

**Obrigatório para este teste:** `rtk init` apenas adiciona instruções ao `CLAUDE.md`; a mensagem `hooks: NOT registered` significa que o hook automático ainda não foi instalado. **Antes de abrir o Claude ou registrar os tokens iniciais, execute o bloco a seguir** para criar o hook local em `.claude/settings.local.json`. Não pule este bloco na gravação:

~~~bash
mkdir -p .claude
if [ -e .claude/settings.local.json ]; then
  echo "Arquivo .claude/settings.local.json já existe; revisar e mesclar sem sobrescrever."
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
~~~

**Atenção:** não substituir um settings.local.json preexistente. Se já houver configurações, é necessário mesclar o bloco `hooks` preservando as demais opções, antes de prosseguir. O bloco acima é para a pasta vazia preparada para o vídeo.

Verificar o arquivo e a capacidade de reescrita:

~~~bash
python3 -m json.tool .claude/settings.local.json >/dev/null && echo "JSON válido"
cat .claude/settings.local.json
rtk rewrite 'git status'
~~~

Saída esperada da última linha, para esta regra:

~~~text
rtk git status
~~~

**Como confirmar o hook antes do teste principal:**

~~~bash
claude
~~~

Dentro do Claude Code, abrir:

~~~text
/hooks
~~~

Verificar a existência de um hook **PreToolUse / Bash**, com comando **rtk hook claude**, identificado como configuração local do projeto. O comando `rtk init --show` pode indicar que não há hook *global* instalado; isso, sozinho, não invalida o hook criado em .claude/settings.local.json.

Para um teste rápido, solicitar ao Claude: **Execute ls -la no terminal, sem escrever rtk manualmente. Não altere arquivos.** Observar se a saída é compatível com a reescrita e conferir o relatório `rtk gain` fora do Claude. A existência do hook no menu e a saída condensada são indícios; para demonstrar reescrita efetiva, comparar o comando enviado à ferramenta com o comando executado, quando a interface permitir. Não tratar estatísticas isoladas como prova de execução do hook.

Encerrar essa sessão de verificação e iniciar outra sessão nova para a medição oficial.

### Limpar somente as estatísticas, preservando o RTK

O histórico do `rtk gain` é **global**, podendo incluir comandos de testes anteriores com Codex. Antes de zerar, salvar o relatório, se ainda precisar dos dados:

~~~bash
mkdir -p ~/testes-economia-tokens/rtk/backups
rtk gain --all --format json > ~/testes-economia-tokens/rtk/backups/rtk-gain-antes-claude.json
rtk gain --reset
rtk gain
~~~

O `rtk gain --reset` pede confirmação e apaga os dados acumulados de economia e recall; **não desinstala o RTK nem seus hooks**. Fazer o reset **depois** do teste de funcionamento do hook e **antes** da medição da rodada B.

### Executar a Rodada B e medir

Na pasta correta:

~~~bash
cd ~/testes-economia-tokens/rtk/claude-com-rtk
claude
~~~

Dentro do Claude Code:

- confirmar o mesmo modelo MiniMax e modo de permissões da Rodada A;
- registrar a tela `/usage` inicial;
- enviar **exatamente** o mesmo briefing do site;
- conferir build, testes e quatro páginas;
- registrar a tela `/usage` final, sem acrescentar tarefas extras;
- anotar erros, interrupções, tempo e intervenções.

Fora do Claude Code:

~~~bash
rtk gain
~~~

Registrar separadamente (a) consumo líquido da sessão Claude, calculado por **final menos inicial**, e (b) economia estimada de saídas de comandos informada pelo RTK. Um percentual alto no `rtk gain` **não** implica a mesma redução no total de tokens da sessão.

### Se a integração não aparecer

- Conferir se o terminal está na pasta **claude-com-rtk** e não na pasta sem RTK.
- Confirmar o arquivo com `cat .claude/settings.local.json` e JSON válido.
- Abrir `/hooks` no Claude para verificar se o hook local foi carregado.
- Encerrar e abrir uma **nova sessão** do Claude após criar o arquivo.
- Se `rtk init --show` informar ausência de hook, lembrar que a configuração do teste é local e verificar pelo menu do Claude.
- Não recorrer a `rtk init --global` como correção automática: isso contaminaria a rodada sem RTK.

## Prompt do site

Copiar integralmente o briefing da seção **Briefing integral — Cafeteria Aurora**, apresentada abaixo. O texto deve ser o mesmo nas quatro execuções, sem adaptações de conteúdo entre agentes ou condições.

## Briefing integral — Cafeteria Aurora

Criar do zero um site institucional de quatro páginas, sem backend, com Vite + React + TypeScript. Deve conter: cabeçalho e rodapé, navegação funcional, layout responsivo, acessibilidade básica, três cards de oferta, duas perguntas frequentes e formulário com validação local (sem enviar dados).

Todas as informações deste briefing são **fictícias**, para uso em laboratório. Não inventar endereço real ou telefone; usar `contato@exemplo.test` e marcar como contato demonstrativo.

### Página 1 — Início
- Nome/marca: **Cafeteria Aurora**
- Destaque: **Café especial, doces caseiros e uma pausa gostosa no meio da cidade.**
- Texto de apresentação: serviço demonstrativo do setor de cafeteria artesanal.
- Seção de três destaques, usando os três cards definidos abaixo.
- CTA: **Conheça nossos serviços** (navega para Serviços/Produtos).

### Página 2 — Sobre
- Título: **Nossa história**
- Conteúdo fixo: A Cafeteria Aurora nasceu do desejo de reunir pessoas em torno de cafés preparados com atenção e receitas feitas na casa.
- Valores: **acolhimento, transparência e simplicidade**.
- CTA: **Entre em contato** (navega para Contato).

### Página 3 — Serviços/Produtos
- Título: **O que oferecemos**
1. Espresso da Casa — café encorpado com notas de chocolate
2. Cappuccino Aurora — espresso, leite vaporizado e canela
3. Bolo de Laranja — fatia macia com calda cítrica
- FAQ:
  - Há opções sem lactose? Sim, mediante disponibilidade.
  - É necessário reservar? Não, o atendimento é por ordem de chegada.
- Sem carrinho, pagamento, login, APIs ou funcionalidades externas.

### Página 4 — Contato
- Título: **Fale com a gente**
- Texto: **Envie uma mensagem para saber mais sobre nossas atividades.**
- Formulário demonstrativo com **nome, e-mail, assunto e mensagem**, validação no cliente e feedback visível de envio simulado, sem backend.
- Contato demonstrativo: **contato@exemplo.test**.
- Aviso de que o formulário não envia mensagens reais.


## Registro das quatro execuções — resultados medidos (19–20/11/2026)

**Protocolo:** uma rodada sem e outra com RTK para cada harness, no Ubuntu/WSL2. Em cada comparação, usar somente dados do mesmo modelo, descontando o estado inicial da sessão. Os valores iniciais compactados em K/M são **arredondados**, logo os valores líquidos também são aproximados. A ferramenta RTK mede *saídas locais de comandos*, e não o total da execução.

### Codex CLI — GPT-6.1 Sol Medium

A interface do Codex exibiu, **antes do prompt principal**, estes contadores:

| Condição | Inicial `used` | Inicial `in` | Inicial `out` | Final `used` |
|---|---:|---:|---:|---:|
| Sem RTK | ~4,27 mil | ~16,2 mil | 10 | 65.734 |
| Com RTK | ~4,31 mil | ~16,2 mil | 10 | 69.336 |

**Significado das medidas:** no Codex, o contador `used` é a soma de **entrada não armazenada em cache + saída**; `in` inclui a entrada em cache. Portanto, é incorreto descontar os ~16,2 mil de `in` diretamente dos valores finais de `used` e também incorreto interpretar `4,27K used` como mero tamanho da janela de contexto. Fonte: [implementação oficial de `TokenUsage::blended_total`](https://github.com/openai/codex/blob/main/codex-rs/tui/src/token_usage.rs) e [exibição da status line](https://github.com/openai/codex/blob/main/codex-rs/tui/src/chatwidget/status_surfaces.rs).

**Contadores finais brutos** (diretamente do comando exibido no terminal):

| Métrica final | Sem RTK | Com RTK |
|---|---:|---:|
| `used` (entrada não cacheada + saída) | 65.734 | 69.336 |
| Entrada não cacheada | 52.842 | 56.290 |
| Saída | 12.892 | 13.046 |
| Entrada em cache | 868.096 | 829.696 |

Cálculo da **tarefa líquida**: subtrair os contadores iniciais correspondentes. Como o `in` inicial é arredondado, o cache inicial é estimado por `in inicial − (used inicial − out inicial)`.

| Métrica líquida estimada | Sem RTK | Com RTK | Variação |
|---|---:|---:|---:|
| Entrada não cacheada | ~48.582 | ~51.990 | ~+3.408 (**+7,0%**) |
| Saída | ~12.882 | ~13.036 | +154 (**+1,2%**) |
| **Entrada não cacheada + saída (`used`)** | **~61.464** | **~65.026** | **~+3.562 (+5,8%)** |
| Entrada em cache | ~856.156 | ~817.796 | ~−38.360 (**−4,5%**) |

No comando `rtk gain`, o RTK reportou **1 comando**, redução estimada de **33 para 10 tokens** e **23 tokens economizados (69,7%) apenas naquela saída**. Não extrapolar 69,7% para a sessão inteira. Os prints originais mostram os contadores acumulados, enquanto a tabela acima mostra estimativas ajustadas ao início da tarefa.

### Claude Code — MiniMax M3.1 Flash

A condição sem RTK começou com aproximadamente **12,9 mil de entrada** e **82 de saída**. Ao final, o Claude Code mostrava **79,5 mil de entrada** e **30,2 mil de saída**. Subtraindo o ponto inicial, temos **~66.600 de entrada + ~30.118 de saída = ~96.718**. A condição com RTK começou zerada para entrada/saída e terminou com **~73.700 + ~25.500 = ~99.200**.

| Métrica | Sem RTK (líquido) | Com RTK (líquido) | Variação |
|---|---:|---:|---:|
| Entrada | ~66.600 | ~73.700 | **+10,7%** |
| Saída | ~30.118 | ~25.500 | **−15,3%** |
| Entrada + saída | **~96.718** | **~99.200** | **+2,6%** |
| Cache read mostrado no painel final* | ~2,5 milhões | ~1,6 milhão | ~−36% |
| Requisições | 76 | 62 | −18,4% |
| Tempo mostrado no painel | 12min10s | 10min49s | −1min21s |

*Os valores de cache do Claude são os exibidos nos painéis finais, **não uma subtração comprovada de cache final − cache inicial**. Não tratá-los como medidas líquidas equivalentes às de entrada e saída.

O `rtk gain` registrou **17 comandos**, redução estimada de **747 para 406 tokens** e **341 tokens economizados (45,6%) nas saídas desses comandos**. A rodada com RTK gerou visualmente um site mais simples, além de ter exigido retomada durante a execução. **Não há evidência de causalidade** entre a ferramenta, a simplificação visual e a interrupção. O tempo exibido pelo painel não equivale necessariamente ao tempo de trabalho/gravação.

### Interpretação dos resultados

- **Codex:** +5,8% na soma líquida de entrada não cacheada + saída. O percentual anterior de **+5,5%** comparava finais **sem descontar o consumo inicial** e foi substituído pelo valor metodologicamente ajustado.
- **Claude Code:** +2,6% na soma líquida de entrada + saída, embora a saída e o cache exibido tenham diminuído.
- **RTK:** 69,7% (Codex) e 45,6% (Claude) são **percentuais locais de compressão**, não economias globais de tokens.
- **Limitação:** uma única execução por condição; resultados exploratórios, não comprovação de causa e efeito.

## Simulação financeira de API (não representa cobrança real)

Valores utilizados (USD por milhão de tokens): **GPT-6.1 Sol** entrada **US$ 2,00**, saída **US$ 10,00**, leitura de cache **US$ 0,10**; **MiniMax M3.1 Flash** entrada **US$ 0,15**, saída **US$ 0,60**, leitura de cache **US$ 0,015**. Confirmar tarifas na data de republicação. Fontes: [OpenAI](https://developers.openai.com/api/docs/models/gpt-6.1-sol) e [MiniMax](https://www.minimax.io/blog/minimax-m31f).

Fórmula ilustrativa, **pressupondo campos de entrada não cacheada, saída e leitura de cache distintos**:

```text
Custo (US$) = (entrada_sem_cache × preco_entrada
              + saida × preco_saida
              + leitura_cache × preco_cache) / 1.000.000
```

| Simulação | Sem RTK | Com RTK | Variação |
|---|---:|---:|---:|
| Codex com linha de base descontada | ~US$ 0,3116 | ~US$ 0,3161 | **~+US$ 0,0045 (+1,5%)** |
| Claude Code com cache final aproximado | ~US$ 0,0656 | ~US$ 0,0504 | **~−US$ 0,0152 (−23,2%)** |

Os valores do Codex foram **corrigidos após descontar a linha de base**: estimativa de entrada ~48.582/51.990; saída ~12.882/13.036; cache ~856.156/817.796. O resultado financeiro é apenas uma **simulação de preços de API**, não custo efetivamente faturado pelas assinaturas, e depende da hipótese de tratamento separado do cache. No Claude, o cache é especialmente incerto porque não se dispõe de uma linha de base comprovadamente descontada. Não inclui gravações de cache, ferramentas tarifadas separadamente ou eventuais regras adicionais.

**Lição:** economia na saída de comandos ≠ redução na soma dos tokens da sessão ≠ economia de custo. Avaliar entrada, saída, cache, custo e qualidade separadamente.

## Erros encontrados e ajustes necessários

Os resultados das quatro execuções foram preenchidos acima. Registrar o que ocorreu sem confundir observação com causa:
- erro e mensagem completa;
- ambiente e rodada em que ocorreu;
- comando ou configuração utilizada;
- correção realmente executada;
- resultado observado.

Não descrever hipótese como solução validada.

**Ocorrências observadas e referências de troubleshooting (revisar a rodada exata nas gravações):**
- O Claude Code conectado ao MiniMax mostrou aviso de que a checagem de segurança do modo Auto não estava disponível através do gateway externo. A alternativa escolhida foi permanecer no modo Auto, com aprovação manual quando exigida.
- O Claude Code exibiu repetidamente `API Error: The response stream was malformed`; a execução prosseguiu e o agente informou conclusão do site, mas o aviso deve ser documentado.
- O comando `rtk init --global --dry-run` retornou `Nothing written`, conforme esperado de uma simulação; portanto não havia instalado o hook global.
- A separação entre `claude-sem-rtk` e `claude-com-rtk` precisa incluir os **hooks**, e não apenas os arquivos de código.
- **Rodada Claude com RTK:** aviso `No hook installed` mesmo havendo hook local `PreToolUse` visível no Claude Code em `.claude/settings.local.json`; comportamento semelhante ao descrito na [issue #2024](https://github.com/rtk-ai/rtk/issues/2024) do RTK. Hipótese compatível, mas não se comprovou a ativação do hook em **todas** as chamadas. O `rtk gain` registrou saídas comprimidas, o que não confirma interceptação integral. Não ativar globalmente só para remover o aviso, pois isso poderia contaminar a condição sem RTK.
- **Rodada Claude com RTK:** houve interrupção e retomada; a causa não foi comprovada.

## Remover a integração RTK depois dos testes

Antes de remover, conferir a documentação da versão instalada e revisar as alterações feitas durante o teste. Os comandos abaixo são referências que precisam ser confirmadas na versão em uso.

Codex, na pasta do projeto de teste:

```bash
rtk init --codex --uninstall --dry-run
```

Se a prévia estiver correta e a opção for suportada:

```bash
rtk init --codex --uninstall
```

Claude Code neste laboratório: o hook foi configurado **somente** em `claude-com-rtk/.claude/settings.local.json`. Ao terminar, inspecionar esse arquivo antes de removê-lo; se ele contiver configurações além do hook RTK, remover apenas o bloco do RTK. O arquivo `~/.claude/settings.json` global **não precisa ser alterado** para este teste. Se em outro ambiente foi usado `rtk init -g`, consultar `rtk init -g --uninstall` na documentação oficial antes de remover o hook global.


- [ ] Confirmar versões de Ubuntu, VS Code, extensão WSL, Codex, Claude Code, MiniMax e RTK.
- [ ] Conferir comandos de instalação e integração RTK na documentação oficial atual.
- [ ] Gravar a conexão do VS Code ao WSL2 e o teste do terminal Linux.
- [x] Instalação do RTK demonstrada na gravação.
- [x] Executar as quatro rodadas com pastas e sessões independentes.
- [x] Registrar e comparar consumo de tokens das quatro rodadas, com desconto das linhas de base conhecidas.
- [ ] Auditar nos logs originais os testes automatizados/build de cada rodada e a linha de base de cache do Claude.
- [x] Revisão editorial de referências privadas, conteúdo sensível e orientações de publicação.


## Instalar o Codex CLI no Ubuntu/WSL2

Esta seção fica como referência para quem precisar preparar o Codex. **No vídeo deste episódio, a instalação demonstrada será a do Claude Code**; o Codex já estará instalado no ambiente da gravação.

Fonte oficial: https://learn.chatgpt.com/docs/cli e https://github.com/openai/codex

No terminal Ubuntu/WSL2:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

Depois, conferir:

```bash
codex --version
command -v codex
```

Iniciar:

```bash
codex
```

Na primeira execução, seguir o fluxo de autenticação apresentado pelo Codex. A documentação oficial também disponibiliza instalação via npm:

```bash
npm install -g @openai/codex
```

Usar apenas um método de instalação por vez. Não instalar por cima de uma instalação existente sem antes identificar o método e decidir se é atualização ou instalação limpa.

## Instalar o Claude Code no Ubuntu/WSL2

**Esta é a instalação que será demonstrada no vídeo.** O procedimento usado no ambiente de gravação foi o instalador nativo oficial da Anthropic.

Fonte oficial: https://docs.anthropic.com/en/docs/claude-code/getting-started

No terminal Ubuntu/WSL2:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Verificar:

```bash
claude --version
command -v claude
```

O caminho do executável pode variar conforme o método e a versão do instalador. A localização do executável pode ser diferente; neste tipo de instalação, um caminho comum é `$HOME/.local/bin/claude`.

A documentação da Anthropic também apresenta a instalação via npm:

```bash
npm install -g @anthropic-ai/claude-code
```

Não usar `sudo npm install -g`. Para este vídeo, manter o método nativo acima, que foi o método observado e testado no Ubuntu/WSL2.

## Configurar o Claude Code com o MiniMax M Plan / Token Plan

Fonte oficial MiniMax: https://platform.minimax.io/docs/m-plan/claude-code

O M Plan/Token Plan fornece uma Subscription Key própria para uso em ferramentas compatíveis. Essa chave é diferente da chave padrão de API pré-paga. Não publicar a chave em repositórios, capturas de tela ou gravações.

A MiniMax disponibiliza um assistente de configuração para integrar o plano ao Claude Code. No terminal Ubuntu/WSL2:

```bash
npx -y mmx-cli@latest agent setup
```

Seguir o assistente:
- selecionar Claude Code;
- selecionar/configurar a chave de assinatura do M Plan/Token Plan;
- conferir o modelo e a região/endereço indicados pelo assistente;
- concluir a configuração e reiniciar o Claude Code.

Verificar a versão e iniciar:

```bash
claude --version
claude
```

