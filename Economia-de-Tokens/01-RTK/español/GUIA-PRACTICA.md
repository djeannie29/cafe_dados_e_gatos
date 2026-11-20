# RTK en Ubuntu/WSL2 — Guía práctica y resultados medidos

**Café com Dados & Gatos · Serie Ahorro de Tokens · Episodio 01 · Noviembre de 2026**

Esta guía documenta la instalación y las pruebas del **RTK (Rust Token Killer)** con **Codex CLI (GPT-6.1 Sol, razonamiento Medium)** y **Claude Code (MiniMax M3.1 Flash)**. En cada agente desarrollamos un sitio web de cuatro páginas una vez **sin RTK** y otra **con RTK**.

**Advertencia metodológica:** hicimos una ejecución por condición. Los resultados son exploratorios y no demuestran causalidad. El porcentaje de `rtk gain` se refiere a la compresión de la **salida de determinados comandos**, no al ahorro global de tokens ni al costo real de una sesión.

## Documentación oficial

- [Proyecto RTK](https://github.com/rtk-ai/rtk)
- [Instalación de RTK](https://www.rtk-ai.app/docs/getting-started/installation/)
- [Agentes compatibles](https://www.rtk-ai.app/docs/getting-started/supported-agents/)
- [Estadísticas de RTK gain](https://www.rtk-ai.app/docs/analytics/gain/)
- [Hooks de Claude Code](https://code.claude.com/docs/en/hooks)
- [VS Code en WSL](https://code.visualstudio.com/docs/remote/wsl)
- [Codex CLI](https://github.com/openai/codex)
- [Instalación de Claude Code](https://docs.anthropic.com/en/docs/claude-code/getting-started)
- [MiniMax con Claude Code](https://platform.minimax.io/docs/m-plan/claude-code)

## Entorno utilizado

| Elemento | Configuración registrada |
|---|---|
| Sistema | Ubuntu en WSL2 (versión exacta no consolidada) |
| Editor | Visual Studio Code conectado a WSL |
| RTK | 1.2.1 |
| Codex CLI | 0.170.0; GPT-6.1 Sol, Medium |
| Claude Code | Modelo MiniMax M3.1 Flash (versión exacta de Claude no consolidada) |
| Proyecto | «Cafeteria Aurora»: sitio institucional de cuatro páginas |
| Tecnologías | Vite + React + TypeScript, sin backend |
| Diseño experimental | Una ejecución sin RTK y otra con RTK por agente |

Utiliza directorios independientes y sesiones nuevas. Mantén el mismo modelo, instrucciones, permisos, dependencias y criterios de verificación **dentro de cada par**. No interpretes las diferencias entre Codex y Claude como una evaluación comparativa de modelos.

## Preparar VS Code y WSL2

En Windows, instala la extensión **WSL** de Microsoft para VS Code. Abre la paleta de comandos con `F1` y selecciona **WSL: Connect to WSL**.

Desde la terminal de Ubuntu:

```bash
mkdir -p ~/testes-economia-tokens
cd ~/testes-economia-tokens
code .
```

Comprueba la conexión al sistema Linux:

```bash
uname -s
pwd
cat /etc/os-release
code --version
codex --version
claude --version
command -v rtk
```

El comando `uname -s` debe devolver `Linux`. Conviene usar una carpeta dentro de `$HOME`, no `/mnt/c`. En Ubuntu instalado directamente, no necesitas la extensión WSL.

## Instalar RTK

Revisa las instrucciones oficiales vigentes. Descarga y **examina** el instalador antes de ejecutarlo:

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh -o /tmp/rtk-install.sh
less /tmp/rtk-install.sh
```

Si coincide con la documentación oficial:

```bash
sh /tmp/rtk-install.sh
export PATH="$HOME/.local/bin:$PATH"
rtk --version
rtk gain
```

`rtk gain` **no** es un contador de consumo total de tokens de una sesión.

## Instalar Codex CLI y Claude Code si todavía no están disponibles

Una opción de instalación documentada para Codex CLI:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
codex --version
command -v codex
```

Otra opción es `npm install -g @openai/codex`. Utiliza un solo método de instalación y evita actualizar entre las dos condiciones.

En el video, Claude Code se instaló con el instalador nativo de Anthropic:

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
command -v claude
```

Como alternativa existe `npm install -g @anthropic-ai/claude-code`. No utilices `sudo npm install -g`.

Para vincular **MiniMax M Plan / Token Plan** a Claude Code, el asistente oficial permite:

```bash
npx -y mmx-cli@latest agent setup
```

Selecciona Claude Code, configura el tipo de clave de suscripción correcto y revisa la región/endpoint. Reinicia la aplicación después. **Nunca publiques claves privadas**: la clave de suscripción del M Plan es distinta de una clave común de API prepagada.

## Cuatro ejecuciones del experimento

Antes de enviar la solicitud principal, registra el contador inicial con `/status` (Codex) o `/usage` (Claude). Al terminar, registra el contador final de la **misma sesión**. Comprueba los hooks **antes** de capturar la línea de base de la tarea.

### A — Codex sin RTK

```bash
mkdir -p ~/testes-economia-tokens/rtk/codex-sem-rtk
cd ~/testes-economia-tokens/rtk/codex-sem-rtk
codex
```

En Codex, ejecuta `/status`, envía el texto íntegro del proyecto de prueba que aparece más abajo, verifica el sitio/build/pruebas y ejecuta `/status` otra vez. Asegúrate de que no haya un hook RTK activo para este proyecto.

### B — Codex con RTK local

```bash
mkdir -p ~/testes-economia-tokens/rtk/codex-com-rtk
cd ~/testes-economia-tokens/rtk/codex-com-rtk
rtk init --codex --dry-run
```

Examina la vista previa. Si es correcta:

```bash
rtk init --codex
cat .codex/hooks.json
codex
```

La configuración esperada es `PreToolUse` para `Bash`, con `rtk hook codex`. En una prueba real de este episodio, Codex solicitó `ls -la .codex` sin prefijo y Bash recibió `rtk ls -la .codex`: esto verifica la reescritura **de ese comando**, no de toda la sesión. Repite la tarea y guarda `/status` al principio y al final.

En la terminal, fuera de Codex:

```bash
rtk gain
```

### C — Claude Code sin RTK

```bash
mkdir -p ~/testes-economia-tokens/rtk/claude-sem-rtk
cd ~/testes-economia-tokens/rtk/claude-sem-rtk
rtk init --show
claude
```

Comprueba que no exista un hook RTK global ni local en la configuración de Claude. Selecciona MiniMax M3.1 Flash y usa `/usage` antes y después de la solicitud. Registra entrada, salida, caché, solicitudes, duración y errores.

### D — Claude Code con hook RTK **local**

**No uses `rtk init -g`**, porque afectaría también la prueba de control sin RTK.

```bash
mkdir -p ~/testes-economia-tokens/rtk/claude-com-rtk
cd ~/testes-economia-tokens/rtk/claude-com-rtk
rtk init
```

El comando `rtk init` por sí solo **no instala el hook automático**. En un proyecto nuevo y vacío, crea `.claude/settings.local.json`:

```bash
mkdir -p .claude
if [ -e .claude/settings.local.json ]; then
  echo "Ya existe configuración; revísala y combina sin sobrescribir."
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
python3 -m json.tool .claude/settings.local.json >/dev/null
rtk rewrite 'git status'
```

Abre Claude y consulta `/hooks` para verificar `PreToolUse / Bash / rtk hook claude`. Ver el hook en el menú **no garantiza** que se haya ejecutado en todos los comandos. Realiza una prueba de funcionamiento antes de tomar los contadores iniciales.

Si deseas limpiar las estadísticas previas del RTK, **haz una copia primero**, porque esas estadísticas son globales:

```bash
mkdir -p ~/testes-economia-tokens/rtk/backups
rtk gain --all --format json > ~/testes-economia-tokens/rtk/backups/rtk-gain-antes-claude.json
rtk gain --reset
rtk gain
```

El reinicio afecta solo a las estadísticas, no desinstala el RTK. Después inicia una nueva sesión de Claude en el mismo proyecto, registra `/usage` inicial, ejecuta la solicitud idéntica, registra `/usage` final y consulta `rtk gain` desde la terminal.

## Instrucciones completas de prueba — Cafeteria Aurora

**Para reproducir una comparación controlada, usa exactamente el mismo texto en las cuatro ejecuciones.**

> Crea desde cero un sitio web institucional de cuatro páginas, sin backend, con Vite + React + TypeScript. Debe incluir cabecera y pie de página, navegación funcional, diseño adaptable, accesibilidad básica, tres tarjetas de ofertas, dos llamadas a la acción y una página de contacto con formulario validado y mensaje de confirmación local, sin envío real. Crea cuatro páginas: Inicio, Sobre nosotros, Servicios/Productos y Contacto. La empresa ficticia es «Cafeteria Aurora», una cafetería artesanal con café de especialidad, dulces caseros y un espacio acogedor en el centro de la ciudad. Mantén una identidad visual coherente y páginas completas, no solo marcadores de posición. Incluye un README con los comandos de instalación, desarrollo y compilación. Ejecuta la compilación y comunica qué comprobaciones pasaron y cuáles fallaron. No añadas backend, base de datos ni envíos reales de datos.

> **Nota:** la traducción anterior es para lectores hispanohablantes. En el video, el texto original de prueba estaba en portugués. Para una réplica estricta del experimento grabado, conserva ese idioma y el texto original sin modificaciones entre las cuatro condiciones.

## Resultados con línea de base inicial descontada

Los pantallazos contienen **contadores finales acumulados**. Las comparaciones siguientes restan el consumo inicial conocido. Como algunos indicadores se muestran en K/M, los valores netos son aproximados.

### Codex CLI / GPT-6.1 Sol Medium

| Métrica | Sin RTK | Con RTK | Variación |
|---|---:|---:|---:|
| `used` inicial | ~4.270 | ~4.310 | — |
| `used` final | 65.734 | 69.336 | — |
| **`used` neto de la tarea** | **~61.464** | **~65.026** | **+5,8 %** |
| Entrada neta sin caché | ~48.582 | ~51.990 | +7,0 % |
| Salida neta | ~12.882 | ~13.036 | +1,2 % |
| Lectura de caché neta estimada | ~856.156 | ~817.796 | −4,5 % |

En Codex, `used` equivale a **entrada sin caché + salida**; la entrada `in` incluye tokens cacheados. Véase la [implementación oficial de Codex](https://github.com/openai/codex/blob/main/codex-rs/tui/src/token_usage.rs). El punto inicial está redondeado.

**`rtk gain`:** un comando, salida estimada de 33 → 10 tokens, **23 ahorrados (69,7 %) localmente**. En cambio, el uso neto de la tarea con RTK fue **~3.562 tokens mayor (+5,8 %)**.

### Claude Code / MiniMax M3.1 Flash

| Métrica | Sin RTK | Con RTK | Variación |
|---|---:|---:|---:|
| Entrada neta | ~66.600 | 73.700 | +10,7 % |
| Salida neta | ~30.118 | 25.500 | −15,3 % |
| **Entrada + salida netas** | **~96.718** | **99.200** | **+2,6 %** |
| Lectura de caché mostrada al final* | ~2,5 millones | ~1,6 millones | ~−36 % |
| Solicitudes | 76 | 62 | −18,4 % |
| Tiempo indicado | 12min10s | 10min49s | −1min21s |

La sesión sin RTK comenzó con aproximadamente **12.900 de entrada y 82 de salida**; la sesión con RTK comenzó con entrada y salida a cero.

*Los contadores de caché corresponden a los valores mostrados al final: **no se dispone de una sustracción comprobada del caché inicial**. Por eso la diferencia de ~36 % es solo indicativa.*

**`rtk gain`:** 17 comandos, de 747 → 406 tokens de salida estimados; **341 ahorrados (45,6 %) localmente**. El sitio creado con RTK resultó más sencillo y hubo una interrupción/reanudación. Esto **no prueba** que el RTK causara ninguna de las dos diferencias.

## Simulación de precios de API, no facturación real

Tarifas utilizadas, USD por cada millón de tokens:

| Modelo | Entrada sin caché | Salida | Lectura de caché |
|---|---:|---:|---:|
| GPT-6.1 Sol | US$ 2,00 | US$ 10,00 | US$ 0,10 |
| MiniMax M3.1 Flash | US$ 0,15 | US$ 0,60 | US$ 0,015 |

Referencias: [OpenAI](https://developers.openai.com/api/docs/models/gpt-6.1-sol), [MiniMax](https://www.minimax.io/blog/minimax-m31f). Verifica los precios oficiales actualizados antes de volver a utilizarlos.

Suponiendo que las tres categorías se facturan por separado:

```text
Costo USD = (entrada_sin_cache * precio_entrada
           + salida * precio_salida
           + cache_leido * precio_cache) / 1.000.000
```

| Estimación | Sin RTK | Con RTK | Diferencia |
|---|---:|---:|---:|
| Codex, línea de base descontada | ~US$ 0,3116 | ~US$ 0,3161 | **+1,5 %** |
| Claude, caché final aproximado | ~US$ 0,0656 | ~US$ 0,0504 | **−23,2 %** |

Se trata de **estimaciones académicas**, no de cargos reales de Codex/Claude Code ni de facturas de MiniMax. En particular, el cálculo del Claude usa el caché **final aproximado**, no una medición neta comprobada. No incluye escrituras de caché, herramientas facturadas aparte, contexto largo ni otras tarifas.

## Problemas y limitaciones

- La sesión con RTK en Claude mostró `No hook installed`, aunque `/hooks` mostraba `PreToolUse / Bash / rtk hook claude` configurado localmente. La [incidencia #2024](https://github.com/rtk-ai/rtk/issues/2024) de RTK recoge un comportamiento parecido cuando se instala un hook solo en el proyecto. Es una **hipótesis**, no una explicación demostrada de este caso.
- En una prueba de preparación anterior se observó `API Error: The response stream was malformed` mediante el proveedor externo. No se debe asumir que ocurrió en todas las pruebas finales.
- El proveedor externo puede mostrar avisos de verificación de seguridad en modo Auto. Revisa los permisos y confirmaciones.
- `rtk init --global --dry-run` es solo una simulación y no instala un hook global.
- No sobrescribas un `.claude/settings.local.json` ya existente; combina los campos manualmente.
- Para quitar RTK, revisa primero la configuración local. En Codex, examina `rtk init --codex --uninstall --dry-run` antes de aplicar cambios. En Claude, elimina solo el hook RTK sin modificar los demás ajustes.

## Conclusión

RTK consiguió comprimir las salidas de los comandos registrados, pero el consumo neto de entrada sin caché + salida **aumentó en las dos comparaciones**. En la simulación de API, el costo del Codex aumentó ligeramente y el del Claude disminuyó **bajo las hipótesis explicadas**, mientras que la interfaz generada por Claude con RTK fue visualmente más simple.

**Una ejecución por condición no permite establecer causalidad.** Para generalizar, habría que repetir los experimentos, registrar caché inicial y final, comprobar las pruebas de compilación y evaluar la calidad visual.

El PDF de la presentación del episodio se publica **solo en portugués, en la raíz de `01-RTK`**.
