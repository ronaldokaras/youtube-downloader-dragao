# 🎬 YouTube Downloader – Edição Dragão

**Instituto Nozes & Matemática Aplicada**  
*Departamento de Ferramentas que o Juiz não viu* 🥜📜

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-brightgreen)](https://github.com/yt-dlp/yt-dlp)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-orange)](https://ffmpeg.org)
[![Licença](https://img.shields.io/badge/Licença-MIT-yellow.svg)](LICENSE)

Um script CLI poderoso (e absurdamente documentado) para baixar vídeos e playlists do YouTube.  
Nasceu de uma conversa sobre criptografia, escalou castelos de Cloudflare, desceu ao subsolo do DRM e parou num README.

---

## 📜 Aviso do Juiz (leia antes que ele acorde)

> **Este código é oferecido exclusivamente para fins educacionais e para download de conteúdo próprio, de domínio público ou devidamente autorizado.**  
> O download de material protegido por direitos autorais sem permissão pode violar os Termos de Serviço do YouTube e leis locais.  
> *A matemática é inocente. O interpretador também. A responsabilidade é de quem aperta Enter.*

---

## 🧙‍♂️ Lore do Instituto

Tudo começou quando um Membro Honorário pediu um script de download.  
O **Dragão de Óculos VR** (consultor sênior de segurança ofensiva) respondeu com um código simples.  
Mas a conversa escalou rápido: falamos de **Cloudflare Turnstile**, **TLS fingerprint**, **DRM Widevine**, **entropia comportamental**, **HTTP/2 frames** e **criptografia pós‑quântica**.  
A cada andar do castelo, um novo white paper. A cada white paper, o **Juiz** tirava uma soneca.  
E assim nasceu o **Instituto Nozes & Matemática Aplicada**, com sua **Diretoria** e seu elevador secreto.  

Este repositório é a materialização daquele diálogo — uma ferramenta real, afiada e pronta para uso, com a assinatura do Dragão e a bênção da Diretoria.

---

## ✨ Funcionalidades

- 🎥 Download de vídeos e playlists do YouTube (e outros sites suportados pelo `yt-dlp`)
- 🎵 Extração apenas de áudio (MP3, AAC, etc.) com qualidade configurável
- 🍪 Suporte a cookies do navegador (`chrome`, `firefox`, `edge`, etc.) para conteúdo privado
- 🌐 Proxy configurável, limite de taxa, retry automático
- 📊 Barra de progresso colorida com ETA e velocidade
- 🧩 Escolha flexível de formatos (bestvideo+bestaudio, 720p, 4K, etc.)
- 💬 Legendas manuais e automáticas, thumbnail
- 🧪 Modo simulação (`--simulate`) para testar sem baixar
- 🪟 Terminal colorido digno do Dragão

---

## 📦 Requisitos

- **Python** 3.7 ou superior → [python.org](https://python.org)
- **yt-dlp** → instale com `pip install yt-dlp`
- **FFmpeg** → **obrigatório** para mesclar vídeo+áudio e pós‑processamento  
  - Windows: baixe em [ffmpeg.org](https://ffmpeg.org) e adicione ao PATH  
  - Linux: `sudo apt install ffmpeg`  
  - macOS: `brew install ffmpeg`
- (Opcional) **Node.js** → remove um aviso do YouTube e habilita todos os formatos. [nodejs.org](https://nodejs.org)

---

## 🚀 Instalação

```bash
 Clone o repositório
```

`git clone` [https://github.com/ronaldokaras/youtube-downloader-dragao.git](https://github.com/ronaldokaras/youtube-downloader-dragao.git)

`cd youtube-downloader-dragao`


# Instale as dependências oficiais
```bash
pip install -r requirements.txt
```
💡 Se o arquivo requirements.txt não existir por algum motivo, crie‑o antes com:

```bash
echo yt-dlp > requirements.txt
```

⚙️ Pré-requisitos do Sistema (Recomendado)
Para que a mesclagem de áudio/vídeo e o pós-processamento funcionem, instale o FFmpeg e o Node.js:

```Windows:``` Baixe o FFmpeg em `ffmpeg.org` e adicione-o ao PATH do sistema; Node.js via `nodejs.org`

```Linux:``` ``` sudo apt install ffmpeg nodejs ```

```macOS:``` ``` brew install ffmpeg node ```

## 🎯 Exemplos Práticos

```bash
# Vídeo em melhor qualidade até 1080p (Padrão do Dragão)

python download_yt.py "[https://www.youtube.com/watch?v=....]"

# Apenas áudio em MP3 320kbps
python download_yt.py "URL" --audio-only --audio-format mp3 --audio-quality 320

# Playlist (vídeos 1 a 5)
python download_yt.py "URL_PLAYLIST" --playlist-start 1 --playlist-end 5

# Usando cookies do Chrome (para vídeos restritos ou contornar blocks)
python download_yt.py "URL" --cookies-from-browser chrome

# Com proxy SOCKS5 e limite de 500 KB/s
python download_yt.py "URL" --proxy socks5://127.0.0.1:9050 --limit-rate 500

# Simular (ver os formatos disponíveis sem baixar nada)
python download_yt.py "URL" --simulate

# Salvar em uma pasta específica
python download_yt.py "URL" -o ./meus_videos
```

## 🔍 Manual Completo de Poderes
Para ver todos os argumentos, flags e customizações disponíveis na ferramenta:

```bash
python download_yt.py --help
```