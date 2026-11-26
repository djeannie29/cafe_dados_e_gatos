# OpenBot en Ubuntu 26.04 (AMD64 / x86_64)

[Português](./openbot-ubuntu-26.md) · [Español](./openbot-ubuntu-26-es.md) · [English](./openbot-ubuntu-26-en.md)

**Sitio oficial:** https://openbot.run/

## Preparar Ubuntu

Abre la terminal y actualiza la lista de paquetes:

```bash
sudo apt update
```

Este comando no instala ni actualiza aplicaciones.

## Descargar OpenBot desde el sitio oficial

- Abre https://openbot.run/ en Firefox.
- Haz clic en **Download for Linux**.
- Comprueba que la versión para Linux sea **x86_64 / AMD64** y esté en formato **AppImage**.
- Descarga el archivo en la carpeta **Descargas**.

Que el sitio detecte Linux no significa que todas las dependencias estén instaladas.

## Abrir la aplicación

### Sin usar la terminal: Gear Lever (probado en el video)

En Ubuntu 26.04, el AppImage de OpenBot se abrió con [Gear Lever](https://flathub.org/en/apps/it.mijorus.gearlever), una aplicación gráfica que permite abrir archivos AppImage y añadirlos al menú de aplicaciones.

- En **Bazaar**, busca **Gear Lever** e instálalo.
- Abre Gear Lever y arrastra el AppImage de OpenBot desde **Descargas** hasta la ventana de Gear Lever.
- Haz clic en **Move to the app menu** para añadir OpenBot al menú de aplicaciones. Luego haz clic en **Launch** para abrirlo. Si solo quieres probarlo sin añadirlo al menú, haz clic directamente en **Launch**.

### Alternativa: abrirlo directamente desde el gestor de archivos

- Abre el gestor de archivos **Archivos**.
- Si hace falta, crea la carpeta **Applications** dentro de tu carpeta personal.
- Mueve el AppImage de **Descargas** a **Applications**.
- En **Propiedades → Permisos**, habilita la ejecución del archivo si aparece esa opción.

Si la opción no aparece, usa:

```bash
chmod +x "$HOME"/Applications/OpenBot-*-x86_64.AppImage
```

Intenta abrir el AppImage con un doble clic. **No instales dependencias de antemano: primero comprueba si se abre.**

## Solo si no se abre

**Error de FUSE / fusermount3:** comprueba si el comando existe:

```bash
command -v fusermount3
```

Si no aparece una ruta, instala la dependencia y vuelve a intentarlo:

```bash
sudo apt install fuse3
```

**Error de sandbox o de espacios de nombres de usuario (user namespaces):** en Ubuntu 26.04, OpenBot puede necesitar un perfil de AppArmor. Es un ajuste indicado en la documentación oficial. Si aparece ese error, ejecuta:

```bash
curl -fL -o /tmp/openbot.apparmor https://raw.githubusercontent.com/nightly-labs/openbot/main/build/linux/openbot.apparmor
```

Revisa el archivo descargado:

```bash
cat /tmp/openbot.apparmor
```

Instala el perfil oficial y vuelve a cargar AppArmor:

```bash
sudo install -m 0644 /tmp/openbot.apparmor /etc/apparmor.d/openbot
sudo systemctl reload apparmor
```

Si `curl` no está instalado, instálalo antes de descargar el perfil (`sudo apt install curl`). No uses `--no-sandbox` para evitar el problema.

El AppImage debe permanecer en la carpeta `~/Applications` para que coincida con la ruta del perfil.
