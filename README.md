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
```

(Opcional) Se você tiver uma GPU NVIDIA, instale o PyTorch com suporte a CUDA para o Whisper rodar muito mais rápido.⚙️ Configuração (Obrigatório)Antes de executar, você precisa editar o início do código Python (main.py):1. API Key do Google (Gemini)Obtenha sua chave gratuita no Google AI Studio.Cole a chave na variável API_KEY:PythonAPI_KEY = "SUA_CHAVE_AQUI"
2. Caminho do ImageMagickO MoviePy precisa saber onde o executável do ImageMagick está. Localize o arquivo magick.exe no seu computador e atualize a linha de configuração:Python# Exemplo (verifique o caminho real no seu PC):
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})
🚀 Como UsarExecute o script no terminal:Bashpython seu_script.py
O programa pedirá a URL do YouTube. Cole o link e aperte Enter.Aguarde o processo automático:⬇️ Baixando: O vídeo é salvo temporariamente.🧠 Lendo: O Whisper transcreve o áudio.🤖 Analisando: O Gemini escolhe os melhores cortes.✂️ Editando: O MoviePy gera os arquivos finais.Os vídeos prontos aparecerão na pasta clips_virais/ criada automaticamente.📂 Estrutura de SaídaPlaintext/pasta_do_projeto
  ├── video_temp.mp4          (Vídeo original baixado)
  ├── clips_virais/
  │   ├── clip_1_Titulo_Viral.mp4
  │   ├── clip_2_Outro_Momento.mp4
  │   └── clip_3_Conclusao.mp4
  └── seu_script.py
⚠️ Solução de Problemas ComunsErroSoluçãoImageMagick not foundVerifique se o caminho no change_settings está correto e aponta para magick.exe.AttributeError: 'NoneType' objectA IA do Google pode ter falhado ao retornar o JSON. Tente rodar novamente ou verifique se sua API Key é válida.MoviePy TextClip ErrorGeralmente é problema com o ImageMagick. Tente reinstalá-lo ou verificar as permissões de pasta.📝 LicençaEste projeto foi desenvolvido para fins educacionais e de automação de conteúdo.Disclaimer: O uso de vídeos de terceiros deve respeitar as leis de direitos autorais da sua região e as políticas da plataforma (YouTube).
