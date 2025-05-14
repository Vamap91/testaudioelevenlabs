# Projeto testaudioelevenlabs

Este projeto consiste em um aplicativo Streamlit que utiliza a API da ElevenLabs para gerar áudios a partir de um JSON de entrada. As falas são processadas individualmente e depois combinadas em um único arquivo de áudio com pausas entre elas.

## 🎯 Objetivo

Criar um microaplicativo chamado `testaudioelevenlabs`, hospedado em Streamlit.io, que utiliza a API da ElevenLabs para gerar áudios com vozes combinadas a partir de um JSON inserido no app. O foco é testar enredos variados com múltiplas falas e renderizar um único áudio concatenado.

## 🧱 Estrutura de Pastas

```
testaudioelevenlabs/
├── app/
│   └── streamlit_app.py               # Interface principal do app
├── audio_engine/
│   ├── elevenlabs_api.py              # Módulo de envio à ElevenLabs
│   └── audio_combiner.py              # Junta os áudios com pausa
├── data/
│   └── input.json                     # Exemplo de entrada
├── output/                            # Diretório para áudios gerados
│   ├── parts/                         # Áudios individuais antes da combinação
│   └── final_output.mp3               # Áudio combinado final
├── requirements.txt                   # Dependências do projeto
├── README.md                          # Este arquivo
```

## 📦 Dependências (`requirements.txt`)

```txt
streamlit
requests
pydub
```

## 🛠️ Pré-requisitos

Para que a biblioteca `pydub` funcione corretamente para manipulação de áudio (especialmente para formatos como MP3), é necessário ter o `ffmpeg` instalado no ambiente onde o aplicativo será executado.

- No Streamlit Community Cloud, o `ffmpeg` geralmente está disponível. Se estiver executando localmente ou em outro ambiente, pode ser necessário instalá-lo manualmente.
  - Para Debian/Ubuntu: `sudo apt update && sudo apt install ffmpeg`
  - Para macOS (usando Homebrew): `brew install ffmpeg`
  - Para Windows: Baixe os binários do site oficial do ffmpeg e adicione ao PATH.

## 🔐 API Key da ElevenLabs

A chave da API da ElevenLabs deve ser adicionada manualmente no painel do Streamlit Cloud, em `Settings > Secrets`. A chave deve ser nomeada como `ELEVEN_API_KEY`.

Exemplo no arquivo de segredos do Streamlit (não é para criar este arquivo no repositório, apenas como referência de formato no painel do Streamlit):

```toml
ELEVEN_API_KEY = "sua_chave_api_real_aqui"
```

O aplicativo (`streamlit_app.py`) está configurado para ler esta chave usando `st.secrets["ELEVEN_API_KEY"]`.

## 🧠 Lógica do Sistema

1.  **Interface do Streamlit (`streamlit_app.py`)**: Permite ao usuário colar um JSON ou fazer upload de um arquivo JSON contendo o diálogo.
2.  **Processamento do JSON**: O JSON deve ter uma chave `"content"` contendo uma lista de objetos, onde cada objeto representa uma fala com `"text"`, `"voice_id"`, etc.
3.  **Geração de Áudio por Fala (`elevenlabs_api.py`)**: Para cada fala no JSON:
    *   Uma requisição individual é enviada para a API da ElevenLabs.
    *   São aplicados parâmetros de voz fixos (`stability`, `similarity_boost`, `style`).
    *   O áudio resultante (.mp3) é salvo na pasta `output/parts/`.
4.  **Combinação dos Áudios (`audio_combiner.py`)**: Após todas as falas serem processadas:
    *   Os arquivos de áudio individuais da pasta `output/parts/` são carregados usando `pydub`.
    *   Um silêncio (pausa, por padrão de 1 segundo) é inserido entre cada segmento de áudio.
    *   O áudio final combinado é salvo como `output/final_output.mp3`.
5.  **Reprodução e Download**: O aplicativo Streamlit permite que o usuário ouça o áudio final e faça o download do arquivo `final_output.mp3`.

## 🔁 Atualizações via GitHub e Deploy no Streamlit Cloud

1.  Faça commit das suas alterações para o repositório GitHub: [https://github.com/Vamap91/testaudioelevenlabs](https://github.com/Vamap91/testaudioelevenlabs)
2.  No Streamlit Cloud, acesse as configurações do seu aplicativo (`Manage App`).
3.  Clique em `Reboot App` para aplicar as mudanças mais recentes do repositório.

## 🚀 Como Executar Localmente (para desenvolvimento)

1.  Clone o repositório.
2.  Crie e ative um ambiente virtual: `python -m venv venv && source venv/bin/activate` (ou `venv\Scripts\activate` no Windows).
3.  Instale as dependências: `pip install -r requirements.txt`.
4.  Instale o `ffmpeg` se ainda não o tiver.
5.  Crie um arquivo `.streamlit/secrets.toml` na raiz do projeto (APENAS PARA TESTE LOCAL, NÃO FAÇA COMMIT DESTE ARQUIVO) com sua chave da API:
    ```toml
    ELEVEN_API_KEY = "sua_chave_api_real_aqui"
    ```
6.  Execute o aplicativo Streamlit: `streamlit run app/streamlit_app.py`.

