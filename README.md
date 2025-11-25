# 🎬 AI Viral Clip Generator (YouTube to TikTok/Shorts)

Este projeto é uma ferramenta de automação que utiliza Inteligência Artificial para baixar vídeos do YouTube, identificar momentos virais e criar clipes verticais (9:16) com legendas dinâmicas estilo "Word-by-Word" (Alex Hormozi style), prontos para TikTok, Instagram Reels e YouTube Shorts.

## ✨ Funcionalidades

-   **Download Automático:** Baixa vídeos do YouTube na melhor qualidade disponível.
-   **Transcriçao Precisa (Whisper):** Usa o modelo `Whisper` da OpenAI para transcrever o áudio com *timestamps* palavra por palavra.
-   **Curadoria com IA (Gemini 2.0):** Envia a transcrição para o Google Gemini (Flash), que analisa o conteúdo e seleciona os 3 momentos com maior potencial viral.
-   **Edição Automática (MoviePy):**
    -   Corta os segmentos selecionados.
    -   Recorta o vídeo para formato vertical (9:16).
    -   Adiciona legendas amarelas, grandes e centralizadas, sincronizadas palavra por palavra.
    -   Exporta em MP4 otimizado.

## 🛠️ Pré-requisitos

Antes de rodar o script, você precisa ter instalado no seu computador:

1.  **Python 3.8+**
2.  **FFmpeg:** Essencial para manipulação de vídeo e áudio.
3.  **ImageMagick:** Obrigatório para o MoviePy gerar textos.
    -   *Windows:* [Baixe aqui](https://imagemagick.org/script/download.php#windows). Durante a instalação, marque a opção **"Install legacy utilities (e.g. convert)"**.

## 📦 Instalação

1.  Clone este repositório ou baixe o código.
2.  Instale as bibliotecas Python necessárias:

```bash
pip install openai-whisper yt-dlp google-generativeai moviepy imageio-ffmpeg numpy
