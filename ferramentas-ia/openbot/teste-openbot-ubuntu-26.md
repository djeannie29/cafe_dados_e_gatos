# OpenBot no Ubuntu 26.04 — instalação e testes de laboratório

**Café com Dados & Gatos — roteiro copy-paste de teste (não é resultado de teste concluído)**  
**Preparado em:** 23/11/2026  
**Projeto testado:** [nightly-labs/openbot](https://github.com/nightly-labs/openbot)  
**Versão fixada para o laboratório:** [v0.76.1](https://github.com/nightly-labs/openbot/releases/tag/v0.76.1), publicada em 21/11/2026.  
**Sistema-alvo:** Ubuntu 26.04 Desktop, Linux x86_64.  
**Objetivo:** instalar e abrir o OpenBot nativo no Linux, verificar interface, configuração e, numa etapa separada, testar um agente em uma pasta de laboratório sem tocar em projetos reais.

> **Estado inicial:** comandos conferidos na documentação/release oficiais; **ainda não executados no computador da Denise**. Anotar o resultado de cada etapa em [registro-do-teste.md](registro-do-teste.md). Não publicar chaves de API, tokens, histórico privado nem dados pessoais nas capturas do vídeo.

## Conferir o ambiente

No **terminal do Ubuntu**, não no PowerShell:

\`\`\`bash
cat /etc/os-release | grep PRETTY_NAME
uname -m
echo "$XDG_SESSION_TYPE"
\`\`\`

Esperado: Ubuntu 26.04; arquitetura \`x86_64\` para o arquivo usado neste guia. A sessão pode ser \`x11\` ou \`wayland\`; algumas funções de desktop remoto exigem X11.

## Preparar dependências

\`\`\`bash
sudo apt update
sudo apt install -y curl fuse3
\`\`\`

O AppImage do OpenBot usa \`fusermount3\` (pacote \`fuse3\`). **Não precisa de \`libfuse2\`**, segundo o README oficial. Versão pré-compilada não requer instalar Bun, Node.js, npm ou Docker.

## Baixar a versão de teste

\`\`\`bash
mkdir -p "$HOME/Applications"
cd "$HOME/Applications"
curl -fL --retry 3 \
  -o OpenBot-0.76.1-x86_64.AppImage \
  https://github.com/nightly-labs/openbot/releases/download/v0.76.1/OpenBot-0.76.1-x86_64.AppImage
\`\`\`

**Verificação de integridade do download** (antes de executar):

\`\`\`bash
curl -fL --retry 3 \
  -o SHA256SUMS-linux.txt \
  https://github.com/nightly-labs/openbot/releases/download/v0.76.1/SHA256SUMS-linux.txt
grep 'OpenBot-0.76.1-x86_64.AppImage' SHA256SUMS-linux.txt | sha256sum -c -
\`\`\`

Esperado: \`OpenBot-0.76.1-x86_64.AppImage: OK\`. Se \`grep\` não encontrar o nome ou a verificação falhar, **pare** e confira a release: não execute arquivo sem integridade confirmada. O \`sha256sum\` confirma correspondência com o arquivo de checksums daquela release; não substitui uma política de verificação de procedência.

\`\`\`bash
chmod +x OpenBot-0.76.1-x86_64.AppImage
\`\`\`

## Configurar o AppArmor (Ubuntu 26.04)

O projeto informa que Ubuntu 23.10+ pode restringir os *user namespaces* de que o sandbox do Electron necessita. O perfil a seguir é fornecido **pelo próprio OpenBot**, fixado na versão testada.

\`\`\`bash
curl -fL --retry 3 \
  -o /tmp/openbot.apparmor \
  https://raw.githubusercontent.com/nightly-labs/openbot/v0.76.1/build/linux/openbot.apparmor
cat /tmp/openbot.apparmor
\`\`\`

O perfil oficial contém um caminho de anexação que abrange \`~/Applications/OpenBot*.AppImage\`; por isso mantemos o arquivo nessa pasta.

\`\`\`bash
sudo install -m 0644 /tmp/openbot.apparmor /etc/apparmor.d/openbot
sudo systemctl reload apparmor
\`\`\`

**Não usar \`--no-sandbox\`** como correção de erro. A própria documentação desencoraja desativar essa proteção.

## Abrir o aplicativo

\`\`\`bash
cd "$HOME/Applications"
./OpenBot-0.76.1-x86_64.AppImage
\`\`\`

### Checagens na tela (registrar, não presumir sucesso)

- [ ] Janela gráfica abriu.
- [ ] Versão exibida conferida.
- [ ] Tela de configuração/provedores abre.
- [ ] A interface reconhece agentes já instalados, se houver.
- [ ] Nenhum token ou segredo aparece na gravação.
- [ ] Aplicativo fecha normalmente.

**Primeiro teste:** não conceder acesso aos repositórios e pastas reais. O OpenBot executa agentes que podem acessar arquivos, comandos e rede com permissões locais. Identificar as opções de permissão antes de habilitar um agente.

## Teste funcional — somente depois de configurar um provedor

Esta etapa não foi validada ainda e depende de um agente/provedor autenticado.

\`\`\`bash
mkdir -p "$HOME/Documentos/lab-openbot"
printf 'Laboratorio OpenBot - nao modificar outros diretorios.\n' > "$HOME/Documentos/lab-openbot/LEIA-ME.txt"
\`\`\`

No OpenBot, **se for possível delimitar a pasta de trabalho**, escolher \`~/Documentos/lab-openbot\`. Não presumir que a escolha da pasta seja uma barreira de segurança; permissões do agente e da ferramenta precisam ser verificadas.

Prompt inicial (apenas leitura):

> Leia o arquivo LEIA-ME.txt da pasta de laboratório e explique seu conteúdo. Não execute comandos, não edite arquivos e não acesse outras pastas.

Quando a leitura funcionar e **somente se as permissões forem compreendidas**, testar escrita:

> Crie apenas o arquivo resultado-openbot.txt na pasta de laboratório com a frase "Teste de escrita OpenBot concluído". Não altere nenhum outro arquivo.

Conferir no terminal:

\`\`\`bash
ls -la "$HOME/Documentos/lab-openbot"
cat "$HOME/Documentos/lab-openbot/resultado-openbot.txt"
\`\`\`

Se \`~/Documentos\` não existir, usar uma pasta de laboratório escolhida manualmente; registrar o caminho efetivamente utilizado.

## Problemas conhecidos / diagnóstico

**AppImage reclama de \`fusermount\`:**

\`\`\`bash
command -v fusermount3
sudo apt install -y fuse3
\`\`\`

**Fecha imediatamente com erro de \`user namespaces\` ou \`SUID sandbox\`:** conferir se \`/etc/apparmor.d/openbot\` foi instalado e se o AppImage está no caminho esperado pelo perfil. Não recorrer ao \`--no-sandbox\`.

**Falha de GPU na abertura:** o guia oficial descreve o teste de inicialização com renderização por CPU:

\`\`\`bash
cd "$HOME/Applications"
OPENBOT_DISABLE_GPU=1 ./OpenBot-0.76.1-x86_64.AppImage
\`\`\`

Esse comando é **alternativo**, apenas se houver falha de GPU; não executar simultaneamente com a instância normal.

**Desktop remoto indisponível:** recursos de desktop remoto no Linux x64 requerem sessão X11; Wayland tem limitações específicas. Não confundir com falha na instalação da interface gráfica.

**Agente exige CLI:** testar a instalação e o login da CLI correspondente separadamente. Exemplo para um Codex já instalado:

\`\`\`bash
codex --version
\`\`\`

Não publicar credenciais; não instalar agentes automaticamente sem necessidade.

## Encerrar o laboratório / remoção opcional

Fechar o OpenBot pela interface. Se quiser remover somente o arquivo AppImage baixado:

\`\`\`bash
rm -i "$HOME/Applications/OpenBot-0.76.1-x86_64.AppImage"
\`\`\`

**Atenção:** este comando remove o instalador/app executável e pede confirmação. Não apaga automaticamente as configurações do usuário em \`~/.config/OpenBot\`.

O AppImage pode criar atalhos em \`~/.local/share/applications/openbot.desktop\` e \`~/.local/share/icons/openbot.png\`. A remoção de perfis ou configurações deve ser uma decisão separada, depois da avaliação do teste.

## Fontes primárias consultadas

- [README oficial — Linux, AppImage e AppArmor](https://github.com/nightly-labs/openbot#linux)
- [Release v0.76.1 — assets Linux e SHA256](https://github.com/nightly-labs/openbot/releases/tag/v0.76.1)
- [Perfil AppArmor oficial nesta versão](https://github.com/nightly-labs/openbot/blob/v0.76.1/build/linux/openbot.apparmor)
- [Troubleshooting oficial](https://github.com/nightly-labs/openbot/blob/main/docs/TROUBLESHOOTING.md)

**Regra editorial do vídeo:** mostrar o que realmente aconteceu no computador; erros, adaptações, limitações e acertos devem ser registrados em [registro-do-teste.md](registro-do-teste.md). Não descrever etapas ainda não realizadas como se estivessem funcionando.
