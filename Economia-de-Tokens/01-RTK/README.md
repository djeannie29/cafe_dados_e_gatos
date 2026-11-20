# RTK — Série Economia de Tokens | Café com Dados & Gatos

Materiais do **primeiro episódio** da série, com testes reais do [RTK (Rust Token Killer)](https://github.com/rtk-ai/rtk) no **Codex CLI** e no **Claude Code** em Ubuntu/WSL2.

**Vídeo:** [RTK economiza tokens de verdade? Testamos com Codex e Claude Code](https://youtu.be/AGIbPHTOKHk)

## Documentação nos três idiomas

| Idioma | Guia |
|---|---|
| 🇧🇷 Português | [Guia prático — instalação, comandos, testes e resultados](portugues/GUIA-PRATICO.md) |
| 🇺🇸 English | [Practical guide — setup, commands, tests and results](english/PRACTICAL-GUIDE.md) |
| 🇪🇸 Español | [Guía práctica — instalación, comandos, pruebas y resultados](espa%C3%B1ol/GUIA-PRACTICA.md) |

### Apresentação / Presentation / Presentación

O PDF de apoio da apresentação, com as capturas e os resultados, é disponibilizado **somente em português** e fica **na raiz desta pasta**, separado das traduções.

**Arquivo reservado:** `RTK_Cafe_com_Dados_e_Gatos_VALORES_LIQUIDOS_CODEX_CLAUDE.pdf`

> O PDF é único: não será traduzido nem duplicado nas pastas de idiomas.

## Resumo dos resultados / Summary / Resumen

| Agente | RTK: economia localizada | Variação de tokens líquidos com RTK | Variação do custo simulado de API |
|---|---:|---:|---:|
| Codex CLI · GPT-6.1 Sol Medium | 69,7% em um comando | **+5,8%** | **+1,5%** |
| Claude Code · MiniMax M3.1 Flash | 45,6% em 17 comandos | **+2,6%** | **−23,2%** |

Os valores consideram o desconto da linha de base inicial conhecida. Contadores arredondados geram estimativas aproximadas; no Claude, não foi possível calcular a linha de base de leitura de cache com o mesmo rigor. **Uma execução por condição não comprova causalidade nem economia financeira real.**

**Café com Dados & Gatos:** https://cafecomdadosegatos.com.br/

---
*Material educativo para reprodução de testes técnicos. Verifique sempre as instruções, versões e preços oficiais atualizados.*
