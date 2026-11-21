# Como transformar uma TV Box em um Gateway de IA — Parte 1

**Café com Dados & Gatos | Documentação e comandos do vídeo 01**

Neste guia, utilizamos uma **BTV BX**, com processador **Amlogic S905X**, placa **p212**, **2 GB de RAM** e **16 GB de armazenamento**, para executar **Armbian Linux**, **XFCE Minimal**, **XRDP** e **FreeLM**. A BTV hospeda o gateway; as respostas de inteligência artificial são processadas por provedores externos, não por um modelo grande dentro da TV Box.

> **Atenção à compatibilidade:** TV Boxes de aparência semelhante podem ter placas, chips de Wi-Fi e controladores diferentes. Confirme o hardware e teste o Linux por mídia externa antes de considerar uma instalação no armazenamento interno. Instalar na eMMC pode substituir o sistema original e exigir procedimentos específicos para recuperação.

## Downloads utilizados

**Gravador de imagem USB — balenaEtcher:**  
https://etcher.balena.io/

**Imagem do Armbian utilizada na BTV BX:**  
`Armbian_26.11.0_amlogic_s905x_bookworm_6.12.117_server_2026.11.14.img.gz`

**Download direto da imagem:**  
https://github.com/ophub/amlogic-s9xxx-armbian/releases/download/Armbian_bookworm_arm64_server_2026.11/Armbian_26.11.0_amlogic_s905x_bookworm_6.12.117_server_2026.11.14.img.gz

**Página da versão (releases):**  
https://github.com/ophub/amlogic-s9xxx-armbian/releases/tag/Armbian_bookworm_arm64_server_2026.11

**SHA-256 publicado para o arquivo acima:**  
`35af9e3e5e13c18a60c268e45e6c4d270f79a12805b4e026c2a1a829e2a7aade`

**DTB utilizado pela placa p212:** `meson-gxl-s905x-p212.dtb`.

## Preparar o pendrive — Windows

No balenaEtcher, escolha **Flash from file**, selecione o `.img.gz` indicado, escolha o pendrive e clique em **Flash**. O programa grava a imagem diretamente do arquivo compactado.

**Atenção:** o pendrive será apagado. Depois da gravação, não aceite a solicitação do Windows para formatar as partições Linux.

Para esta placa, confira na partição de inicialização o arquivo `uEnv.txt` e a referência ao DTB da p212:

```text
FDT=/dtb/amlogic/meson-gxl-s905x-p212.dtb
```

A localização e o formato exatos dependem da imagem utilizada. Não misture arquivos de boot de projetos diferentes nem copie um `u-boot` arbitrário de outra TV Box.

## Conferir Linux e armazenamento — terminal da BTV

```bash
cat /etc/os-release
uname -m
uname -r
free -h
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS
df -h
ip -br address
```

O comando `lsblk` permite verificar se a raiz `/` está montada na mídia externa (`sda`, por exemplo) ou no armazenamento interno (`mmcblk`, dependendo da placa).

## Testar a rede — terminal da BTV

```bash
ping -c 3 1.1.1.1
getent hosts github.com
```

## Instalar o XFCE Minimal — terminal da BTV

```bash
sudo apt update
sudo apt install -y --no-install-recommends xorg xfce4 xfce4-terminal lightdm lightdm-gtk-greeter dbus-x11
sudo systemctl enable lightdm
sudo reboot
```

Após reiniciar, confirme a interface gráfica, o teclado, o mouse e o terminal.

## Descobrir o IP da BTV e conferir o SSH — terminal da BTV

```bash
hostname -I
systemctl is-active ssh
```

Se o servidor SSH não estiver instalado ou ativo:

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

## Acessar o terminal da BTV — PowerShell do Windows

Substitua `teste` pelo usuário Linux da sua TV Box e `192.168.10.106` pelo IP mostrado em `hostname -I`.

```powershell
ssh teste@192.168.10.106
```

Os comandos Linux a seguir são executados **na BTV**, inclusive quando digitados pela conexão SSH. Não rode `apt` no PowerShell sem uma sessão SSH.

## Instalar o XRDP — terminal da BTV

Execute como usuário Linux comum com permissão `sudo` (por exemplo, `teste`):

```bash
sudo apt update
sudo apt install -y xrdp xorgxrdp dbus-x11
printf 'startxfce4\n' > "$HOME/.xsession"
sudo systemctl enable --now xrdp
systemctl is-active xrdp
hostname -I
ss -lnt | grep ':3389'
```

## Conectar pelo Windows — Área de Trabalho Remota

Pressione **Win + R**, digite `mstsc`, informe o IP da BTV e entre com o usuário e a senha do **Linux**, selecionando a sessão **Xorg**, caso a opção seja exibida.

O PC e a BTV devem estar na mesma rede. **Não exponha a porta 3389 ao acesso externo pela internet.** O XRDP pode abrir uma sessão gráfica separada da que aparece no HDMI.

## Ferramentas básicas — terminal da BTV

```bash
sudo apt update
sudo apt install -y python3 python3-pip curl ca-certificates git
python3 --version
```

Em uma TV Box adaptada, não execute atualizações de kernel ou bootloader sem verificar a compatibilidade com a placa.

## Instalar Node.js 22 pelo nvm — terminal da BTV

O FreeLM 0.5.2 exige Node.js 20 ou superior. Neste projeto, usamos o **Node.js 22** por meio do nvm, sem instalar pacotes npm globais como `root`.

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

## Instalar e iniciar o FreeLM — terminal da BTV

```bash
npm install -g freelm
freelm --help
freelm doctor
freelm serve
```

Mantenha esse terminal aberto. O servidor utiliza o endereço **`http://127.0.0.1:4000/v1` na própria BTV**.

## Testar o servidor — outro terminal da BTV

```bash
curl -fsS http://127.0.0.1:4000/health
curl -fsS http://127.0.0.1:4000/v1/models
```

## Abrir o túnel SSH — PowerShell no PC Windows

Com `freelm serve` executando na BTV, abra **outra janela** de PowerShell no computador e execute:

```powershell
ssh -N -L 4400:127.0.0.1:4000 teste@192.168.10.106
```

Substitua o usuário e o IP pelos da sua TV Box. Mantenha a janela do túnel aberta: ela encaminha a porta **4400 do PC** para a porta **4000 da BTV** sem expor o servidor à internet.

## Testar o túnel — segundo PowerShell no PC

```powershell
curl.exe -fsS http://127.0.0.1:4400/health
```

## Configurar o cliente de IA no VS Code — PC Windows

No cliente ou extensão que aceite APIs compatíveis com OpenAI, utilize os seguintes dados, conforme os campos disponíveis:

| Configuração | Valor |
| --- | --- |
| Tipo de API | OpenAI Compatible |
| Base URL | `http://127.0.0.1:4400/v1` |
| API Key (valor local de teste) | `freelm` |
| Modelo | `auto` |

Faça uma pergunta curta para verificar a comunicação entre o VS Code, o túnel SSH e o FreeLM. A disponibilidade de modelos gratuitos depende dos provedores e de suas cotas.

## Encerrar o teste

Pressione **Ctrl+C** no PowerShell do túnel e no terminal da BTV em que `freelm serve` estiver rodando.

## Erros encontrados e ajustes necessários

**Node.js 18 incompatível com o FreeLM:** a versão presente inicialmente nos pacotes Debian era inferior ao requisito da ferramenta. Utilizamos Node.js 22 pelo nvm.

**Erro `EACCES` com `npm install -g`:** a instalação global no diretório do sistema não tinha permissão para o usuário comum. Com nvm, o Node.js e os pacotes npm globais ficam sob o diretório do próprio usuário, sem necessidade de `sudo`.

## Referências técnicas

- [Armbian comunitário para Amlogic — ophub](https://github.com/ophub/amlogic-s9xxx-armbian)
- [Hardware BTV BX e informações da placa p212 — EducaBox](https://github.com/educabox/educabox/blob/main/boxes/btvbx.md)
- [XFCE e ambientes gráficos — Armbian](https://docs.armbian.com/config/desktops/)
- [XRDP](https://github.com/neutrinolabs/xrdp)
- [nvm](https://github.com/nvm-sh/nvm)
- [FreeLM](https://github.com/shihabshahrier/freelm)

---

**Café com Dados & Gatos — Parte 1.**