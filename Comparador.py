import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import time
import os
from weasyprint import HTML, CSS
from io import BytesIO

# Configurando a API Key do GEMINI AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"]) 

# Definindo o layout em WideScreen
st.set_page_config(layout="wide")

# Definindo o layout com duas colunas
col1, col2 = st.columns([1, 1])  # Duas colunas de tamanho igual

# Logotipo na primeira coluna (alinhada à esquerda)
with col1:
    st.image("https://www.biolabfarma.com.br/wp-content/themes/biolabtheme/assets/images/logo-menu.png", width=150)

# TAG 'Viva a Evolução' na segunda coluna (alinhada à direita)
with col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end;">
            <img src="https://www.biolabfarma.com.br/wp-content/themes/biolabtheme/assets/images/tagline-viva-evolucao.png" style="max-width: 100%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

# Código HTML e CSS para a faixa no cabeçalho
html_code = """
<div style='
    background: #bfd730;
    background: linear-gradient(133deg, #bfd730 10%, #008fc4 60%);
    background: -webkit-linear-gradient(133deg, #bfd730 10%, #008fc4 60%);
    background: -moz-linear-gradient(133deg, #bfd730 10%, #008fc4 60%);
    margin: 0px 0px 0px 0px;
    width: 100%;
    position: fixed;
    padding: 10px;
    bottom: 0;
    left: 0;
    text-align: center;
    color: white;
    font-family: Arial, sans-serif;
    font-size: 24px; 
    font-weight: bold; 
'>
   Comparador de Bulas
</div>
"""

# Renderiza o HTML na aplicação Streamlit
components.html(html_code, height=50)

# Funções definidas antes do uso
def save_uploaded_file(uploaded_file):
    # Salvar o arquivo no diretório temporário
    temp_path = os.path.join("tempDir", uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_path

def upload_to_gemini(file_path, mime_type=None):
    file = genai.upload_file(file_path, mime_type=mime_type)
    return file

def wait_for_files_active(files):
    st.write("Esperando o processamento dos arquivos...")
    progress_bar = st.progress(0)
    for i, name in enumerate((file.name for file in files)):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"Arquivo {file.name} falhou no processamento")
        progress_bar.progress((i + 1) / len(files))
    st.write("Todos os arquivos foram processados com sucesso!")

def save_chat_to_pdf(chat_history):
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; font-size: 12px; margin: 0; padding: 0; table-layout: fixed;}
            table { border: 1px solid #ddd; width: 100%; max-width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; word-wrap: break-word; }
            th { background-color: #f4f4f4; text-align: left; }
            .message { margin-bottom: 10px; }
            .user { color: blue; }
            .assistant { color: black; }
            .logo {top: 0px; left: 10px; width: 100px; }
        </style>
    </head>
    <body> 
    <img src="https://www.biolabfarma.com.br/wp-content/themes/biolabtheme/assets/images/logo-menu.png" class="logo" alt="Logo Biolab", width="80">
    """
    for message in chat_history:
        role = "Pergunta" if message["role"] == "user" else " "
        html_content += f'<div class="message {role}"><strong>{role.capitalize()}</strong> {message["content"]}</div>'
    html_content += "</body></html>"

    pdf_file_path = os.path.join("tempDir", "chat_history.pdf")
    HTML(string=html_content).write_pdf(pdf_file_path, stylesheets=[CSS(string='body { font-family: Arial, sans-serif; font-size: 12px; }')])
    return pdf_file_path

# File upload
uploaded_files = st.file_uploader(
    "Faça o upload de **duas** bulas (no formato PDF)", 
    accept_multiple_files=True, 
    key="file_uploader_1"
)

# Verificação de número de arquivos
if uploaded_files:
    if len(uploaded_files) != 2:
        st.error("Atenção: Faça o upload de **exatamente dois** arquivos PDF para comparar.")
    else:
        # Criar diretório temporário se não existir
        os.makedirs("tempDir", exist_ok=True)
        
        file_paths = [save_uploaded_file(file) for file in uploaded_files]
        files = [upload_to_gemini(path, mime_type="application/pdf") for path in file_paths]
        wait_for_files_active(files)
        
        # Define model and safety settings
        safety_settings = {
          'HARASSMENT': 'BLOCK_NONE',  
          'HATE': 'BLOCK_NONE',        
          'SEXUAL': 'BLOCK_NONE',       
          'DANGEROUS': 'BLOCK_NONE'     
        }

        generation_config = {
            "temperature": 0,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=( 
                    """Responda sempre em formato de tabela HTML pronto para renderização sem o ```html, comparando dois medicamentos fornecidos. A tabela deve incluir as 4 colunas seguintes:
                    Item: A seção da bula sendo comparada.
                    Nome do Medicamento 1 (Resumo): Um breve resumo do primeiro medicamento (ex: Depakene).
                    Nome do Medicamento 2 (Resumo): Um breve resumo do segundo medicamento (ex: Epilenil).
                    Diferença: Uma descrição concisa das diferenças entre os medicamentos.
                    Instruções Adicionais:
                    Compare todas as seções da bula de ambos os medicamentos e dica em cada resumo de cada seção, a página onde se encontra o conteúdo.
                    Ignore diferenças de formatação, focando apenas no conteúdo.
                    **Procure nas bulas se contém imagens, e somente caso contiver, inclua a seção 'Imagens' na tabela e fale de maneira bem detalhada a descrição e as diferenças das imagens.**
                    Faça em último lugar uma seção sobre os dizeres legais.
                    Os resumos dos medicamentos devem ser limitados a poucas palavras.
                    Se não houver diferença em uma seção, indique 'Sem diferença'
                    Não inclua frases adicionais antes ou depois da tabela"""),
            safety_settings=safety_settings
        )

        # Inicialização da conversa
        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(
                history=[{
                    "role": "user",
                    "parts": [files[0], files[1]],
                }]
            )
            
            # Enviar a mensagem inicial e armazenar a resposta
            with st.spinner("Processando a comparação inicial..."):
                response = st.session_state.chat.send_message("Compare as bulas carregadas e gere um relatório comparativo, com as diferenças resumidas.")
            st.session_state.messages = [{"role": "assistant", "content": response.text}]

        def main():
            # Inicializa o estado das mensagens, se não estiver definido
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Exibe as mensagens anteriores
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"], unsafe_allow_html=True)

            # Entrada do usuário
            if prompt := st.chat_input("Faça uma Pergunta:"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Responde à pergunta
                with st.spinner("Processando sua pergunta..."):
                    response = st.session_state.chat.send_message(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant"):
                    st.markdown(response.text)

            # Salva o histórico do chat em PDF
            pdf_file_path = save_chat_to_pdf(st.session_state.messages)
            with open(pdf_file_path, "rb") as pdf_file:
                st.download_button(
                    label="Download do histórico do chat",
                    data=pdf_file,
                    file_name="Comparacao_Bulas.pdf",
                    mime="application/pdf"
                )

        if __name__ == "__main__":
            main()
