"""
Módulo para interagir com a API da ElevenLabs para geração de áudio.
"""
import requests
import streamlit as st
import os

ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

DEFAULT_VOICE_SETTINGS = {
    "stability": 0.8,
    "similarity_boost": 0.8,
    "style": 0.5,
    "use_speaker_boost": True # Default, mas pode ser ajustado se necessário
}

# O parâmetro 'speed' não é diretamente suportado pela API v1 TTS da ElevenLabs da mesma forma que outros.
# A velocidade da fala é geralmente uma característica da voz escolhida ou ajustada nas configurações da voz no site da ElevenLabs.
# Se for um requisito crítico, pode ser necessário explorar a API de "Voice Design" ou verificar atualizações na documentação da API.
# Por ora, o parâmetro "speed": 1.0 foi removido das configurações fixas da API, pois não é um parâmetro padrão da requisição TTS.

def generate_audio_from_text(text: str, voice_id: str, output_path: str, voice_settings: dict = None):
    """
    Gera um arquivo de áudio a partir do texto usando a API da ElevenLabs.

    Args:
        text (str): O texto a ser convertido em áudio.
        voice_id (str): O ID da voz a ser usada (ex: "Rachel", "Bella").
        output_path (str): O caminho para salvar o arquivo .mp3 gerado.
        voice_settings (dict, optional): Configurações de voz personalizadas. Usa DEFAULT_VOICE_SETTINGS se None.

    Returns:
        bool: True se o áudio foi gerado com sucesso, False caso contrário.
    """
    api_key = st.secrets.get("ELEVEN_API_KEY")
    if not api_key:
        st.error("Chave da API da ElevenLabs (ELEVEN_API_KEY) não encontrada nos segredos do Streamlit.")
        return False

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    current_voice_settings = voice_settings if voice_settings else DEFAULT_VOICE_SETTINGS

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2", # ou outro modelo conforme necessidade
        "voice_settings": current_voice_settings
    }

    url = ELEVENLABS_API_URL.format(voice_id=voice_id)

    try:
        response = requests.post(url, json=data, headers=headers, timeout=60) # Timeout de 60 segundos
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        # st.success(f"Áudio salvo em: {output_path}") # Log para debug, pode ser removido
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao chamar a API da ElevenLabs para o texto '{text[:50]}...': {e}")
        if hasattr(e, 'response') and e.response is not None:
            st.error(f"Detalhes da resposta: {e.response.text}")
        return False

def process_dialogue(dialogue_content: list, output_dir: str) -> list:
    """
    Processa uma lista de diálogos, gerando um arquivo de áudio para cada entrada.

    Args:
        dialogue_content (list): Lista de dicionários, cada um representando uma fala.
                                 Ex: {"text": "Olá", "voice_id": "Rachel", ...}
        output_dir (str): Diretório para salvar os arquivos de áudio gerados.

    Returns:
        list: Lista dos caminhos dos arquivos de áudio gerados com sucesso.
    """
    audio_files = []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, entry in enumerate(dialogue_content):
        text = entry.get("text")
        voice_id = entry.get("voice_id")
        # voice_name = entry.get("voice_name") # Não usado diretamente na API, mas bom para logs/UI
        # labels = entry.get("labels") # Não usado diretamente na API, mas bom para logs/UI

        if not text or not voice_id:
            st.warning(f"Entrada de diálogo inválida no índice {i}: {entry}. Pulando.")
            continue

        output_filename = f"voice_{i}.mp3"
        output_path = os.path.join(output_dir, output_filename)

        # Parâmetros de voz fixos conforme solicitado
        fixed_voice_settings = {
            "stability": 0.8,
            "similarity_boost": 0.8,
            "style": 0.5, # style exertion
            "use_speaker_boost": True
        }

        st.info(f"Gerando áudio para: '{text[:30]}...' com a voz '{voice_id}'...")
        if generate_audio_from_text(text, voice_id, output_path, voice_settings=fixed_voice_settings):
            audio_files.append(output_path)
        else:
            st.error(f"Falha ao gerar áudio para o trecho: '{text[:50]}...'")
            # Considerar se deve parar ou continuar em caso de falha em um trecho

    return audio_files

if __name__ == '__main__':
    # Exemplo de uso (requer que os segredos do Streamlit estejam configurados se executado via Streamlit)
    # Para teste local direto, você precisaria mockar st.secrets ou carregar a chave de outra forma.
    print("Este módulo é destinado a ser importado em um aplicativo Streamlit.")
    # Para testar, você pode criar um JSON de exemplo e chamar process_dialogue
    # Exemplo:
    # sample_dialogue = [
    #     {"text": "Olá mundo!", "voice_id": "21m00Tcm4TlvDq8ikWAM", "voice_name": "Rachel"},
    #     {"text": "Este é um teste.", "voice_id": "AZnzlk1XvdvUeBnXmlld", "voice_name": "Adam"}
    # ]
    # # Crie um diretório 'temp_output' para este teste
    # if not os.path.exists("temp_output"):
    #     os.makedirs("temp_output")
    # # Mock st.secrets para teste local (NÃO FAÇA ISSO EM PRODUÇÃO NO STREAMLIT)
    # class MockSecrets:
    #     def get(self, key):
    #         if key == "ELEVEN_API_KEY":
    #             return "SUA_CHAVE_API_AQUI" # Substitua pela sua chave real para teste
    #         return None
    # st.secrets = MockSecrets()
    # generated_files = process_dialogue(sample_dialogue, "temp_output")
    # print(f"Arquivos gerados: {generated_files}")

