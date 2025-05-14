"""
Aplicativo Streamlit para gerar áudios combinados usando a API da ElevenLabs.
"""
import streamlit as st
import json
import os
from elevenlabs_api import process_dialogue
from audio_combiner import combine_audio_files

# Define os diretórios de saída
OUTPUT_DIR_PARTS = "output/parts"
OUTPUT_DIR_FINAL = "output"
FINAL_AUDIO_FILENAME = "final_output.mp3"
FINAL_AUDIO_PATH = os.path.join(OUTPUT_DIR_FINAL, FINAL_AUDIO_FILENAME)

# Cria os diretórios de saída se não existirem
os.makedirs(OUTPUT_DIR_PARTS, exist_ok=True)
os.makedirs(OUTPUT_DIR_FINAL, exist_ok=True)

st.set_page_config(page_title="Test Audio ElevenLabs", layout="wide")

st.title("🎙️ Teste de Áudio com ElevenLabs")
st.markdown("Crie áudios com múltiplas falas e vozes combinadas a partir de um JSON.")

# Verifica se a chave da API está configurada
if not st.secrets.get("ELEVEN_API_KEY"):
    st.error("🚨 A chave da API da ElevenLabs (ELEVEN_API_KEY) não está configurada nos segredos do Streamlit. Por favor, adicione-a em `Settings > Secrets` no Streamlit Cloud para que o aplicativo funcione.")
    st.stop()

# Carrega o JSON de exemplo
DEFAULT_JSON_PATH = "data/input.json"

def load_json_example():
    try:
        with open(DEFAULT_JSON_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.warning(f"Arquivo de exemplo JSON ({DEFAULT_JSON_PATH}) não encontrado.")
        return "{\n  \"content\": [\n    {\n      \"text\": \"Exemplo de fala não carregado.\",\n      \"voice_id\": \"Rachel\",\n      \"voice_name\": \"Narradora\",\n      \"labels\": [\"neutral\"]\n    }\n  ]\n}"
    except Exception as e:
        st.error(f"Erro ao carregar o JSON de exemplo: {e}")
        return "{}"

json_example = load_json_example()

st.subheader("Insira seu JSON aqui ou use o exemplo abaixo:")

json_input_area = st.text_area("Conteúdo JSON do Diálogo", value=json_example, height=300, key="json_input")

st.subheader("Ou faça upload de um arquivo JSON:")
uploaded_file = st.file_uploader("Escolha um arquivo JSON", type=['json'], key="json_upload")

if uploaded_file is not None:
    try:
        json_string = uploaded_file.read().decode("utf-8")
        # Atualiza a área de texto com o conteúdo do arquivo carregado
        st.session_state.json_input = json_string 
        st.success("Arquivo JSON carregado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo JSON: {e}")
        json_string = json_input_area # Mantém o que estava na área de texto
else:
    json_string = json_input_area

if st.button("🎧 Gerar Áudio Combinado", key="generate_button"):
    if not json_string.strip():
        st.warning("Por favor, insira um conteúdo JSON válido.")
    else:
        try:
            data = json.loads(json_string)
            dialogue_content = data.get("content")

            if not dialogue_content or not isinstance(dialogue_content, list):
                st.error("O JSON deve conter uma chave 'content' com uma lista de falas.")
            else:
                with st.spinner("Gerando áudios individuais..."):
                    # Limpa arquivos de áudio anteriores das partes
                    for f in os.listdir(OUTPUT_DIR_PARTS):
                        os.remove(os.path.join(OUTPUT_DIR_PARTS, f))
                    
                    generated_audio_parts = process_dialogue(dialogue_content, OUTPUT_DIR_PARTS)
                
                if not generated_audio_parts:
                    st.error("Nenhuma parte de áudio foi gerada. Verifique os logs para mais detalhes.")
                else:
                    st.success(f"{len(generated_audio_parts)} partes de áudio geradas com sucesso!")
                    
                    with st.spinner("Combinando áudios..."):
                        # Limpa o arquivo de áudio final anterior
                        if os.path.exists(FINAL_AUDIO_PATH):
                            os.remove(FINAL_AUDIO_PATH)

                        pause_ms = 1000 # Pausa de 1 segundo entre as falas
                        success_combine = combine_audio_files(generated_audio_parts, FINAL_AUDIO_PATH, pause_duration_ms=pause_ms)
                    
                    if success_combine and os.path.exists(FINAL_AUDIO_PATH):
                        st.success("🎉 Áudio final combinado gerado com sucesso!")
                        
                        st.subheader("Ouvir o resultado:")
                        try:
                            audio_file = open(FINAL_AUDIO_PATH, 'rb')
                            audio_bytes = audio_file.read()
                            st.audio(audio_bytes, format='audio/mp3')
                            audio_file.close()

                            # Link para download
                            with open(FINAL_AUDIO_PATH, "rb") as fp:
                                btn = st.download_button(
                                    label="📥 Baixar Áudio Final (.mp3)",
                                    data=fp,
                                    file_name=FINAL_AUDIO_FILENAME,
                                    mime="audio/mp3"
                                )
                        except Exception as e:
                            st.error(f"Erro ao tentar reproduzir ou fornecer download do áudio: {e}")

                    else:
                        st.error("Falha ao combinar os áudios. Verifique se o ffmpeg está instalado e acessível.")

        except json.JSONDecodeError:
            st.error("Erro de decodificação do JSON. Por favor, verifique a formatação do seu JSON.")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")

st.markdown("---")
st.markdown("Desenvolvido por Manus. Baseado nas especificações do projeto `testaudioelevenlabs`.")
st.markdown("Lembre-se de que `ffmpeg` precisa estar disponível no ambiente para que a combinação de áudio com `pydub` funcione corretamente.")

