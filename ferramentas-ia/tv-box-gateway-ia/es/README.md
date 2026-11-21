# Cómo convertir una TV Box en una puerta de enlace de IA — Parte 1

**Café com Dados & Gatos | Documentación y comandos del video 01**

En esta guía utilizamos una **BTV BX**, con procesador **Amlogic S905X**, placa **p212**, **2 GB de RAM** y **16 GB de almacenamiento**, para ejecutar **Armbian Linux**, **XFCE Minimal**, **XRDP** y **FreeLM**. La BTV aloja la puerta de enlace; las respuestas de inteligencia artificial las procesan proveedores externos, no un modelo grande que se ejecute dentro de la TV Box.

> **Atención a la compatibilidad:** las TV Box de aspecto similar pueden tener placas, chips Wi-Fi y controladores diferentes. Comprueba el hardware y prueba Linux desde un medio externo antes de considerar instalarlo en el almacenamiento interno. La instalación en eMMC puede sustituir el sistema original y requerir procedimientos específicos de recuperación.

## Descargas utilizadas

**Herramienta para grabar imágenes USB — balenaEtcher:**  
https://etcher.balena.io/

**Imagen de Armbian utilizada en la BTV BX:**  
`Armbian_26.11.0_amlogic_s905x_bookworm_6.12.117_server_2026.11.14.img.gz`

**Descarga directa de la imagen:**  
https://github.com/ophub/amlogic-s9xxx-armbian/releases/download/Armbian_bookworm_arm64_server_2026.11/Armbian_26.11.0_amlogic_s905x_bookworm_6.12.117_server_2026.11.14.img.gz

**Página de la versión (releases):**  
https://github.com/ophub/amlogic-s9xxx-armbian/releases/tag/Armbian_bookworm_arm64_server_2026.11

**SHA-256 publicado para el archivo anterior:**  
`35af9e3e5e13c18a60c268e45e6c4d270f79a12805b4e026c2a1a829e2a7aade`

**DTB utilizado por la placa p212:** `meson-gxl-s905x-p212.dtb`.

## Preparar la memoria USB — Windows

En balenaEtcher, elige **Flash from file**, selecciona el archivo `.img.gz` indicado, escoge la memoria USB y haz clic en **Flash**. El programa graba la imagen directamente desde el archivo comprimido.

**Atención:** se borrará todo el contenido de la memoria USB. Después de grabarla, no aceptes la solicitud de Windows de formatear las particiones Linux.

Para esta placa, comprueba en la partición de arranque el archivo `uEnv.txt` y la referencia al DTB de la p212:

```text
FDT=/dtb/amlogic/meson-gxl-s905x-p212.dtb
```

La ubicación y el formato exactos dependen de la imagen utilizada. No mezcles archivos de arranque de proyectos diferentes ni copies arbitrariamente un `u-boot` de otra TV Box.

## Comprobar Linux y el almacenamiento — terminal de la BTV

```bash
cat /etc/os-release
uname -m
uname -r
free -h
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS
df -h
ip -br address
```

El comando `lsblk` permite comprobar si la raíz `/` está montada en el medio externo (`sda`, por ejemplo) o en el almacenamiento interno (`mmcblk`, dependiendo de la placa).

## Probar la red — terminal de la BTV

```bash
ping -c 3 1.1.1.1
getent hosts github.com
```

## Instalar XFCE Minimal — terminal de la BTV

```bash
sudo apt update
sudo apt install -y --no-install-recommends xorg xfce4 xfce4-terminal lightdm lightdm-gtk-greeter dbus-x11
sudo systemctl enable lightdm
sudo reboot
```

Después del reinicio, comprueba que funcionan la interfaz gráfica, el teclado, el ratón y el terminal.

## Obtener la IP de la BTV y comprobar SSH — terminal de la BTV

```bash
hostname -I
systemctl is-active ssh
```

Si el servidor SSH no está instalado o activo:

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

## Acceder al terminal de la BTV — PowerShell de Windows

Sustituye `teste` por el usuario Linux de tu TV Box y `192.168.10.106` por la IP que muestra `hostname -I`.

```powershell
ssh teste@192.168.10.106
```

Los comandos Linux siguientes se ejecutan **en la BTV**, incluso cuando se escriben mediante la conexión SSH. No ejecutes `apt` directamente en PowerShell sin haber abierto una sesión SSH.

## Instalar XRDP — terminal de la BTV

Ejecuta estos comandos con un usuario Linux normal que tenga permisos `sudo` (por ejemplo, `teste`):

```bash
sudo apt update
sudo apt install -y xrdp xorgxrdp dbus-x11
printf 'startxfce4\n' > "$HOME/.xsession"
sudo systemctl enable --now xrdp
systemctl is-active xrdp
hostname -I
ss -lnt | grep ':3389'
```

## Conectarse desde Windows — Escritorio remoto

Pulsa **Win + R**, escribe `mstsc`, introduce la IP de la BTV e inicia sesión con el usuario y la contraseña de **Linux**, seleccionando la sesión **Xorg** si aparece esa opción.

El PC y la BTV deben estar en la misma red. **No expongas el puerto 3389 a Internet.** XRDP puede abrir una sesión gráfica distinta de la que se ve por HDMI.

## Herramientas básicas — terminal de la BTV

```bash
sudo apt update
sudo apt install -y python3 python3-pip curl ca-certificates git
python3 --version
```

En una TV Box adaptada, no actualices el kernel ni el gestor de arranque sin comprobar primero la compatibilidad con la placa.

## Instalar Node.js 22 mediante nvm — terminal de la BTV

FreeLM 0.5.2 requiere Node.js 20 o posterior. En este proyecto usamos **Node.js 22** mediante nvm, sin instalar paquetes npm globales como `root`.

```bash
command -v curl
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh | bash
source ~/.bashrc
nvm install 22
nvm alias default 22
node --version
npm --version
which node
```

## Instalar e iniciar FreeLM — terminal de la BTV

```bash
npm install -g freelm
freelm --help
freelm doctor
freelm serve
```

Mantén abierta esa ventana del terminal. El servidor utiliza **`http://127.0.0.1:4000/v1` en la propia BTV**.

## Probar el servidor — otro terminal de la BTV

```bash
curl -fsS http://127.0.0.1:4000/health
curl -fsS http://127.0.0.1:4000/v1/models
```

## Abrir el túnel SSH — PowerShell del PC Windows

Con `freelm serve` en ejecución en la BTV, abre **otra ventana** de PowerShell en el PC y ejecuta:

```powershell
ssh -N -L 4400:127.0.0.1:4000 teste@192.168.10.106
```

Sustituye el usuario y la IP por los de tu TV Box. Mantén abierta la ventana del túnel: redirige el puerto **4400 del PC** al puerto **4000 de la BTV** sin exponer el servidor a Internet.

## Probar el túnel — segunda ventana de PowerShell del PC

```powershell
curl.exe -fsS http://127.0.0.1:4400/health
```

## Configurar el cliente de IA en VS Code — PC Windows

En un cliente o extensión compatible con las API de OpenAI, utiliza los siguientes valores según los campos disponibles:

| Configuración | Valor |
| --- | --- |
| Tipo de API | OpenAI Compatible |
| URL base | `http://127.0.0.1:4400/v1` |
| Clave de API (valor local de prueba) | `freelm` |
| Modelo | `auto` |

Haz una pregunta breve para comprobar la comunicación entre VS Code, el túnel SSH y FreeLM. La disponibilidad de modelos gratuitos depende de los proveedores y sus cuotas.

## Finalizar la prueba

Pulsa **Ctrl+C** en el PowerShell del túnel y en el terminal de la BTV donde esté ejecutándose `freelm serve`.

## Errores encontrados y ajustes necesarios

**Node.js 18 incompatible con FreeLM:** la versión disponible inicialmente en los paquetes de Debian era inferior a la requerida por la herramienta. Utilizamos Node.js 22 mediante nvm.

**Error `EACCES` con `npm install -g`:** la instalación global en el directorio del sistema no tenía permisos para el usuario normal. Con nvm, Node.js y los paquetes npm globales quedan dentro del directorio del propio usuario, sin necesidad de `sudo`.

## Referencias técnicas

- [Armbian comunitario para Amlogic — ophub](https://github.com/ophub/amlogic-s9xxx-armbian)
- [Hardware BTV BX y datos de la placa p212 — EducaBox](https://github.com/educabox/educabox/blob/main/boxes/btvbx.md)
- [XFCE y entornos de escritorio — Armbian](https://docs.armbian.com/config/desktops/)
- [XRDP](https://github.com/neutrinolabs/xrdp)
- [nvm](https://github.com/nvm-sh/nvm)
- [FreeLM](https://github.com/shihabshahrier/freelm)

---

**Café com Dados & Gatos — Parte 1.**
