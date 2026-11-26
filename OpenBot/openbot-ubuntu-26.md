# OpenBot — Ubuntu 26.04 (AMD64 / x86_64)

[Português](./openbot-ubuntu-26.md) · [Español](./openbot-ubuntu-26-es.md) · [English](./openbot-ubuntu-26-en.md)

**Site oficial:** https://openbot.run/

## 1. Preparar o Ubuntu

Abra o Terminal e atualize a lista de pacotes:

```bash
sudo apt update
```

Esse comando não instala nem atualiza aplicativos.

## 2. Baixar o OpenBot pelo site

1. Abra https://openbot.run/ no Firefox.
2. Clique em **Download for Linux**.
3. Confira que a versão para Linux é **x86_64 / AMD64**, em formato **AppImage**.
4. Baixe o arquivo para **Downloads**.

O site reconhecer o Linux não confirma se todas as dependências estão instaladas.

## 3. Abrir o aplicativo

### Sem terminal: Gear Lever (testado no vídeo)

No Ubuntu 26.04, o AppImage do OpenBot foi aberto com o [Gear Lever](https://flathub.org/en/apps/it.mijorus.gearlever), um aplicativo gráfico para abrir AppImages e adicioná-los ao menu de aplicativos.

- No **Bazaar**, procure por **Gear Lever** e instale-o.
- Abra o Gear Lever e arraste o AppImage do OpenBot da pasta **Downloads** para a janela do Gear Lever.
- Clique em **Move to the app menu** para adicionar o OpenBot ao menu de aplicativos. Depois, clique em **Launch** para abri-lo. Para apenas testar, sem adicionar ao menu, clique direto em **Launch**.

### Alternativa: abrir diretamente pelo gerenciador de arquivos

1. Abra o gerenciador **Arquivos**.
2. Crie a pasta **Applications** na sua pasta pessoal, se necessário.
3. Mova o AppImage da pasta Downloads para **Applications**.
4. Em **Propriedades → Permissões**, habilite a execução do arquivo, se essa opção aparecer.

Se a opção de execução não aparecer, use:

```bash
chmod +x "$HOME"/Applications/OpenBot-*-x86_64.AppImage
```

Tente abrir o AppImage com dois cliques. **Não instale dependências antecipadamente; primeiro verifique se abre.**

## 4. Somente se não abrir

**Erro de FUSE / fusermount3:** confira se o comando existe:

```bash
command -v fusermount3
```

Se não aparecer um caminho, instale a dependência e tente novamente:

```bash
sudo apt install fuse3
```

**Erro relacionado a sandbox / user namespaces:** no Ubuntu 26.04, o OpenBot pode exigir um perfil AppArmor. É um ajuste indicado na documentação oficial. Se aparecer esse erro, execute:

```bash
curl -fL -o /tmp/openbot.apparmor https://raw.githubusercontent.com/nightly-labs/openbot/main/build/linux/openbot.apparmor
```

Confira o arquivo baixado:

```bash
cat /tmp/openbot.apparmor
```

Instale o perfil oficial e recarregue o AppArmor:

```bash
sudo install -m 0644 /tmp/openbot.apparmor /etc/apparmor.d/openbot
sudo systemctl reload apparmor
```

Se `curl` não estiver instalado, será necessário instalá-lo antes de baixar o perfil (`sudo apt install curl`). Não contorne o problema usando `--no-sandbox`.

O AppImage deve permanecer na pasta `~/Applications` para corresponder ao perfil indicado.
