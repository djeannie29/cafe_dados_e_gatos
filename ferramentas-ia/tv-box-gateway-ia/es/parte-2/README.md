# Cómo convertir una TV Box en un gateway de IA — Parte 2

**Café com Dados & Gatos | New API y automatizaciones con Telegram**

En este laboratorio, la BTV BX ejecutará New API como gateway de modelos de inteligencia artificial y un bot de Python para consultas, resúmenes y monitorización mediante Telegram.

## Pantalla negra y desconexión de XRDP cuando XFCE está abierto por HDMI

**Síntoma observado:** al acceder a la BTV BX mediante Escritorio remoto de Windows usando Xorg y la cuenta `teste`, se aceptaba la contraseña, aparecía una pantalla negra y la sesión remota terminaba casi inmediatamente. El acceso por SSH seguía funcionando.

**Mensajes registrados en los logs:**

```text
Session started successfully for user teste on display 10
Window manager ... exited quickly (2 secs)
(xfwm4): Gtk-WARNING: cannot open display: :10.0
```

La configuración `/home/teste/.xsession` contenía `startxfce4`, como se esperaba. A continuación, los comandos de diagnóstico mostraron:

```bash
loginctl list-sessions
ps -u teste -o pid,cmd | grep -E 'xfce4-session|xfwm4|Xorg'
```

La cuenta `teste` ya mantenía una sesión gráfica local `seat0` por HDMI, incluidos `xfce4-session` y `xfwm4 --display :0.0`. **Causa identificada en este equipo:** la sesión XFCE abierta automáticamente por HDMI con la misma cuenta `teste` interfería en la creación de la sesión XRDP. Detener la sesión local permitió acceder remotamente. El mensaje `X server already running`, por sí solo, no indica un fallo.

**Prueba que funcionó:** mantener abierto el terminal SSH como `root`, detener **temporalmente** el gestor de inicio de sesión local y, **antes de reiniciarlo**, abrir Escritorio remoto de Windows.

```bash
systemctl stop display-manager
```

**Resultado observado:** con el gestor local detenido, XRDP permitió acceder desde Windows. Este procedimiento interrumpe la interfaz gráfica por HDMI, pero no apaga Linux, SSH ni los servicios de IA. **No ejecutar `systemctl start display-manager` antes de probar XRDP**, ya que vuelve a abrir la sesión local.

**Restaurar HDMI después de la prueba temporal:** cerrar la sesión gráfica remota y ejecutar lo siguiente en la misma sesión SSH:

```bash
systemctl start display-manager
```

### Acceder únicamente desde Windows, sin abrir XFCE por HDMI

Con 2 GB de RAM, es preferible no mantener dos sesiones gráficas simultáneas. La BTV puede funcionar sin monitor, con acceso por **SSH** (terminal), **XRDP** (escritorio gráfico) o **túnel SSH** (paneles web/APIs). El túnel SSH no muestra un escritorio.

La detención temporal del gestor gráfico resolvió la desconexión en la prueba realizada. Para evitar que la sesión HDMI vuelva automáticamente después de reiniciar, desactive el inicio de **LightDM** sin eliminar XFCE ni XRDP. Confirme el resultado después de reiniciar la BTV.

**Antes de realizar cambios:** mantener abierta una sesión SSH en PowerShell, confirmar que SSH funciona y que XRDP está configurado para iniciarse con el sistema. En la BTV, desde el shell `root`:

```bash
systemctl is-enabled ssh
systemctl is-enabled xrdp
systemctl is-active xrdp
systemctl status lightdm --no-pager
```

Si SSH no está habilitado, corregirlo **antes** de desactivar el inicio de sesión gráfico local. No desactivar SSH ni XRDP. No abrir el puerto 3389 directamente a Internet.

**Una vez confirmado el acceso remoto**, desactivar únicamente LightDM local, inmediatamente y para los siguientes arranques:

```bash
systemctl disable --now lightdm
```

Esto **no desinstala** XFCE, LightDM ni XRDP; solo detiene el gestor de inicio de sesión local y deshabilita su activación automática. HDMI puede quedar sin interfaz gráfica: es el comportamiento esperado. XRDP inicia su propia sesión Xorg/XFCE al iniciar sesión remotamente. Fuente: [manual oficial de systemctl](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) y [proyecto XRDP](https://github.com/neutrinolabs/xrdp).

**Verificación después del cambio:**

```bash
systemctl is-enabled lightdm
systemctl is-active lightdm
systemctl is-active xrdp
```

Resultado esperado: `lightdm` deshabilitado e inactivo; `xrdp` activo. A continuación, acceder desde Windows con `mstsc`, usuario `teste`, sesión Xorg. **Reiniciar la BTV solo después de confirmar el acceso remoto** y repetir la prueba tras el arranque para verificar que el comportamiento persiste.

**Para recuperar HDMI con inicio de sesión gráfico automático**, mediante SSH como `root`:

```bash
systemctl enable --now lightdm
```

**Cómo ahorrar RAM:** al terminar de usar XRDP, elegir **Salir / Cerrar sesión** en el menú de XFCE en lugar de simplemente cerrar la ventana de Escritorio remoto. Desconectarse puede dejar la sesión y sus procesos cargados para una reconexión. Cuando solo se necesite un terminal o panel web, es preferible usar SSH o un túnel SSH sin iniciar XFCE.

**Importante:** sin HDMI, guarde la IP de la BTV y mantenga SSH accesible por la red. El funcionamiento después de reiniciar todavía debe confirmarse en esta unidad.

## Gateway de API con panel visual

### Descargar el binario

Acceda a https://github.com/QuantumNous/new-api/releases y descargue el binario Linux ARM64 para la BTV BX (versión v1.0.0-rc.51 o posterior compatible con `HOST`).

Cree el directorio de instalación:

```bash
mkdir -p "$HOME/new-api"
```

Guarde el ejecutable en `~/new-api` con el nombre `new-api`.

### Iniciar New API

```bash
cd "$HOME/new-api"
chmod +x new-api
HOST=127.0.0.1 PORT=3000 ./new-api
```

Mantenga abierto el terminal.

### Acceder al panel visual

En el navegador de la propia BTV:

```text
http://127.0.0.1:3000
```

Para acceder desde el PC, abra un túnel en PowerShell, sustituyendo el usuario y la IP por los de su BTV:

```powershell
ssh -N -L 3300:127.0.0.1:3000 teste@192.168.1.100
```

En el navegador del PC:

```text
http://127.0.0.1:3300
```

### Configurar New API

- Complete la configuración inicial y cree la cuenta de administrador.
- Registre un canal con el proveedor de IA, la clave del proveedor y los modelos deseados.
- Pruebe el canal.
- Cree una clave de API para el bot, con acceso únicamente a los modelos necesarios y un límite de consumo adecuado.

### Iniciar New API automáticamente con la TV Box

Después de completar la configuración inicial, detenga el proceso manual de New API con Ctrl+C. Ejecute los comandos siguientes en el terminal de la BTV con un usuario normal. El servicio se iniciará junto con la TV Box, sin necesidad de acceder por SSH, entrar en XRDP ni mantener un terminal abierto. El túnel SSH solo será necesario para acceder al panel desde el PC.

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

### Administrar New API

Iniciar:

```bash
sudo systemctl start new-api.service
```

Reiniciar:

```bash
sudo systemctl restart new-api.service
```

Detener:

```bash
sudo systemctl stop new-api.service
```

Comprobar si está habilitado para iniciarse con el sistema y si está en ejecución:

```bash
systemctl is-enabled new-api.service
systemctl is-active new-api.service
```

Consultar el estado y los logs:

```bash
systemctl status new-api.service --no-pager
sudo journalctl -u new-api.service -n 50 --no-pager
```

## Instalar Python 3

En el terminal de la BTV:

```bash
sudo apt update
sudo apt install -y python3 ca-certificates
python3 --version
mkdir -p "$HOME/central-ia"
```

El bot utiliza la biblioteca estándar de Python.

## Crear el bot en Telegram

La aplicación Telegram puede utilizarse en el teléfono móvil o en el ordenador. En el vídeo, la configuración se demostrará desde el ordenador para facilitar la visualización. En la BTV BX ejecutaremos únicamente el bot de Python, que consulta el endpoint de New API (`http://127.0.0.1:3000/v1`) con la clave de API configurada.

Abra [@BotFather](https://t.me/BotFather), envíe `/newbot` y siga las instrucciones. Abra la conversación privada con el bot creado y envíe `/start`.

## Configurar las credenciales

Utilice el token completo proporcionado por BotFather para su propio bot. No comparta el token ni la clave de API.

En el terminal de la BTV:

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

No publique el archivo `telegram.env`.

## Crear el bot de Python

El código completo está disponible en el archivo [telegram_central.py](./telegram_central.py). No es necesario copiar todo el código en el terminal.

### Descargar el archivo en el ordenador

Abra el archivo en GitHub, haga clic en **Download raw file** y guarde `telegram_central.py` en la carpeta Descargas del ordenador.

### Enviar el archivo a la BTV mediante SCP

Mantenga abierta la sesión SSH. Abra otra ventana de PowerShell en Windows y ejecute:

```powershell
scp "$HOME\Downloads\telegram_central.py" root@192.168.1.100:/root/central-ia/
```

Sustituya la IP por la dirección de su TV Box. El ejemplo utiliza el usuario `root`, tal como se muestra en la demostración. Si utiliza otro usuario, use la misma cuenta empleada para configurar las credenciales y el directorio `central-ia` de la carpeta personal de esa cuenta. Introduzca la contraseña SSH si se solicita.

### Verificar el archivo en la BTV

Vuelva al terminal SSH de la BTV y ejecute:

```bash
ls -l "$HOME/central-ia/telegram_central.py"
python3 -m py_compile "$HOME/central-ia/telegram_central.py"
```

Si el segundo comando no muestra errores, continúe con la autorización del chat y la prueba del bot.

## Autorizar el chat y realizar pruebas

```bash
set -a
. "$HOME/central-ia/telegram.env"
set +a
python3 "$HOME/central-ia/telegram_central.py" bot
```

Envíe `/id` en la conversación privada con el bot. Copie el número devuelto y detenga el proceso con Ctrl+C.

```bash
read -r -p 'Seu chat_id: ' TG_CHAT_ID
printf 'ALLOWED_CHAT_ID=%s\n' "$TG_CHAT_ID" >> "$HOME/central-ia/telegram.env"
unset TG_CHAT_ID
set -a
. "$HOME/central-ia/telegram.env"
set +a
python3 "$HOME/central-ia/telegram_central.py" bot
```

En la conversación con su bot (no con BotFather), envíe `/status` y `/ia Explica qué es una API en una frase`. Detenga el proceso con Ctrl+C antes de crear los servicios.

## Iniciar el bot automáticamente

Detenga el bot ejecutado manualmente con Ctrl+C si todavía está en ejecución. Ejecute el bloque siguiente en el terminal SSH de la BTV. El servicio del gateway debe llamarse `new-api.service`.

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

## Programar un resumen de noticias a las 07:00

### Comprobar y ajustar la zona horaria

En el terminal SSH de la BTV:

```bash
timedatectl
```

Si la zona horaria es incorrecta, ajústela a la de su ciudad. En el vídeo utilizamos Campo Grande/MS:

```bash
timedatectl set-timezone America/Campo_Grande
```

Si devuelve `Failed to set time zone: Access denied`, compruebe si está conectado como root:

```bash
id -u
```

Si devuelve `0`, intente configurar directamente la zona horaria:

```bash
test -f /usr/share/zoneinfo/America/Campo_Grande && \
  ln -sfn /usr/share/zoneinfo/America/Campo_Grande /etc/localtime && \
  echo "America/Campo_Grande" > /etc/timezone
date
timedatectl
```

Confirme que la hora y la zona horaria son correctas antes de crear la programación. Para otra ciudad, sustituya `America/Campo_Grande` por la zona correspondiente (`timedatectl list-timezones`). Si el cambio directo falla, no continúe con la programación hasta corregir la zona horaria.

### Crear la programación

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

## Monitorizar un sitio web cada 15 minutos

Introduzca la URL HTTPS de un sitio web propio o que tenga autorización para monitorizar.

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

El monitor comprueba el sitio web cada 15 minutos cuando el temporizador está activo y avisa únicamente cuando cambia el estado observado (incluida la primera comprobación). La prueba manual de notificaciones funcionó; todavía debe validarse la ejecución automática continua. Un fallo de acceso aislado no significa que el sitio esté caído para todos.

## Probar con el PC apagado

```bash
systemctl is-active new-api central-telegram
systemctl list-timers --all | grep central-
free -h
```

Apague el PC, mantenga la TV Box conectada a la corriente y a Internet y pruebe el bot desde el teléfono móvil.

## Referencias oficiales

- [New API — Releases](https://github.com/QuantumNous/new-api/releases)
- [New API — Documentación](https://docs.newapi.ai/en/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python 3 — Debian](https://packages.debian.org/bookworm/python3)
- [systemd.timer](https://www.freedesktop.org/software/systemd/man/systemd.timer.html)

**Café com Dados & Gatos — Parte 2.**