# Lección 04 — Obsidian con OpenViking y Hindsight en Hermes

## Objetivo de la lección

Usar el mismo Vault de Obsidian como base de conocimiento para comparar OpenViking y Hindsight en Hermes.

Al final, será posible:

- importar el contenido del Vault a OpenViking;
- importar el mismo contenido a Hindsight;
- validar la ingesta en ambos proveedores;
- probar el Perfil `aluno` con OpenViking;
- probar el Perfil `lois` con Hindsight;
- comparar la recuperación usando exactamente la misma base.

## Requisitos previos

- Hermes Agent funcionando.
- Perfil `aluno` configurado con OpenViking.
- Perfil `lois` configurado con Hindsight.
- OpenViking ya configurado en la Lección 3.
- Hindsight ya configurado en el Perfil `lois`.
- Obsidian instalado.
- Un Vault de Obsidian ya existente con archivos Markdown.

## Concepto central

Obsidian organiza los archivos Markdown en el Vault. OpenViking y Hindsight no pasan a conocer este contenido automáticamente solo porque el Vault exista.

En esta lección, el Vault ya está listo. El objetivo es únicamente integrar la carpeta existente con ambos proveedores.

En el entorno utilizado en la grabación, Obsidian está en Windows y Hermes está en WSL2. El Vault se encuentra en:

```text
K:\Onedrive\material estudo\machine_learning
```

En WSL2, se accede al mismo directorio mediante:

```text
/mnt/k/Onedrive/material estudo/machine_learning
```

---

# OpenViking

## Iniciar el servidor local de OpenViking

Abrir una terminal:

```bash
openviking-server
```

Mantener esta terminal abierta durante toda la parte de OpenViking.

En otra terminal, comprobar el estado del servidor:

```bash
curl http://127.0.0.1:1933/health
```

Resultado esperado:

```text
{"status":"ok","healthy":true,...}
```

No iniciar una segunda instancia de `openviking-server` mientras la primera esté activa.

---

## Validar el cliente de OpenViking

En la segunda terminal:

```bash
ov config validate
```

El resultado esperado es:

```text
Config file   valid
Server        reachable
Auth          accepted
Health        healthy
```

Si la configuración del cliente aún no existe o necesita rehacerse:

```bash
ov config
```

Después, repetir:

```bash
ov config validate
```

En el entorno local utilizado en la lección, el servidor usado por la CLI es:

```text
http://127.0.0.1:1933
```

---

## Confirmar el VLM antes de la ingesta

Antes de importar el Vault:

```bash
ov observer models
```

En esta lección, el VLM utilizado por OpenViking es Codex con el modelo Terra.

Este comando se utiliza para comprobar el modelo de generación activo. El embedding local configurado en `ov.conf` no necesita aparecer en esta lista.

---

## Comprobar OpenViking en Hermes

Comprobar el Perfil `aluno`:

```bash
hermes -p aluno memory status
```

El proveedor activo debe ser:

```text
openviking
```

---

## Importar el Vault a OpenViking

Ejecutar:

```bash
ov add-resource "/mnt/k/Onedrive/material estudo/machine_learning" \
  --to viking://resources/machine-learning-vault
```

En esta grabación, el Vault se importa una sola vez, con Codex + Terra ya configurado desde el principio.

---

## Supervisar el procesamiento

Durante la ingesta, en otra terminal:

```bash
ov observer queue
```

La cola `Semantic-Nodes` puede mostrar elementos en `Pending` y `In Progress` durante el procesamiento semántico del contenido.

Antes de continuar, esperar a que aparezca:

```text
Pending      0
In Progress  0
Errors       0
```

También es posible comprobar nuevamente los modelos:

```bash
ov observer models
```

No reiniciar el servidor mientras haya procesamiento en curso.

---

## Confirmar la importación en OpenViking

Mostrar el árbol:

```bash
ov tree viking://resources/machine-learning-vault
```

Mostrar el overview:

```bash
ov overview viking://resources/machine-learning-vault
```


Si el overview aún no está disponible, comprobar primero:

```bash
ov observer queue
```

y esperar a que finalice el procesamiento semántico antes de concluir que hubo un fallo.

---

## Probar búsquedas directamente en OpenViking

Búsqueda directa:

```bash
ov find "What is the difference between AI and Machine Learning?" \
  --uri viking://resources/machine-learning-vault
```

Búsqueda relacionando conceptos:

```bash
ov find "What is the relationship between overfitting, validation, and regularization?" \
  --uri viking://resources/machine-learning-vault
```

Si los resultados devuelven contenido del Vault, la ingesta está funcionando.

---

## Probar mediante Hermes con OpenViking

Abrir:

```bash
hermes -p aluno chat
```

Preguntar:

```text
¿Cuál es la diferencia entre IA y Machine Learning?
```

Después:

```text
¿Por qué KNN y K-Means son sensibles a la escala, aunque resuelvan problemas diferentes?
```

Después:

```text
Relacione overfitting, validación y regularización.
```


---



# Hindsight

## Actualización importante antes de continuar

Antes de importar el Vault, conviene registrar un cambio importante respecto a la Lección 3.

El **24 de septiembre de 2026**, Hindsight dejó de ser tratado como proveedor interno de Hermes y pasó a distribuirse mediante el **catálogo de plugins** de Hermes.

Durante esta transición, hubo una limitación conocida del modo `local_embedded` en instalaciones gestionadas por el package manager de Hermes.

El **29 de septiembre de 2026**, el catálogo de Hermes se actualizó nuevamente a una versión más reciente de Hindsight, con la indicación de que el modo embebido volvió a funcionar en este tipo de instalación.

Por ello, dependiendo de la versión exacta de Hermes y de la versión del plugin Hindsight instalada en la máquina, el comportamiento puede ser diferente de lo mostrado anteriormente en el curso.

En esta grabación, para partir de una instalación limpia y actual del plugin en el Perfil `lois`, Hindsight se eliminará y se instalará nuevamente desde el catálogo oficial de Hermes.

---

## Eliminar Hindsight del Perfil `lois`

Ejecutar:

```bash
hermes -p lois plugins remove hindsight
```

Después de que el comando confirme que el plugin fue eliminado y que el proveedor fue restablecido, continuar directamente con la reinstalación.

---

## Instalar nuevamente Hindsight desde el catálogo oficial

Ejecutar:

```bash
hermes -p lois plugins install hindsight
```

Si el instalador pregunta si desea habilitar el plugin en el Perfil, responder:

```text
y
```

Si pregunta si Hermes debe preparar las dependencias mediante el package manager, responder:

```text
y
```

Después, validar:

```bash
hermes -p lois memory status
```

Si el plugin aparece instalado, pero el estado muestra:

```text
Provider: (none - built-in only)
```

esto significa que el plugin se instaló correctamente, pero aún no se ha seleccionado como proveedor activo del Perfil `lois`.

Activarlo manualmente:

```bash
hermes -p lois config set memory.provider hindsight
```

Después, comprobar nuevamente:

```bash
hermes -p lois memory status
```

El resultado esperado es:

```text
Provider: hindsight
Plugin: installed ✓
Status: available ✓
hindsight ← active
```

---

## Cómo se utilizará Hindsight en esta lección

En esta lección, Hindsight se utilizará en modo `local_external`.

Esto significa que hay dos partes separadas:

1. el servidor local de Hindsight, ejecutándose en `http://127.0.0.1:8888`;
2. la CLI `hindsight`, utilizada para importar el Vault y ejecutar `recall` / `reflect`.

El plugin de Hermes solo conecta el Perfil `lois` al servidor Hindsight. Instalar el plugin de Hermes **no instala automáticamente la CLI `hindsight` en el PATH**.

---


## Comprobar si el servidor Hindsight está activo

Probar:

```bash
curl -sS http://127.0.0.1:8888/health
```

Si el comando queda bloqueado sin devolver respuesta, interrumpirlo con `Ctrl+C` y preparar nuevamente el servidor local con:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

Si el servidor se cierra al iniciarse con un error de CUDA en una GPU NVIDIA antigua, agregar las dos configuraciones al archivo `~/.hindsight/server.env`:

```bash
cat >> ~/.hindsight/server.env <<'EOF'
HINDSIGHT_API_EMBEDDINGS_LOCAL_FORCE_CPU=1
HINDSIGHT_API_RERANKER_LOCAL_FORCE_CPU=1
EOF
```

Comprobar el archivo:

```bash
cat ~/.hindsight/server.env
```

Después, cargar nuevamente el archivo e iniciar el servidor:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

Y probar nuevamente:

```bash
curl -sS http://127.0.0.1:8888/health
```

Resultado esperado:

```json
{"status":"healthy","database":"connected",...}
```

Si el puerto aún no está activo, cargar la configuración e iniciar el servidor:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

En el primer inicio, esperar unos segundos antes de probar `/health`.

Si es necesario, comprobar:

```bash
tail -n 100 ~/.hindsight/daemon.log
```

---

## Instalar la CLI de Hindsight

La CLI es independiente del servidor `hindsight-api` y también es independiente del plugin de Hermes.

Comprobar primero:

```bash
hindsight --help
```

Si aparece:

```text
hindsight: command not found
```

instalar la CLI oficial:

```bash
curl -fsSL https://hindsight.vectorize.io/get-cli | bash
```

Después, recargar el shell:

```bash
source ~/.bashrc
```

Y confirmar:

```bash
hindsight --help
```

---

## Configurar la CLI para el servidor local

Después de que el servidor Hindsight esté activo y la comprobación de estado responda correctamente, apuntar la CLI `hindsight` a ese servidor.

Para la sesión actual de la terminal:

```bash
export HINDSIGHT_API_URL=http://localhost:8888
```

También es posible guardar la URL usando la propia CLI:

```bash
hindsight configure --api-url http://127.0.0.1:8888
```

---

## Conectar el Perfil `lois` a Hindsight

Con el servidor activo y la CLI ya apuntando a él, activar Hindsight como proveedor del Perfil `lois`:

```bash
hermes -p lois config set memory.provider hindsight
```

Validar:

```bash
hermes -p lois memory status
```

El resultado esperado es:

```text
Provider: hindsight
Plugin: installed ✓
Status: available ✓
hindsight ← active
```

De esta forma, la CLI `hindsight` y el Perfil `lois` pasan a utilizar el mismo servidor Hindsight en `127.0.0.1:8888`.

---

---

## Importar el Vault a Hindsight

Usando el `bank_id` predeterminado:

```bash
hindsight bank create hermes

```

Crear el bank antes de la importación es necesario porque `retain-files` guarda los archivos dentro de un bank existente. Si el bank aún no existe, la CLI devuelve `404: Bank 'hermes' not found`.

Después, importar el Vault:

```bash
hindsight memory retain-files hermes "/mnt/k/Onedrive/material estudo/machine_learning/"
```

El comando `retain-files` acepta directorios y procesa los archivos de forma recursiva.

Este comando depende de que la CLI `hindsight` esté instalada y configurada para `http://127.0.0.1:8888`.

Hindsight convierte los archivos en documentos y extrae memorias a partir del contenido.

---

## Confirmar la importación en Hindsight

Realizar una recuperación directa:

```bash
hindsight memory recall hermes "What is the difference between AI and Machine Learning?"
```

Probar una relación entre conceptos:

```bash
hindsight memory recall hermes "What is the relationship between overfitting, validation, and regularization?"
```

Probar una síntesis:

```bash
hindsight memory reflect hermes "Create a map relating AI, Machine Learning, Neural Networks, Deep Learning, and Transformers."
```

Si el contenido del Vault aparece en los resultados, la ingesta está funcionando.

---

## Probar mediante Hermes con Hindsight

Abrir:

```bash
hermes -p lois chat
```

Repetir las mismas preguntas utilizadas en el Perfil `aluno`:

```text
¿Cuál es la diferencia entre IA y Machine Learning?
```

```text
¿Por qué KNN y K-Means son sensibles a la escala, aunque resuelvan problemas diferentes?
```

```text
Relacione overfitting, validación y regularización.
```

---

# Preguntas para comparar los dos proveedores

## Recuperación directa

```text
¿Cuál es la diferencia entre IA y Machine Learning?
```

```text
¿Qué caracteriza un problema de regresión?
```

```text
¿Cuál es el papel de k en KNN?
```

```text
¿Qué hace el bias en una neurona artificial?
```

```text
¿Qué significa una época en el entrenamiento de redes neuronales?
```

## Relaciones entre conceptos

```text
¿Por qué la preparación de los datos afecta la calidad de la evaluación de un modelo?
```

```text
¿Cuál es la relación entre overfitting, validación y regularización?
```

```text
¿Por qué KNN y K-Means son sensibles a la escala, aunque resuelvan problemas diferentes?
```

```text
¿Cómo aparece el concepto de generalización tanto en regresión como en redes neuronales?
```

```text
¿Cuál es la relación entre el umbral de decisión y precision/recall?
```

## Comparaciones

```text
Compare regresión y clasificación.
```

```text
Compare bagging y boosting.
```

```text
Compare K-Means y DBSCAN.
```

```text
Compare RNN, LSTM/GRU y Transformer.
```

```text
Compare MAE y RMSE y diga en qué situación uno puede ser preferible al otro.
```

## Preguntas que requieren cuidado

```text
¿Un R² de 0,90 significa 90% de predicciones correctas?
```

```text
¿Una accuracy del 99% garantiza que un clasificador es excelente?
```

```text
¿PCA con 95% de varianza explicada garantiza 95% de accuracy?
```

```text
¿Un cluster descubierto por el algoritmo es automáticamente un perfil real?
```

```text
¿Un coeficiente de regresión prueba causalidad?
```

## Síntesis larga

```text
Describa un pipeline completo de Machine Learning, desde la preparación de los datos hasta la evaluación.
```

```text
Explique cómo un modelo puede obtener resultados excelentes en entrenamiento y fallar en producción.
```

```text
Cree un mapa relacionando IA → Machine Learning → Redes Neuronales → Deep Learning → Transformers.
```

```text
Explique por qué el mejor modelo depende del problema, de la métrica y del costo de los errores.
```

```text
¿Qué conceptos aparecen repetidamente a lo largo de los temas?
```

---

## Eliminar un Vault importado de OpenViking

Si desea eliminar un Vault ya importado en OpenViking, use:

```bash
ov rm -r viking://resources/machine-learning-vault
```

Después, si desea confirmar que fue eliminado:

```bash
ov tree viking://resources
```

Sustituya `machine-learning-vault` por el nombre del recurso que desea eliminar.

---


# Diferencia importante

## Obsidian

Obsidian organiza los archivos Markdown para lectura y edición humanas.

## OpenViking

OpenViking importa los archivos como recursos dentro de una jerarquía `viking://` y permite búsqueda, lectura y navegación estructuradas.

## Hindsight

Hindsight importa los archivos como documentos y extrae memorias que pueden recuperarse y relacionarse mediante el mecanismo de memoria.

Tener un archivo dentro del Vault no significa que ya esté disponible en ninguno de los dos proveedores.

Realice siempre la ingesta antes de las pruebas.

---

# Fuentes oficiales

Hermes Agent — Proveedores de memoria:

https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers

OpenViking — Gestión de recursos:

https://docs.openviking.ai/en/api/02-resources

OpenViking — Inicio rápido:

https://docs.openviking.ai/en/getting-started/02-quickstart

OpenViking — Configuración de la CLI:

https://docs.openviking.ai/en/getting-started/05-cli-setup

OpenViking — Guía de configuración (VLM, timeout, reintentos y concurrencia):

https://github.com/volcengine/OpenViking/blob/main/docs/en/guides/01-configuration.md

Hindsight — Referencia de la CLI:

https://github.com/vectorize-io/hindsight/blob/main/skills/hindsight-docs/references/sdks/cli.md

Hindsight — Retain Files:

https://github.com/vectorize-io/hindsight/blob/main/skills/hindsight-docs/references/developer/api/retain.md


OpenViking — discusión reciente sobre la configuración del cliente:

https://github.com/volcengine/OpenViking/issues/3650

OpenViking — discusión reciente sobre `ov.conf` y `ovcli.conf`:

https://github.com/volcengine/OpenViking/issues/3125


Hindsight — integración con Hermes:

https://github.com/NousResearch/hermes-agent/blob/main/plugins/memory/hindsight/README.md



---

# Si Hindsight presenta problemas después de una actualización de Hermes

> Use esta sección solo si el Perfil continúa apuntando a `hindsight`, pero el modo local embebido deja de estar disponible o entra en un ciclo de actualización. En el entorno de esta lección, la solución fue ejecutar Hindsight como servidor local externo y hacer que el Perfil `lois` apunte a él.

## 1. Confirmar el estado del Perfil

```bash
hermes -p lois memory status
```

Si el plugin está instalado, pero Hindsight no está disponible en modo local embebido, siga los pasos a continuación.

## 2. Preparar Hindsight local externo

El servidor se ejecutará localmente en:

```text
http://127.0.0.1:8888
```

Crear la carpeta de configuración:

```bash
mkdir -p ~/.hindsight
umask 077
```

Registrar la clave de MiniMax sin mostrarla en pantalla:

```bash
read -s -p "Paste the NEW MiniMax key: " MM_KEY
echo
```

Crear el archivo de entorno usando MiniMax-M3:

```bash
cat > ~/.hindsight/server.env <<EOF
HINDSIGHT_API_LLM_PROVIDER=minimax
HINDSIGHT_API_LLM_MODEL=MiniMax-M3
HINDSIGHT_API_LLM_API_KEY=$MM_KEY
EOF
unset MM_KEY
chmod 600 ~/.hindsight/server.env
```

Comprobar únicamente el proveedor y el modelo, sin mostrar la clave:

```bash
grep -E 'HINDSIGHT_API_LLM_PROVIDER|HINDSIGHT_API_LLM_MODEL' ~/.hindsight/server.env
```

Resultado esperado:

```text
HINDSIGHT_API_LLM_PROVIDER=minimax
HINDSIGHT_API_LLM_MODEL=MiniMax-M3
```

## 3. Iniciar el servidor Hindsight

Primero, comprobar si el puerto 8888 ya está en uso:

```bash
ss -ltnp | grep 8888
```

Si no hay ningún proceso en el puerto, cargar el entorno e iniciar:

```bash
set -a
source ~/.hindsight/server.env
set +a
uvx hindsight-api --daemon
```

En el primer inicio, Hindsight puede tardar unos segundos en cargar los modelos locales y PostgreSQL embebido.

Probar:

```bash
curl -sS http://127.0.0.1:8888/health
```

Resultado esperado:

```json
{"status":"healthy","database":"connected",...}
```

Si la prueba se ejecuta demasiado pronto y falla, comprobar el log:

```bash
tail -n 100 ~/.hindsight/daemon.log
```

Buscar:

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8888
```

## 4. Cambiar el Perfil `lois` a `local_external`

Hacer una copia de seguridad de la configuración:

```bash
cp ~/.hermes/profiles/lois/hindsight/config.json ~/.hermes/profiles/lois/hindsight/config.json.bak
```

Cambiar únicamente el modo y la URL:

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

## 5. Validar en Hermes

```bash
hermes -p lois memory status
```

El resultado correcto debe mostrar:

```text
Provider: hindsight
Plugin: installed ✓
Status: available ✓
hindsight ← active
```

A partir de este punto, Hermes utiliza Hindsight local mediante la API en `127.0.0.1:8888`, sin depender del modo `local_embedded`.

> Seguridad: nunca coloque la clave de MiniMax directamente en documentación, GitHub, capturas de pantalla o vídeo. Si una clave se muestra accidentalmente, revóquela y genere otra.
