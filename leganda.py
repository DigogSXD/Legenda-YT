import whisper
import yt_dlp
import os
import json
import re 
import google.generativeai as genai 
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.config import change_settings

# --- CONFIGURAÇÕES ---
API_KEY = "" 

# Configuração do ImageMagick 
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

genai.configure(api_key=API_KEY)

def baixar_video_youtube(url, output_name="video_temp"):
    print(f"⬇️ Baixando vídeo...")
    if os.path.exists(output_name + ".mp4"): os.remove(output_name + ".mp4")
    ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'outtmpl': output_name + '.%(ext)s', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
    return output_name + ".mp4"

def transcrever_audio(video_path):
    print("🧠 Whisper lendo (palavra por palavra)...")
    model = whisper.load_model("base") 
    # MUDANÇA CRUCIAL: word_timestamps=True obriga a IA a dizer o tempo de cada palavra
    result = model.transcribe(video_path, language="pt", fp16=False, word_timestamps=True)
    return result

def limpar_json(texto):
    padrao = r"```json\s*(.*?)\s*```"
    match = re.search(padrao, texto, re.DOTALL)
    if match: return match.group(1)
    padrao_simples = r"```\s*(.*?)\s*```"
    match_simples = re.search(padrao_simples, texto, re.DOTALL)
    if match_simples: return match_simples.group(1)
    return texto

def limpar_nome_arquivo(titulo):
    titulo = re.sub(r'[<>:"/\\|?*]', '', titulo)
    titulo = titulo.replace("'", "").replace('"', "")
    titulo = titulo.strip().replace(' ', '_')
    return titulo[:50]

def analisar_viralidade(whisper_result):
    print("🤖 IA (Gemini 2.0) analisando conteúdo...")
    
    # Prepara o texto para a IA (usando segmentos para contexto)
    transcript_text = ""
    for seg in whisper_result['segments']:
        tempo = int(seg['start'])
        transcript_text += f"[{tempo}s] {seg['text']}\n"

    texto_para_analise = transcript_text[:50000] 

    prompt = f"""
    Você é um editor de vídeos profissional para TikTok.
    Analise a transcrição e identifique 3 momentos com alto potencial viral.
    
    Regras OBRIGATÓRIAS:
    1. Retorne APENAS um JSON válido.
    2. Formato:
    [
        {{"start_time": 10, "end_time": 60, "titulo": "Titulo Curto"}},
        {{"start_time": 150, "end_time": 180, "titulo": "Titulo 2"}}
    ]
    3. Clipes entre 30 e 60 segundos.

    Transcrição:
    {texto_para_analise}
    """

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        texto_limpo = limpar_json(response.text)
        cortes_sugeridos = json.loads(texto_limpo)
        return cortes_sugeridos

    except Exception as e:
        print(f"❌ Erro na IA: {e}")
        return []

def criar_clips_virais(video_path, whisper_result, cortes_ia, output_folder="clips_virais"):
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    
    video = VideoFileClip(video_path)
    print(f"✂️ Criando {len(cortes_ia)} clips no estilo Word-by-Word...")

    # Extrair TODAS as palavras com timestamps
    todas_palavras = []
    for seg in whisper_result['segments']:
        if 'words' in seg:
            todas_palavras.extend(seg['words'])
        else:
            # Fallback se word_timestamps falhar: usa o segmento inteiro
            todas_palavras.append({'word': seg['text'], 'start': seg['start'], 'end': seg['end']})

    for i, corte in enumerate(cortes_ia):
        start = corte['start_time']
        end = corte['end_time']
        titulo_seguro = limpar_nome_arquivo(corte['titulo'])
        
        if start >= end: continue
        
        print(f"🔥 Processando Clip {i+1}: {titulo_seguro}")
        nome_arquivo = f"{output_folder}/clip_{i+1}_{titulo_seguro}.mp4"

        try:
            # 1. Corte Base
            clip = video.subclip(start, end)
            w, h = clip.size
            novo_w = h * 9 // 16
            clip = clip.crop(x1=w/2 - novo_w/2, y1=0, width=novo_w, height=h)

            # 2. Gerar Clips de Texto (UM POR PALAVRA)
            text_clips = []
            
            for palavra in todas_palavras:
                p_start = palavra['start']
                p_end = palavra['end']
                texto = palavra['word'].strip()

                # Verifica se a palavra está dentro deste corte viral
                if p_start >= start and p_end <= end:
                    # Ajusta tempo relativo ao clip
                    rel_start = p_start - start
                    rel_end = p_end - start
                    duracao = rel_end - rel_start

                    # Cria o clip da palavra
                    txt_clip = (TextClip(texto, 
                                       font='Impact', 
                                       fontsize=100, # BEM GRANDE
                                       color='#FFD700', # Amarelo
                                       stroke_color='black', 
                                       stroke_width=5,
                                       method='caption',
                                       size=(clip.w * 0.9, None))
                                .set_position('center')
                                .set_start(rel_start)
                                .set_duration(duracao))
                    
                    # Efeito de "Pop" (Pequeno Zoom)
                    # O texto cresce 10% durante a exibição
                    # txt_clip = txt_clip.resize(lambda t: 1 + 0.1 * t) 

                    text_clips.append(txt_clip)

            # 3. Compor tudo
            # Adiciona o vídeo base + todas as palavras pulando na tela
            final_clip = CompositeVideoClip([clip] + text_clips)

            final_clip.write_videofile(nome_arquivo, codec='libx264', audio_codec='aac', fps=24, logger=None)
            print(f"✅ Salvo: {nome_arquivo}")
        
        except Exception as e:
            print(f"❌ Erro ao salvar clip {i+1}: {e}")

    video.close()

if __name__ == "__main__":
    if "SUA_KEY" in API_KEY:
        print("❌ ERRO: Coloque sua API Key do Google!")
    else:
        url = input("URL do YouTube: ")
        path_video = baixar_video_youtube(url)
        # O resultado do whisper agora contém 'words' dentro dos segmentos
        whisper_result = transcrever_audio(path_video)
        cortes = analisar_viralidade(whisper_result)
        
        if cortes:
            criar_clips_virais(path_video, whisper_result, cortes)
            print("🚀 Clips Word-by-Word gerados!")
        else:
            print("❌ Falha na análise da IA.")
