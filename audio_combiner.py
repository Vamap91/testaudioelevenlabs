"""
Módulo para combinar múltiplos arquivos de áudio com pausas entre eles.
"""
from pydub import AudioSegment
import os
import streamlit as st # Para logging, se necessário

def combine_audio_files(audio_file_paths: list, output_path: str, pause_duration_ms: int = 1000):
    """
    Combina uma lista de arquivos de áudio em um único arquivo, com pausas entre eles.

    Args:
        audio_file_paths (list): Lista de caminhos para os arquivos de áudio .mp3 a serem combinados.
        output_path (str): Caminho para salvar o arquivo de áudio combinado final.
        pause_duration_ms (int): Duração da pausa em milissegundos a ser inserida entre os áudios.

    Returns:
        bool: True se a combinação for bem-sucedida, False caso contrário.
    """
    if not audio_file_paths:
        st.warning("Nenhum arquivo de áudio fornecido para combinação.")
        return False

    combined_audio = None
    pause = AudioSegment.silent(duration=pause_duration_ms)

    try:
        for i, file_path in enumerate(audio_file_paths):
            if not os.path.exists(file_path):
                st.error(f"Arquivo de áudio não encontrado: {file_path}. Pulando.")
                continue
            
            try:
                segment = AudioSegment.from_mp3(file_path)
            except Exception as e:
                st.error(f"Erro ao carregar o arquivo de áudio {file_path} com pydub: {e}. Certifique-se de que o ffmpeg está instalado e no PATH.")
                return False # Falha crítica se um segmento não puder ser carregado

            if combined_audio is None:
                combined_audio = segment
            else:
                combined_audio += pause + segment
        
        if combined_audio:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            combined_audio.export(output_path, format="mp3")
            # st.success(f"Áudio combinado salvo em: {output_path}") # Log para debug
            return True
        else:
            st.warning("Nenhum áudio válido processado para combinação.")
            return False

    except Exception as e:
        st.error(f"Erro durante a combinação dos áudios: {e}")
        return False

if __name__ == '__main__':
    # Exemplo de uso (requer arquivos de áudio de exemplo e ffmpeg)
    print("Este módulo é destinado a ser importado.")
    # Para testar:
    # 1. Crie uma pasta 'temp_audio_parts' e coloque alguns arquivos .mp3 nela (ex: part1.mp3, part2.mp3)
    # 2. Crie uma pasta 'temp_output_combined'
    # mock_audio_files = ["temp_audio_parts/part1.mp3", "temp_audio_parts/part2.mp3"]
    # # Certifique-se de que os arquivos de áudio existem para o teste
    # for f_path in mock_audio_files:
    #     if not os.path.exists(f_path):
    #         print(f"Arquivo de teste {f_path} não encontrado. Crie-o para testar.")
    #         exit()
    # combined_file_path = "temp_output_combined/final.mp3"
    # if combine_audio_files(mock_audio_files, combined_file_path, pause_duration_ms=1500):
    #     print(f"Áudio combinado de teste salvo em: {combined_file_path}")
    # else:
    #     print("Falha ao combinar áudios de teste.")

