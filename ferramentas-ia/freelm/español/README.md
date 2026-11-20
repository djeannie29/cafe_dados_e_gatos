# freelm en español — guía completa y accesible

> **Traducción y adaptación explicativa independiente**, preparada para la comunidad Café com Dados & Gatos a partir del [README oficial de freelm](https://github.com/shihabshahrier/freelm) y del material revisado el 20 de noviembre de 2026. **No es documentación oficial** ni implica el respaldo de los mantenedores. Se conservaron los comandos, los nombres de las API y las variables de entorno; se adaptaron las explicaciones y ejemplos al español.
>
> **Licencia del proyecto original:** MIT, © Shahriar Labs. Fuente y licencia: [repositorio oficial](https://github.com/shihabshahrier/freelm) · [LICENSE](https://github.com/shihabshahrier/freelm/blob/main/LICENSE).
>
> **Estado de las pruebas:** el 20 de noviembre de 2026 se realizaron varias pruebas de la CLI y de integración en Ubuntu/WSL2. Los resultados observados figuran al final. **No** se ha demostrado un failover provocado por un error real.

## Índice

- [¿Qué es freelm?](#qué-es-freelm)
- [Inicio rápido sin Python](#inicio-rápido-sin-python)
- [Cómo obtener y configurar claves gratuitas](#cómo-obtener-y-configurar-claves-gratuitas)
- [Comandos principales de la CLI](#comandos-principales-de-la-cli)
- [Uso de freelm con herramientas compatibles con OpenAI](#uso-de-freelm-con-herramientas-compatibles-con-openai)
- [Proveedores gratuitos y sus límites](#proveedores-gratuitos-y-sus-límites)
- [Cómo funciona el failover](#cómo-funciona-el-failover)
- [Cómo elegir modelos](#cómo-elegir-modelos)
- [Opciones de configuración](#opciones-de-configuración)
- [Ejemplos de Python y JavaScript](#ejemplos-de-python-y-javascript)
- [Comparación con otras herramientas](#comparación-con-otras-herramientas)
- [Preguntas frecuentes y solución de problemas](#preguntas-frecuentes-y-solución-de-problemas)
- [Seguridad, costos y límites](#seguridad-costos-y-límites)
- [Fuentes y resultados de las pruebas](#fuentes-y-resultados-de-las-pruebas)

## ¿Qué es freelm?

**freelm** es una biblioteca y herramienta de línea de comandos (CLI) que combina **cuotas gratuitas de distintos proveedores de modelos de lenguaje**. Una sola solicitud puede seleccionar modelos ofrecidos por Gemini, Groq, OpenRouter, Cloudflare Workers AI, Z.ai, Cohere, Mistral, NVIDIA NIM, Kilo Gateway y otros servicios compatibles.

En lugar de implementar una integración diferente para cada servicio, freelm ofrece una interfaz compatible con OpenAI. Según su desarrollador, permite:

- Descubrir modelos gratuitos que están disponibles en ese momento.
- Cambiar de modelo, clave o proveedor cuando falla un intento (**failover**).
- Considerar los límites de solicitudes y las cuotas gratuitas.
- Iniciar un intento alternativo si un proveedor tarda demasiado.
- Funcionar como biblioteca Python, biblioteca JavaScript/TypeScript, CLI o API local `/v1` opcional.

**Lo que freelm NO es:** no es un modelo de IA, no descarga automáticamente pesos de modelos grandes, no ejecuta la inferencia localmente ni garantiza un uso gratuito ilimitado. Las preguntas son procesadas por **proveedores externos**.

**Conceptos importantes:**
- **Proveedor:** empresa o servicio que ofrece acceso a un modelo (por ejemplo, Groq).
- **Modelo:** sistema de IA específico que procesa la solicitud.
- **Clave de API:** credencial secreta que permite acceder a la cuenta del proveedor.
- **Enrutamiento:** decisión sobre dónde enviar cada solicitud.
- **Failover:** cambio a otra opción cuando la primera no puede atender la solicitud.
- **429:** error HTTP que indica que se ha superado un límite de solicitudes.
- **Endpoint:** dirección mediante la cual otro programa se comunica con un servicio.

## Inicio rápido sin Python

Este es el procedimiento más sencillo para nuestro laboratorio con **Ubuntu/WSL2**. El paquete JavaScript requiere **Node.js 20 o superior**.

### Comprobar Node.js

```bash
node --version
npm --version
```

Estos comandos consultan las versiones de Node.js y npm; no son comandos específicos de freelm.

### Probar sin clave y sin instalación global

```bash
npx freelm chat "¡Hola! Explica en una frase qué es un modelo de lenguaje."
```

El README oficial documenta `npx freelm chat "hello"`. Cuando no hay claves configuradas, freelm indica que puede utilizar rutas públicas anónimas de Kilo Gateway y OVHcloud. **Sus límites son bajos y estos servicios pueden registrar las preguntas. Nunca envíes datos personales o confidenciales.**

### Instalar el paquete localmente como indica el autor

```bash
mkdir -p ~/testes-freelm
cd ~/testes-freelm
npm install freelm
```

El README indica `npm install freelm`. **No** presenta `npm install -g freelm` como método de instalación. Por eso usamos `npx freelm` para ejecutar la CLI instalada en la carpeta.

### Consultar los comandos y modelos

```bash
npx freelm --help
npx freelm models
npx freelm chat "Explica qué significa failover en una frase." --model chat:fast --stream
```

## Cómo obtener y configurar claves gratuitas

No es obligatorio contar con una clave propia para probar las rutas anónimas, pero resulta recomendable para obtener un acceso más predecible y para comprobar el cambio entre **proveedores distintos**.

Portales oficiales:
- **Gemini / Google AI Studio:** https://aistudio.google.com/apikey
- **Groq:** https://console.groq.com/keys
- **OpenRouter:** https://openrouter.ai/keys

**Antes de crear una clave, comprueba que tu cuenta dispone de un plan gratuito y qué modelos siguen siendo gratuitos.** Los límites del README pueden haber cambiado.

### Configurar la clave de Gemini en Ubuntu

Pausa la grabación de pantalla antes de introducirla:

```bash
read -rsp "Clave de Gemini: " GEMINI_API_KEY; echo
export GEMINI_API_KEY
```

### Configurar la clave de Groq

```bash
read -rsp "Clave de Groq: " GROQ_API_KEY; echo
export GROQ_API_KEY
```

### Configurar la clave de OpenRouter

```bash
read -rsp "Clave de OpenRouter: " OPENROUTER_API_KEY; echo
export OPENROUTER_API_KEY
```

`read -s` impide que la clave se muestre mientras se introduce. Las variables exportadas quedan disponibles en la sesión actual de la terminal y en los procesos iniciados desde ella. **Nunca subas claves a GitHub, las incluyas en scripts públicos ni las muestres durante una grabación.**

### Verificar conexiones y modelos

```bash
npx freelm doctor
npx freelm models
npx freelm chat "Explica la diferencia entre proveedor y modelo." --model chat:fast --stream
```

`doctor` realiza una pequeña solicitud real para comprobar las claves configuradas. El README incluye ejemplos de éxito y de errores de autenticación, como HTTP 401.

## Comandos principales de la CLI

| Comando en Ubuntu con instalación local | Para qué sirve |
|---|---|
| `npx freelm chat "Hola"` | Hacer una pregunta desde la terminal |
| `npx freelm chat "Hola" --model chat:fast --stream` | Priorizar velocidad y mostrar la respuesta en flujo |
| `npx freelm doctor` | Verificar claves y diagnosticar problemas |
| `npx freelm doctor --json` | Obtener el diagnóstico en JSON |
| `npx freelm models` | Consultar los modelos disponibles |
| `npx freelm models --provider groq` | Filtrar modelos por proveedor |
| `npx freelm health` | Consultar el estado de las claves en el proceso |
| `npx freelm serve` | Iniciar la API local |
| `npx freelm serve --port 4000` | Especificar el puerto del servicio |

`npx` adapta los comandos `freelm ...` del README a una instalación local. Para consultar otros parámetros, utiliza `npx freelm --help`.

## Uso de freelm con herramientas compatibles con OpenAI

El modo servidor es **opcional**. Permite que otra aplicación utilice freelm a través de una API local.

En Ubuntu:

```bash
cd ~/testes-freelm
npx freelm serve
```

Según el desarrollador, la dirección predeterminada es:

```text
http://127.0.0.1:4000/v1
```

El identificador general del modelo es `auto`.

En **otra terminal**, consulta los modelos:

```bash
curl -s http://127.0.0.1:4000/v1/models
```

Envía una pregunta:

```bash
curl -s http://127.0.0.1:4000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Di: la conexión local funciona."}]
  }'
```

### Integraciones mencionadas en el README original

| Herramienta | Configuración descrita por el proyecto |
|---|---|
| **OpenAI SDK** | `base_url="http://127.0.0.1:4000/v1"` y `api_key="freelm"` (ejemplo local) |
| **LangChain** | `ChatOpenAI(base_url="http://127.0.0.1:4000/v1", api_key="freelm", model="auto")` |
| **LlamaIndex** | `OpenAILike(api_base="http://127.0.0.1:4000/v1", api_key="freelm", model="auto", is_chat_model=True)` |
| **Vercel AI SDK** | `createOpenAICompatible({ name: "freelm", baseURL: "http://127.0.0.1:4000/v1" })("auto")` |
| **Continue** | Proveedor `openai`, `apiBase` local y modelo `auto` |
| **Cline / Roo Code** | Proveedor "OpenAI Compatible", URL local y modelo `auto` |
| **OpenCode** | Proveedor `@ai-sdk/openai-compatible` que utiliza la URL local |
| **OpenClaw** | `models.providers.freelm`, API `openai-completions` y `freelm/auto` incluido entre los modelos permitidos |
| **Hermes Agent** | `hermes model` → endpoint personalizado; URL local y modelo `auto` |
| **Aider** | `aider --openai-api-base http://127.0.0.1:4000/v1 --openai-api-key freelm --model openai/auto` |
| **Open WebUI** | Ejemplo del autor en Docker con `http://host.docker.internal:4000/v1` |
| **n8n** | Credencial de OpenAI con la URL base local |

**Una compatibilidad anunciada no equivale a una prueba exitosa.** No todos los modelos gratuitos admiten una ventana de contexto suficiente, llamadas a herramientas, visión o programación. El README advierte, por ejemplo, que Hermes puede necesitar un modelo con contexto largo. El README original menciona el antiguo Roo Code; nuestra prueba práctica utilizó **Zoo Code**, según los resultados finales.

### Configuración de OpenCode publicada en el README

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

Es un **fragmento de configuración**, no necesariamente un archivo completo para sustituir la configuración actual del usuario.

### Docker (alternativa oficial)

El autor también presenta:

```bash
docker run --rm -p 4000:4000 -e GEMINI_API_KEY=... -e FREELM_SERVER_KEY=change-me ghcr.io/shihabshahrier/freelm
```

Esos valores son marcadores de ejemplo del README, **no un comando listo para ejecutar con secretos reales**. Publicar puertos con Docker puede hacer que el servicio sea accesible fuera de localhost. Se requiere autenticación y protección de red. **Nuestro laboratorio no necesitó Docker.**

## Proveedores gratuitos y sus límites

Esta tabla resume el material original. **Los planes, modelos y cuotas pueden cambiar; compruébalos en cada proveedor.**

| Servicio | Variable de entorno | Observaciones del desarrollador |
|---|---|---|
| Google AI Studio (Gemini) | `GEMINI_API_KEY` | Plan gratuito con límites por modelo; los modelos Pro pueden no tener cuota gratis |
| Groq | `GROQ_API_KEY` | Los límites gratuitos dependen del modelo; no confundir **Groq** con **Grok** |
| OpenRouter | `OPENROUTER_API_KEY` | Utilizar rutas identificadas como `:free` o `openrouter/free` |
| Cloudflare Workers AI (beta) | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | Cuota gratuita medida en Neurons; revisar permisos del token |
| Z.ai / GLM (beta) | `ZAI_API_KEY` | Algunos modelos Flash se describen como gratuitos; otros pueden ser de pago |
| Cohere (beta) | `COHERE_API_KEY` | Claves de prueba; limitaciones de uso no comercial |
| Kilo Gateway | `KILO_API_KEY` (opcional) | Existen rutas anónimas, con cuotas y límites reducidos |
| OVHcloud AI Endpoints | Ninguna para rutas anónimas | Ruta anónima de respaldo con límites bajos |
| Cerebras | `CEREBRAS_API_KEY` | Según el README, ya no es permanentemente gratuito; puede requerir tarjeta/créditos de prueba |
| Mistral | `MISTRAL_API_KEY` | Plan Experiment con límites bajos |
| NVIDIA NIM | `NVIDIA_API_KEY` | Créditos de prueba gratuitos que pueden agotarse |

El autor marca algunos proveedores incorporados en la versión 0.5.0 como **beta**, porque en la fecha del README no todos habían sido comprobados con claves reales. Según el texto original, las listas internas de modelos de respaldo se volvieron a revisar el **9 de octubre de 2026**.

### Varias claves del mismo proveedor

El README explica que se pueden separar claves con comas en una variable como `GROQ_API_KEY` o usar variables con el patrón `FREELM_<PROVIDER>_KEYS`. Eso no elimina cuotas ni permite incumplir las políticas de cada servicio.

### Uso de rutas sin clave

La biblioteca documenta:
- `keyless=True`: incluir rutas anónimas como último recurso;
- `keyless="auto"`: utilizarlas cuando no haya claves configuradas;
- `FREELM_KEYLESS=1|auto|0`: control equivalente mediante variable de entorno.

## Cómo funciona el failover

El objetivo es que un error aislado de un proveedor no arruine toda la solicitud. Según el README:

| Situación | Comportamiento descrito |
|---|---|
| **429** — límite de solicitudes | Cambiar clave, modelo o proveedor, respetando cuotas |
| **401/402** — credencial, autorización o facturación | Desactivar la clave problemática |
| **5xx** — fallo del proveedor | Aplicar espera progresiva (*backoff*) y un disyuntor (*circuit breaker*) |
| **Timeout / lentitud** | Iniciar un intento alternativo tras un retraso adaptable |
| **404/410** — modelo retirado | Excluir temporalmente ese modelo |
| **Parámetro no admitido** | Probar otro proveedor cuando corresponda |
| **Todas las rutas agotadas o caídas** | Mostrar un error explicativo como `NoProvidersAvailable` |

### Selección inteligente

La estrategia predeterminada `smart` utiliza prioridades y latencia observada. Las mediciones pierden vigencia con el tiempo, para no depender eternamente de resultados antiguos. El mecanismo de solicitudes competidoras (*hedge*) puede reducir esperas cuando un proveedor se queda bloqueado.

El texto del proyecto presenta ejemplos de unos **3 segundos para una respuesta en flujo bloqueada y 6 segundos para un proveedor lento**, basados en simulaciones del propio desarrollador. **No son garantías para todas las instalaciones.** Consulta los [benchmarks del proyecto](https://github.com/shihabshahrier/freelm/tree/main/benchmarks).

### Cómo demostrar el failover en un vídeo

Recibir una respuesta **no basta** para afirmar que hubo failover. Es necesario mostrar:
- qué proveedor se intentó primero;
- qué error o demora ocurrió;
- qué proveedor terminó atendiendo la solicitud.

El README documenta eventos `attempt`, `hedge`, `success`, `error`, `wait` y `discovery` mediante callbacks de la biblioteca. **No describe la CLI como un registro exhaustivo de auditoría.** Si la CLI no ofrece los detalles necesarios, se debe explicar la limitación o crear una prueba instrumentada en Node.js por separado.

## Cómo elegir modelos

| Identificador | Significado |
|---|---|
| `auto` o `chat` | Elegir automáticamente un modelo de conversación |
| `chat:fast` | Priorizar modelos rápidos |
| `chat:large` | Priorizar modelos grandes |
| `chat:small` | Priorizar modelos pequeños |
| `chat:tools` | Seleccionar modelos con llamadas a herramientas |
| `vision` | Seleccionar modelos con capacidad de visión |
| `reasoning` | Priorizar modelos de razonamiento |
| `vendor/model-id` | Solicitar un modelo específico |
| `["vendor/id", "chat:fast"]` | Establecer una secuencia ordenada de respaldo |

El README también menciona `prefer=[...]`, prioridades de modelos/proveedores y diferencias entre modelos convencionales y de razonamiento. Un `max_tokens` demasiado bajo puede dar respuestas vacías en modelos de razonamiento; el autor sugiere **128 tokens o más** en esos casos, o utilizar `auto`.

## Opciones de configuración

Opciones de la biblioteca descritas en el README:

| Opción | Valor predeterminado | Qué controla |
|---|---|---|
| `strategy` | `smart` | `smart`, `priority`, `round_robin`, `quota_aware` o `latency` |
| `hedge` | `True` | Intentos simultáneos cuando una respuesta es lenta |
| `max_attempts` | `12` | Número máximo de intentos por solicitud |
| `timeout` | `60` | Tiempo máximo total en segundos |
| `wait` | `False` | Esperar a que haya cuota en lugar de fallar de inmediato |
| `max_wait` | `20` | Espera máxima del ejemplo |
| `on_event` | Sin configurar | Callback de eventos de enrutamiento |
| `persist` | `False` | Conservar cuotas y períodos de espera entre ejecuciones |

También aparecen `tier`, `priority`, `prefer`, `models`, `rpm`, `rpd`, `discover`, `free_only` y `cache_ttl`.

El README describe `FREELM_PERSIST=1` para activar la persistencia del estado en `~/.cache/freelm/state.json`, con permisos restringidos y hashes de claves en lugar de secretos en texto claro. Comprueba el comportamiento en el entorno concreto antes de activar esta función.

**Advertencia:** no desactives `free_only` ni habilites planes de pago sin conocer las reglas de facturación.

## Ejemplos de Python y JavaScript

Esta sección mantiene las funciones avanzadas de la referencia original. **La instalación sencilla del vídeo no requiere escribir este código.**

### JavaScript / TypeScript

Según el README, el paquete de Node.js no tiene dependencias de ejecución y permite usar `FreeLLM.fromEnv()`:

```javascript
import { FreeLLM } from "freelm";

const llm = FreeLLM.fromEnv();
console.log(await llm.text("Explica qué es failover en una frase."));

for await (const parte of llm.stream("Cuenta del uno al cinco.", {
  signal: AbortSignal.timeout(30_000)
})) {
  process.stdout.write(parte);
}
```

El material original informa compatibilidad con ESM y CommonJS y distintos entornos JavaScript. Consulta la [documentación de JavaScript](https://github.com/shihabshahrier/freelm/tree/main/js).

### Python

El paquete Python requiere **Python 3.9 o superior**, y la instalación documentada es:

```bash
pip install freelm
```

Ejemplo básico:

```python
import freelm

llm = freelm.FreeLLM.from_env()
print(llm.text("Explica failover en una frase."))
```

Configuración explícita de proveedores, según el autor:

```python
from freelm import FreeLLM, GoogleAIStudio, Groq, OpenRouter

llm = FreeLLM(
    [GoogleAIStudio("CLAVE-GEMINI"), Groq("CLAVE-GROQ"), OpenRouter("CLAVE-OPENROUTER")],
    strategy="smart",
)

respuesta = llm.chat(
    [{"role": "user", "content": "Explica failover en una frase."}],
    model="chat:fast",
)
print(respuesta.text, "via", respuesta.provider, respuesta.model)
```

**Las claves indicadas son marcadores de ejemplo. Nunca publiques credenciales verdaderas en el código.**

El README también presenta:
- `llm.stream(...)` para respuestas incrementales;
- `llm.chat(..., tools=[...], tool_choice="auto")` y `r.tool_calls` para llamadas a herramientas;
- `response_format={"type": "json_object"}` para respuestas JSON;
- `AsyncFreeLLM` y `astream(...)` para ejecución asíncrona;
- `stream_chunks()` y `astream_chunks()` para fragmentos compatibles con OpenAI.

### Compatibilidad con el SDK de OpenAI en Python

El proyecto documenta una importación alternativa:

```python
from freelm.compat import OpenAI

client = OpenAI()
r = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "¡Hola!"}],
)
print(r.choices[0].message.content)
```

Según el desarrollador, los objetos de respuesta se parecen a los del SDK de OpenAI e incluyen `model_dump()` y streaming. **La compatibilidad real depende de la versión instalada y las capacidades del modelo seleccionado.**

## Comparación con otras herramientas

**Esta tabla resume la descripción del propio desarrollador de freelm**, no una evaluación comparativa independiente.

| Herramienta o categoría | Diferencia presentada en el README |
|---|---|
| OmniRoute, 9Router, FreeLLMAPI, free-claude-code | Suelen ser gateways que se ejecutan como servicio; freelm puede funcionar solamente como biblioteca |
| freellmpool | Otra biblioteca/proxy; freelm destaca su paquete TypeScript sin dependencias |
| LiteLLM | Alcance mayor, incluidos servicios de pago; freelm se concentra en cuotas gratuitas |
| any-llm, aisuite, llm | Unifican API de proveedores; freelm destaca cuotas, cambios automáticos y descubrimiento de modelos gratuitos |
| OpenRouter | Agregador alojado que también puede ser uno de los proveedores de freelm |
| gpt4free | Utiliza endpoints obtenidos mediante ingeniería inversa; freelm afirma priorizar planes gratuitos oficiales |
| LangChain / LlamaIndex | Frameworks de orquestación que pueden utilizar freelm mediante su API o servidor |

## Preguntas frecuentes y solución de problemas

### ¿freelm es realmente gratuito?

La **biblioteca es de código abierto y tiene licencia MIT**, pero el consumo depende de la cuenta y el plan de cada proveedor. El README menciona protecciones para modelos de pago de OpenRouter, Kilo y Z.ai y advierte que opciones como `tier="tier1"` o `free_only=False` pueden modificar la facturación. Los planes de pago de Cloudflare, las claves de producción de Cohere y otros servicios pueden generar cargos.

### ¿Puede responder sin una clave de API?

Según el autor, sí, mediante rutas anónimas de Kilo Gateway y OVHcloud. Pueden no estar disponibles, tienen menos cuota y **pueden registrar las preguntas**.

### ¿Por qué dejó de funcionar un modelo gratuito?

Es posible que lo hayan retirado, se haya agotado la cuota, la clave haya caducado o el servicio esté caído. El README afirma que freelm intenta redirigir la petición y excluye temporalmente modelos retirados o sobrecargados.

### ¿Cómo evitar HTTP 429?

No existe una forma legítima de eliminar las cuotas. El proyecto propone distribuir solicitudes entre claves y proveedores permitidos, respetando límites por minuto y por día. Cumple las condiciones de cada servicio.

### ¿Una respuesta correcta demuestra que hubo failover?

No. Solo demuestra que **alguna ruta respondió**. Para probar failover se necesita evidenciar un primer intento fallido o bloqueado y el éxito de otro intento.

### ¿freelm recibe mis preguntas?

El proyecto informa que las solicitudes llegan a los proveedores externos configurados y que freelm no incorpora telemetría propia. Eso **no elimina el procesamiento, los registros ni las políticas de conservación de datos de los proveedores**.

### ¿Qué hago si no responde la API local?

Comprueba que `npx freelm serve` continúe ejecutándose, que la terminal correcta tenga las variables exportadas y que el puerto 4000 esté disponible. No publiques la API en internet como solución rápida.

### ¿Puede Windows conectarse a freelm en WSL2?

Con el servidor de Ubuntu activo, prueba lo siguiente en PowerShell:

```powershell
curl.exe http://127.0.0.1:4000/v1/models
```

La comunicación mediante localhost está disponible en configuraciones compatibles de WSL2. Depende del modo de red de WSL y no implica que otros equipos puedan acceder al servicio.

### ¿Cómo detenerlo o desinstalarlo?

Pulsa **Ctrl+C** en la terminal del servidor. Para desinstalar el paquete local:

```bash
cd ~/testes-freelm
npm uninstall freelm
```

### ¿Dónde se explican los errores específicos?

El README remite a la [referencia de errores del desarrollador](https://shahriarlabs.com/products/freelm/errors/), con ejemplos de:
- Gemini 429 `RESOURCE_EXHAUSTED`;
- Gemini "User location is not supported";
- Gemini "API key not valid";
- Gemini 503;
- Cuotas de modelos gratis de OpenRouter;
- OpenRouter sin endpoints compatibles con llamadas a herramientas;
- Límites de Groq;
- Mistral 429;
- Z.ai 1302;
- Respuestas vacías de modelos de razonamiento.

## Seguridad, costos y límites

- **Nunca reveles claves de API**, ni siquiera en los registros de errores.
- Las rutas anónimas y los proveedores externos no son lugares apropiados para enviar secretos.
- Antes de usar un modelo "gratis", comprueba **tu cuenta, el modelo concreto y sus condiciones de facturación**.
- Mantén `freelm serve` accesible solo de forma local. Para exponer `--host 0.0.0.0`, configura `--api-key`, firewall y controles adecuados.
- Al conectar agentes de programación, comprueba el contexto, las llamadas a herramientas y las capacidades reales del modelo.
- No presentes los benchmarks del desarrollador como resultados que nosotros hayamos reproducido.
- No consideres `free_only` una garantía universal contra cargos en cuentas con facturación activada.

## Fuentes y resultados de las pruebas

**Material original:** [freelm — README oficial en inglés](https://github.com/shihabshahrier/freelm), consultado el 20 de noviembre de 2026.

**Referencias:**
- [Repositorio original](https://github.com/shihabshahrier/freelm)
- [Licencia MIT](https://github.com/shihabshahrier/freelm/blob/main/LICENSE)
- [README de JavaScript](https://github.com/shihabshahrier/freelm/tree/main/js#readme)
- [Benchmarks del autor](https://github.com/shihabshahrier/freelm/tree/main/benchmarks)
- [Referencia de errores del autor](https://shahriarlabs.com/products/freelm/errors/)
- [Paquete npm](https://www.npmjs.com/package/freelm)
- [Paquete PyPI](https://pypi.org/project/freelm/)

### Observaciones del laboratorio Café com Dados & Gatos (20/11/2026)

Las observaciones proceden de capturas de pantalla de la sesión **Ubuntu/WSL2** de la autora del canal, no de benchmarks independientes.

| Prueba | Resultado observado |
|---|---|
| Node.js y npm | **Funcionaron** — Node.js 22.23.2; npm 12.0.2 |
| freelm | **Funcionó** — versión 0.5.2 mediante `npx` |
| Chat sin clave de API | **Funcionó** — un modelo gratuito de Kilo Gateway respondió en portugués |
| Descubrimiento de modelos | **Funcionó** — se listaron varios modelos de distintos proveedores |
| `doctor` con claves configuradas | **Funcionó** — finalmente se validaron 3 de 3 claves (Gemini, Groq y OpenRouter) |
| Rutas anónimas | **Funcionaron en el diagnóstico** — Kilo Gateway y OVHcloud |
| API local compatible con OpenAI | **Funcionó** — el servidor mostró solicitudes a `/v1/chat/completions` con HTTP 200 |
| Integración con Zoo Code | **Funcionó** — el agente creó una página Hello World en `index.html` y se visualizó en VS Code |
| Distintos modelos en las solicitudes | **Observado** — los registros mostraron respuestas de Nemotron y Gemini |
| Failover automático provocado por error | **No demostrado** — los registros mostraron solicitudes exitosas, no un primer intento fallido |

**Atribución:** traducción, reorganización y explicaciones independientes para facilitar el aprendizaje. Software y documentación original de freelm: Shahriar Labs. Antes de publicar, comprueba de nuevo los comandos, la disponibilidad de modelos, las condiciones de los proveedores y el README actualizado.
