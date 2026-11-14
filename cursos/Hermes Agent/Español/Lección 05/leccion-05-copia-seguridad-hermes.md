# Lección 05 — Hermes Agent: copia de seguridad, actualización y restauración en WSL2

Cómo crear una copia de seguridad de Hermes Agent, actualizarlo desde la terminal y restaurar los datos en la misma instalación de Ubuntu/WSL2.

**Requisito previo:** Hermes Agent ya debe estar instalado y configurado. Todos los comandos de esta guía se ejecutan en la **terminal de Ubuntu/WSL2**, excepto los que se indican expresamente para PowerShell de Windows.

## Comprobar la instalación

```bash
hermes --version
hermes doctor
```

- `hermes --version`: muestra la versión instalada.
- `hermes doctor`: comprueba el estado de la instalación e identifica posibles problemas.

## Crear la copia de seguridad

```bash
BACKUP_FILE="$HOME/hermes-aula05-$(date +%Y%m%d-%H%M%S).zip"
hermes backup --output "$BACKUP_FILE"
```

- `BACKUP_FILE=...`: define el nombre y la ruta de la copia, con fecha y hora para evitar sobrescribir otro archivo.
- `hermes backup --output`: exporta los datos de Hermes al archivo ZIP indicado.

**Mantén abierta esta terminal hasta completar la restauración:** la variable `BACKUP_FILE` solo está disponible en la sesión actual.

## Verificar la copia de seguridad

### Si el comando `unzip` no está instalado

Si aparece `unzip: command not found`, instala la utilidad en Ubuntu/WSL2:

```bash
sudo apt update
sudo apt install -y unzip
```

- `apt update`: actualiza la lista de paquetes disponibles.
- `apt install -y unzip`: instala la herramienta que permite comprobar y extraer archivos ZIP.

Si `unzip` ya funciona, omite esta instalación.

```bash
ls -lh "$BACKUP_FILE"
unzip -t "$BACKUP_FILE"
sha256sum "$BACKUP_FILE"
```

- `ls -lh`: confirma que el archivo existe y muestra su tamaño.
- `unzip -t`: comprueba que el ZIP se puede leer sin errores.
- `sha256sum`: calcula una huella digital del archivo para compararla con otra copia.

**Guarda una copia protegida fuera de WSL2 antes de actualizar.** Compara el hash de la copia con el original. El ZIP puede contener tokens, configuraciones e información personal; no lo publiques en GitHub. Los archivos y bases de datos de herramientas externas, como Obsidian, OpenViking y Hindsight, pueden necesitar copias de seguridad independientes.

## Comprobar si hay actualizaciones disponibles

```bash
hermes update --check
hermes update --plan
```

- `--check`: consulta si hay una actualización disponible.
- `--plan`: muestra las acciones previstas para la actualización sin ejecutarlas.

Estas opciones deben ser compatibles con la versión instalada. Si no se reconocen, consulta `hermes update --help` antes de continuar.

## Actualizar Hermes desde la terminal

```bash
hermes update --backup
```

Actualiza Hermes y solicita una copia de seguridad adicional antes de la actualización, en las versiones que ofrecen esta opción. Úsala solo después de comprobar la copia anterior. Si `--backup` no está disponible, consulta `hermes update --help` para confirmar cómo utilizar `hermes update` en tu versión.

## Comprobar después de actualizar

```bash
hermes --version
hermes doctor
```

Muestra la versión actual y comprueba que la instalación sigue funcionando.

## Restaurar la copia de seguridad

La copia de seguridad también se puede importar cuando la actualización no ha causado pérdida de datos, para demostrar el proceso completo. **La importación puede reemplazar configuraciones y datos actuales.** Conserva el archivo original, confirma que no haya datos nuevos importantes y detén las actividades que escriban datos en Hermes antes de continuar.

```bash
hermes gateway list
hermes gateway stop
```

- `gateway list`: muestra los gateways existentes.
- `gateway stop`: detiene el gateway del perfil actual. Si hay gateways activos de otros perfiles, detenlos también antes de restaurar.

Comprueba que el ZIP seleccionado existe y está íntegro:

```bash
test -n "$BACKUP_FILE" && test -f "$BACKUP_FILE" && unzip -t "$BACKUP_FILE"
```

La comprobación solo se completa correctamente si la variable contiene una ruta válida, el archivo existe y el ZIP está íntegro. Si cerraste la terminal, vuelve a indicar la ruta correcta en `BACKUP_FILE` antes de continuar.

```bash
hermes import "$BACKUP_FILE"
```

Importa la copia de seguridad seleccionada. Lee el aviso de confirmación sobre el reemplazo de datos antes de continuar. **Importar los datos no revierte la versión del programa.**

### Si cerraste la terminal y perdiste la variable

En ese caso, puedes restaurar indicando directamente el nombre del archivo de copia de seguridad. Por ejemplo:

```bash
hermes import hermes-aula05-20261114-163601.zip
```

**Sustituye `hermes-aula05-20261114-163601.zip` por el nombre de tu propia copia de seguridad.** Este ejemplo funciona si estás en la carpeta donde se guardó el ZIP (en este caso, la carpeta personal). Si estás en otra carpeta, indica la ruta completa del archivo. Antes de importarlo, confirma que el ZIP está íntegro y que los gateways implicados están detenidos.

## Comprobar la restauración

```bash
hermes doctor
hermes
```

- `hermes doctor`: comprueba la instalación después de la importación.
- `hermes`: inicia el agente para probar su funcionamiento.

Comprueba que las configuraciones, los perfiles, las skills y las memorias esperadas estén disponibles. Las integraciones externas deben verificarse por separado. Si había un gateway activo antes de la restauración, vuelve a iniciarlo mediante el procedimiento habitual de tu instalación.

## Si Hermes Desktop presenta un error después de la restauración

Si Hermes Desktop abre una ventana en blanco o muestra un error de inicio, cierra la aplicación y reinicia WSL2.

**En PowerShell de Windows:**

```powershell
wsl --shutdown
```

- `wsl --shutdown`: detiene las distribuciones y los procesos de WSL2 para permitir un reinicio limpio. No borra archivos, pero interrumpe los servicios que estén en ejecución.

**Después, vuelve a abrir Ubuntu y ejecuta:**

```bash
hermes desktop
```

- `hermes desktop`: vuelve a iniciar la interfaz gráfica de Hermes.

Si el error continúa, revisa los registros antes de reinstalar o importar otra copia de seguridad. Reiniciar WSL2 no garantiza que se solucionen todos los problemas gráficos de Desktop.

## Si necesitas configurar de nuevo el proveedor o el modelo

Después de la restauración, si el proveedor o el modelo anterior no está disponible, abre el asistente en la **terminal de Ubuntu**:

```bash
hermes setup model
```

- `hermes setup model`: permite volver a elegir el proveedor, el modelo y la autenticación necesaria.

En instalaciones que utilizan perfiles separados, ejecuta el asistente para el perfil correspondiente. **Ejemplo con el perfil `aluno`:**

```bash
hermes -p aluno setup
```

Selecciona el proveedor y el modelo utilizados anteriormente (por ejemplo, **MiniMax** y **MiniMax-M3**) e introduce la clave de API solo si el asistente la solicita. No muestres claves ni tokens en capturas de pantalla.

Al terminar, abre una conversación nueva y prueba con un mensaje sencillo. Si una conversación anterior muestra `Resume failed — not_found`, eso indica un problema al intentar reanudar esa sesión, no necesariamente un fallo del modelo.

## Referencias oficiales

- [Documentación de Hermes Agent](https://hermes-agent.nousresearch.com/docs/)
- [Repositorio oficial de Hermes Agent](https://github.com/NousResearch/hermes-agent)
