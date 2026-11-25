# Como transformar uma TV Box em um Gateway de IA — Parte 2

**Café com Dados & Gatos | New API e automações com Telegram**

Neste laboratório, a BTV BX executará o New API como gateway de modelos de inteligência artificial e um bot Python para consultas, resumos e monitoramento pelo Telegram.

## Tela preta e desconexão no XRDP quando o XFCE está aberto pelo HDMI

**Sintoma observado:** ao entrar na BTV BX pela Área de Trabalho Remota do Windows usando Xorg e a conta `teste`, a senha era aceita, aparecia uma tela preta e a sessão remota terminava quase imediatamente. O acesso via SSH permanecia funcionando.

**Mensagens registradas nos logs:**

```text
Session started successfully for user teste on display 10
Window manager ... exited quickly (2 secs)
(xfwm4): Gtk-WARNING: cannot open display: :10.0
```

A configuração `/home/teste/.xsession` continha `startxfce4`, como esperado. Em seguida, os comandos de diagnóstico mostraram:

```bash
loginctl list-sessions
ps -u teste -o pid,cmd | grep -E 'xfce4-session|xfwm4|Xorg'
```

A conta `teste` já mantinha uma sessão gráfica local `seat0` pelo HDMI, incluindo `xfce4-session` e `xfwm4 --display :0.0`. **Causa identificada neste equipamento:** a sessão XFCE aberta automaticamente pelo HDMI, com a mesma conta `teste`, interferia na criação da sessão XRDP. A interrupção da sessão local permitiu entrar remotamente. A mensagem `X server already running`, isoladamente, não indica falha.

**Teste que funcionou:** manter o terminal SSH aberto, como `root`, interromper **temporariamente** o gerenciador de login local e, **antes de reiniciá-lo**, abrir a Área de Trabalho Remota do Windows.

```bash
systemctl stop display-manager
```

**Resultado observado:** com o gerenciador local parado, o XRDP permitiu entrar pelo Windows. Esse procedimento interrompe a interface gráfica do HDMI, mas não desliga o Linux, o SSH ou os serviços de IA. **Não executar `systemctl start display-manager` antes de testar o XRDP**, pois isso volta a abrir a sessão local.

**Restaurar o HDMI após o teste temporário:** encerrar a sessão gráfica remota e, no mesmo SSH, executar:

```bash
systemctl start display-manager
```

### Acessar somente pelo Windows, sem abrir XFCE no HDMI

Com 2 GB de RAM, é preferível não manter duas sessões gráficas simultâneas. A BTV pode funcionar sem monitor, com acesso por **SSH** (terminal), **XRDP** (área gráfica) ou **túnel SSH** (painéis web/APIs). O túnel SSH não exibe uma área de trabalho.

A parada temporária do gerenciador gráfico resolveu a desconexão no teste realizado. Para impedir que a sessão HDMI volte automaticamente após reiniciar, desative a inicialização do **LightDM** sem remover o XFCE nem o XRDP. Confirme o resultado depois de reiniciar a BTV.

**Antes de mudar:** deixar aberta uma sessão SSH no PowerShell, confirmar que a conexão SSH funciona e que o XRDP está configurado para iniciar no boot. Na BTV, no shell `root`:

```bash
systemctl is-enabled ssh
systemctl is-enabled xrdp
systemctl is-active xrdp
systemctl status lightdm --no-pager
```

Se SSH não estiver habilitado, corrigir isso **antes** de desligar o login gráfico local. Não desativar SSH ou XRDP. Não abrir a porta 3389 diretamente para a internet.

**Uma vez confirmados os acessos remotos**, desativar somente o LightDM local, já e para os próximos boots:

```bash
systemctl disable --now lightdm
```

Isso **não desinstala** XFCE, LightDM ou XRDP; apenas para o gerenciador de login local e remove sua ativação automática. O HDMI pode ficar sem interface gráfica: é o comportamento esperado. O XRDP inicia sua própria sessão Xorg/XFCE quando há login remoto. Fonte: [manual oficial do systemctl](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) e [projeto XRDP](https://github.com/neutrinolabs/xrdp).

**Verificação após a mudança:**

```bash
systemctl is-enabled lightdm
systemctl is-active lightdm
systemctl is-active xrdp
```

Resultado esperado: `lightdm` desabilitado e inativo; `xrdp` ativo. Em seguida, entrar no Windows com `mstsc`, usuário `teste`, sessão Xorg. **Reiniciar a BTV somente depois de confirmar o acesso remoto** e repetir o teste após o boot para validar que o comportamento persiste.

**Para recuperar o HDMI com login gráfico automático**, via SSH com `root`:

```bash
systemctl enable --now lightdm
```

**Como economizar RAM:** quando terminar de usar o XRDP, escolher **Sair / Encerrar sessão** no menu do XFCE, em vez de apenas fechar a janela do aplicativo de Área de Trabalho Remota. O simples ato de desconectar pode deixar a sessão e seus processos carregados para reconexão. Quando só precisar de terminal ou painel web, preferir SSH/túnel SSH, sem iniciar XFCE.

**Importante:** sem HDMI, guarde o IP da BTV e mantenha o SSH acessível pela rede. O funcionamento após reinicialização ainda precisa ser confirmado nesta unidade.

## API Gateway com painel visual

### Download do binário

Acesse https://github.com/QuantumNous/new-api/releases e baixe o binário Linux ARM64 para a BTV BX (versão v1.0.0-rc.51 ou posterior compatível com `HOST`).

Crie a pasta de instalação:

```bash
mkdir -p "$HOME/new-api"
```

Salve o executável na pasta `~/new-api` com o nome `new-api`.

### Iniciar o New API

```bash
cd "$HOME/new-api"
chmod +x new-api
HOST=127.0.0.1 PORT=3000 ./new-api
```

Mantenha o terminal aberto.

### Acessar o painel visual

No navegador da própria BTV:

```text
http://127.0.0.1:3000
```

Para acessar pelo PC, abra um túnel no PowerShell, substituindo o usuário e o IP pelos da BTV:

```powershell
ssh -N -L 3300:127.0.0.1:3000 teste@192.168.1.100
```

No navegador do PC:

```text
http://127.0.0.1:3300
```

### Configurar o New API

- Conclua a configuração inicial e crie a conta administrativa.
- Cadastre um canal com o provedor de IA, a chave do provedor e os modelos desejados.
- Teste o canal.
- Crie uma chave de API para o bot, com acesso somente aos modelos necessários e limite de consumo adequado.

### Iniciar o New API automaticamente com a TV Box

Após concluir a configuração inicial, encerre o processo manual do New API com Ctrl+C. Execute os comandos abaixo no terminal da BTV com o usuário comum. O serviço iniciará junto com a TV Box, sem precisar entrar por SSH, acessar o XRDP ou manter um terminal aberto. O túnel SSH será necessário apenas para acessar o painel pelo PC.

```bash
sudo tee /etc/systemd/system/new-api.service >/dev/null <<SERVICE
[Unit]
Description=Central IA - New API
Wants=network-online.target
After=network-online.target

[Service]
User=$USER
WorkingDirectory=$HOME/new-api
Environment=HOST=127.0.0.1
Environment=PORT=3000
ExecStart=$HOME/new-api/new-api
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE
sudo systemctl daemon-reload
sudo systemctl enable --now new-api.service
```

### Gerenciar o New API

Iniciar:

```bash
sudo systemctl start new-api.service
```

Reiniciar:

```bash
sudo systemctl restart new-api.service
```

Parar:

```bash
sudo systemctl stop new-api.service
```

Conferir se está habilitado para iniciar com o sistema e se está em execução:

```bash
systemctl is-enabled new-api.service
systemctl is-active new-api.service
```

Consultar o status e os logs:

```bash
systemctl status new-api.service --no-pager
sudo journalctl -u new-api.service -n 50 --no-pager
```

## Instalar o Python 3

No terminal da BTV:

```bash
sudo apt update
sudo apt install -y python3 ca-certificates
python3 --version
mkdir -p "$HOME/central-ia"
```

O bot utiliza a biblioteca padrão do Python.

## Criar o bot no Telegram

O aplicativo Telegram pode ser usado no celular ou no computador. No vídeo, a configuração será demonstrada pelo computador para facilitar a visualização. Na BTV BX executaremos apenas o bot em Python, que consulta o endpoint do New API (`http://127.0.0.1:3000/v1`) com a chave de API configurada.

Abra [@BotFather](https://t.me/BotFather), envie `/newbot` e siga as instruções. Abra a conversa privada com o bot criado e envie `/start`.

## Configurar as credenciais

Use o token completo fornecido pelo BotFather para o seu próprio bot. Não compartilhe o token nem a chave de API.

No terminal da BTV:

```bash
umask 077
read -r -s -p 'Token do BotFather: ' TG_TOKEN; echo
read -r -s -p 'Chave de API do New API: ' IA_KEY; echo
read -r -p 'Nome do modelo configurado no New API: ' IA_MODEL
printf 'BOT_TOKEN=%s\nIA_KEY=%s\nIA_MODEL=%s\nIA_URL=http://127.0.0.1:3000/v1\n' \
  "$TG_TOKEN" "$IA_KEY" "$IA_MODEL" > "$HOME/central-ia/telegram.env"
unset TG_TOKEN IA_KEY IA_MODEL
chmod 600 "$HOME/central-ia/telegram.env"
```

Não publique o arquivo `telegram.env`.

## Criar o bot Python

O código completo está disponível no arquivo [telegram_central.py](./telegram_central.py). Não é necessário copiar o código inteiro para o terminal.

### Baixar o arquivo no computador

Abra o arquivo no GitHub, clique em **Download raw file** e salve `telegram_central.py` na pasta Downloads do computador.

### Enviar o arquivo para a BTV via SCP

Mantenha a sessão SSH aberta. Abra outra janela do PowerShell no Windows e execute:

```powershell
scp "$HOME\Downloads\telegram_central.py" root@192.168.1.100:/root/central-ia/
```

Substitua o IP pelo endereço da sua TV Box. O exemplo usa o usuário `root`, conforme a demonstração. Se estiver usando outro usuário, utilize a mesma conta usada na configuração das credenciais e o diretório `central-ia` da pasta pessoal dessa conta. Informe a senha do SSH, se solicitada.

### Verificar o arquivo na BTV

Volte ao terminal SSH da BTV e execute:

```bash
ls -l "$HOME/central-ia/telegram_central.py"
python3 -m py_compile "$HOME/central-ia/telegram_central.py"
```

Se o segundo comando não exibir erros, prossiga para a autorização do chat e o teste do bot.

## Autorizar o chat e testar

```bash
set -a
. "$HOME/central-ia/telegram.env"
set +a
python3 "$HOME/central-ia/telegram_central.py" bot
```

Envie `/id` na conversa privada com o bot. Copie o número retornado e encerre o processo com Ctrl+C.

```bash
read -r -p 'Seu chat_id: ' TG_CHAT_ID
printf 'ALLOWED_CHAT_ID=%s\n' "$TG_CHAT_ID" >> "$HOME/central-ia/telegram.env"
unset TG_CHAT_ID
set -a
. "$HOME/central-ia/telegram.env"
set +a
python3 "$HOME/central-ia/telegram_central.py" bot
```

Na conversa com o seu bot (não com o BotFather), envie `/status` e `/ia Explique o que é uma API em uma frase`. Encerre com Ctrl+C antes de criar os serviços.

## Iniciar o bot automaticamente

Encerre o bot executado manualmente com Ctrl+C, caso ainda esteja em execução. Execute o bloco abaixo no terminal SSH da BTV. O serviço do gateway deve se chamar `new-api.service`.

```bash
sudo tee /etc/systemd/system/central-telegram.service >/dev/null <<SERVICE
[Unit]
Description=Central IA - Telegram
Wants=network-online.target new-api.service
After=network-online.target new-api.service

[Service]
User=$USER
WorkingDirectory=$HOME/central-ia
EnvironmentFile=$HOME/central-ia/telegram.env
ExecStart=/usr/bin/python3 $HOME/central-ia/telegram_central.py bot
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE
sudo systemctl daemon-reload
sudo systemctl enable central-telegram.service
sudo systemctl restart central-telegram.service
systemctl is-active new-api central-telegram
```

## Agendar um resumo de notícias às 07h

### Conferir e ajustar o fuso horário

No terminal SSH da BTV:

```bash
timedatectl
```

Se o fuso estiver incorreto, ajuste para o da sua cidade. No vídeo, utilizamos Campo Grande/MS:

```bash
timedatectl set-timezone America/Campo_Grande
```

Se retornar `Failed to set time zone: Access denied`, confira se está conectado como root:

```bash
id -u
```

Se retornar `0`, tente a configuração direta do fuso horário:

```bash
test -f /usr/share/zoneinfo/America/Campo_Grande && \
  ln -sfn /usr/share/zoneinfo/America/Campo_Grande /etc/localtime && \
  echo "America/Campo_Grande" > /etc/timezone
date
timedatectl
```

Confirme que o horário e o fuso estão corretos antes de criar o agendamento. Para outra cidade, substitua `America/Campo_Grande` pelo fuso correspondente (`timedatectl list-timezones`). Se a alteração direta falhar, não prossiga com o agendamento até corrigir o fuso.

### Criar o agendamento

```bash
sudo tee /etc/systemd/system/central-resumo.service >/dev/null <<SERVICE
[Unit]
Description=Central IA - Resumo de manchetes
Wants=network-online.target new-api.service
After=network-online.target new-api.service

[Service]
Type=oneshot
User=$USER
EnvironmentFile=$HOME/central-ia/telegram.env
ExecStart=/usr/bin/python3 $HOME/central-ia/telegram_central.py resumo
SERVICE
sudo tee /etc/systemd/system/central-resumo.timer >/dev/null <<'TIMER'
[Unit]
Description=Central IA - Resumo diário

[Timer]
OnCalendar=*-*-* 07:00:00
Persistent=false

[Install]
WantedBy=timers.target
TIMER
sudo systemctl daemon-reload
sudo systemctl enable --now central-resumo.timer
sudo systemctl start central-resumo.service
```

## Monitorar um site a cada 15 minutos

Informe a URL HTTPS de um site seu ou que você tenha autorização para monitorar.

```bash
read -r -p 'URL do site: ' SITE_URL
printf 'MONITOR_URL=%s\n' "$SITE_URL" >> "$HOME/central-ia/telegram.env"
unset SITE_URL
sudo tee /etc/systemd/system/central-site.service >/dev/null <<SERVICE
[Unit]
Description=Central IA - Monitorar site
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
User=$USER
EnvironmentFile=$HOME/central-ia/telegram.env
ExecStart=/usr/bin/python3 $HOME/central-ia/telegram_central.py site
SERVICE
sudo tee /etc/systemd/system/central-site.timer >/dev/null <<'TIMER'
[Unit]
Description=Central IA - Monitorar site a cada 15 minutos

[Timer]
OnBootSec=2min
OnUnitActiveSec=15min

[Install]
WantedBy=timers.target
TIMER
sudo systemctl daemon-reload
sudo systemctl enable --now central-site.timer
sudo systemctl start central-site.service
```

O monitor verifica o site a cada 15 minutos quando o timer está ativo e avisa somente quando o estado observado muda (incluindo a primeira verificação). O teste manual de notificações funcionou; a execução automática contínua ainda precisa ser validada. Uma falha de acesso isolada não significa que o site esteja fora do ar para todos.

## Testar com o PC desligado

```bash
systemctl is-active new-api central-telegram
systemctl list-timers --all | grep central-
free -h
```

Desligue o PC, mantenha a TV Box conectada à energia e à internet e teste o bot pelo celular.

## Referências oficiais

- [New API — Releases](https://github.com/QuantumNous/new-api/releases)
- [New API — Documentação](https://docs.newapi.ai/en/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python 3 — Debian](https://packages.debian.org/bookworm/python3)
- [systemd.timer](https://www.freedesktop.org/software/systemd/man/systemd.timer.html)

**Café com Dados & Gatos — Parte 2.**