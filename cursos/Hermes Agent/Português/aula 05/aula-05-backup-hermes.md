# Aula 05 — Hermes Agent: backup, atualização e restauração no WSL2

Como criar um backup do Hermes Agent, atualizar pelo terminal e restaurar os dados na mesma instalação do Ubuntu/WSL2.

**Pré-requisito:** Hermes Agent já instalado e configurado. Todos os comandos abaixo devem ser executados no **terminal do Ubuntu/WSL2**.

## Verificar a instalação

```bash
hermes --version
hermes doctor
```

- `hermes --version`: mostra a versão instalada.
- `hermes doctor`: verifica a saúde da instalação e identifica possíveis problemas.

## Criar o backup

```bash
BACKUP_FILE="$HOME/hermes-aula05-$(date +%Y%m%d-%H%M%S).zip"
hermes backup --output "$BACKUP_FILE"
```

- `BACKUP_FILE=...`: define o nome e o caminho do backup, incluindo data e hora para não sobrescrever outro arquivo.
- `hermes backup --output`: exporta os dados do Hermes para o arquivo ZIP indicado.

**Mantenha este terminal aberto até concluir a restauração:** a variável `BACKUP_FILE` é válida na sessão atual.

## Verificar o backup

### Se o comando `unzip` não estiver instalado

Se aparecer `unzip: command not found`, instale o utilitário no Ubuntu/WSL2:

```bash
sudo apt update
sudo apt install -y unzip
```

- `apt update`: atualiza a lista de pacotes disponíveis.
- `apt install -y unzip`: instala o programa usado para verificar e extrair arquivos ZIP.

Se o `unzip` já funcionar, pule esta instalação.

```bash
ls -lh "$BACKUP_FILE"
unzip -t "$BACKUP_FILE"
sha256sum "$BACKUP_FILE"
```

- `ls -lh`: confirma a existência do arquivo e mostra seu tamanho.
- `unzip -t`: verifica se o ZIP pode ser lido sem erros.
- `sha256sum`: calcula uma impressão digital do arquivo para comparar com outra cópia.

**Guarde uma cópia protegida fora do WSL2 antes de atualizar.** Compare o hash da cópia com o original. O ZIP pode conter tokens, configurações e informações pessoais; não o publique no GitHub. Arquivos e bancos de ferramentas externas, como Obsidian, OpenViking e Hindsight, podem precisar de backup separado.

## Verificar a atualização disponível

```bash
hermes update --check
hermes update --plan
```

- `--check`: consulta se existe atualização.
- `--plan`: apresenta as ações previstas para a atualização, sem executá-las.

Essas opções precisam ser compatíveis com a versão instalada. Se não forem reconhecidas, consulte `hermes update --help` antes de continuar.

## Atualizar o Hermes pelo terminal

```bash
hermes update --backup
```

Atualiza o Hermes e solicita um backup adicional antes da atualização, nas versões que oferecem essa opção. Use somente depois de verificar o backup anterior. Se `--backup` não estiver disponível, consulte `hermes update --help` para confirmar como usar `hermes update` na sua versão.

## Verificar após atualizar

```bash
hermes --version
hermes doctor
```

Mostra a versão atual e verifica se a instalação permanece funcional.

## Restaurar o backup

O backup pode ser importado mesmo quando a atualização não causou perda de dados, para demonstrar o processo completo. **A importação pode substituir configurações e dados atuais.** Preserve o backup original, confirme que não há dados novos importantes e interrompa atividades que escrevam no Hermes antes de continuar.

```bash
hermes gateway list
hermes gateway stop
```

- `gateway list`: mostra os gateways existentes.
- `gateway stop`: interrompe o gateway do perfil atual. Se houver gateways ativos de outros perfis, interrompa-os também antes de restaurar.

Confirme que o ZIP escolhido existe e está íntegro:

```bash
test -n "$BACKUP_FILE" && test -f "$BACKUP_FILE" && unzip -t "$BACKUP_FILE"
```

O teste só passa se a variável tiver um caminho válido, o arquivo existir e o ZIP estiver íntegro. Se o terminal tiver sido fechado, informe novamente o caminho correto em `BACKUP_FILE` antes de continuar.

```bash
hermes import "$BACKUP_FILE"
```

Importa o backup selecionado. Leia a confirmação de substituição antes de prosseguir. **Importar os dados não reverte a versão do programa.**

### Se você fechou o terminal e perdeu a variável

Nesse caso, é possível restaurar informando diretamente o nome do arquivo de backup. Por exemplo:

```bash
hermes import hermes-aula05-20261114-163601.zip
```

**Substitua `hermes-aula05-20261114-163601.zip` pelo nome do seu próprio backup.** Esse exemplo funciona se você estiver na pasta onde o ZIP foi salvo (neste caso, a pasta pessoal). Se estiver em outra pasta, informe o caminho completo do arquivo. Antes da importação, confirme que o ZIP está íntegro e que os gateways envolvidos estão parados.

## Conferir a restauração

```bash
hermes doctor
hermes
```

- `hermes doctor`: verifica a instalação após a importação.
- `hermes`: inicia o agente para testar seu funcionamento.

Confira se as configurações, os perfis, as skills e as memórias esperadas estão acessíveis. Integrações externas precisam ser verificadas separadamente. Caso um gateway estivesse ativo antes, reinicie-o pelo método normalmente utilizado na instalação.

## Se o Desktop apresentar erro após a restauração

Se o Hermes Desktop abrir uma janela em branco ou apresentar erro de inicialização, feche o aplicativo e reinicie o WSL2.

**No PowerShell do Windows:**

```powershell
wsl --shutdown
```

- `wsl --shutdown`: encerra as distribuições e os processos do WSL2 para uma reinicialização limpa. Não apaga os arquivos, mas interrompe os serviços em execução.

**Depois, abra novamente o Ubuntu e execute:**

```bash
hermes desktop
```

- `hermes desktop`: inicia novamente a interface gráfica do Hermes.

Se o erro continuar, verifique os logs antes de reinstalar ou importar outro backup. Reiniciar o WSL2 não garante que todos os problemas gráficos do Desktop sejam corrigidos.

## Se o provedor ou modelo precisar ser configurado novamente

Depois da restauração, se o provedor ou modelo anterior não estiver disponível, abra o assistente no **terminal do Ubuntu**:

```bash
hermes setup model
```

- `hermes setup model`: permite escolher novamente o provedor, o modelo e a autenticação necessária.

Para instalações que usam perfis separados, execute o assistente no perfil desejado. **Exemplo com o perfil `aluno`:**

```bash
hermes -p aluno setup
```

Escolha o provedor e o modelo usados anteriormente (por exemplo, **MiniMax** e **MiniMax-M3**) e informe a chave de API apenas se o assistente solicitar. Não exponha chaves ou tokens em capturas de tela.

Após concluir, abra uma conversa nova e teste uma mensagem simples. Se uma conversa antiga mostrar `Resume failed — not_found`, isso indica um problema para retomar aquela sessão, não necessariamente uma falha do modelo.

## Referências oficiais

- [Documentação do Hermes Agent](https://hermes-agent.nousresearch.com/docs/)
- [Repositório oficial do Hermes Agent](https://github.com/NousResearch/hermes-agent)
