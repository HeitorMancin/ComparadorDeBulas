# Comparador de Bulas  

Este projeto é uma aplicação desenvolvida em **Streamlit** que permite o upload de duas bulas de medicamentos no formato PDF, realiza a extração de texto, e utiliza a API **Google Generative AI (GEMINI AI)** para comparar o conteúdo de ambas, gerando um relatório detalhado em formato de tabela HTML.  

A aplicação também possui um recurso de chat para perguntas e respostas relacionadas à comparação e permite salvar o histórico da interação em PDF.  

## Funcionalidades  
- **Upload de Arquivos**: Aceita o upload de dois arquivos PDF de bulas.  
- **Extração de Texto**: Processa e extrai o texto das bulas utilizando a biblioteca `PyMuPDF`.  
- **Comparação de Bulas**: Gera uma tabela comparativa das bulas, destacando as diferenças entre os medicamentos.  
- **Interface de Chat**: Interação em linguagem natural para perguntas relacionadas à comparação.  
- **Exportação de Histórico**: Salva o histórico do chat em um arquivo PDF.  
- **Design Personalizado**: Layout responsivo com logotipo e tagline da Biolab.  

## Requisitos  
- **Python 3.9+**  
- Bibliotecas necessárias (instale via `pip install -r requirements.txt`):  
  - `streamlit`  
  - `google-generativeai`  
  - `fitz` (PyMuPDF)  
  - `weasyprint`  

## Instalação  
1. Clone este repositório:   

2. Instale as dependências:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Configure sua API Key da **Google Generative AI**:  
   - Substitua a API key no código pela sua chave de API válida.  
   
   https://aistudio.google.com/app/apikey

   para este projeto a conta utilizada para gerar a chave de API é: fabrilbiolab@gmail.com
## Uso  
1. Inicie o aplicativo:  
   ```bash  
   streamlit run app.py  
   ```  

2. Acesse a aplicação em seu navegador no endereço:  
   ```
   http://localhost:8501  
   ```  

3. Faça o upload de **duas bulas** no formato PDF.  

4. Visualize a tabela comparativa gerada.  

5. Interaja no chat para dúvidas ou análises adicionais.  

6. Baixe o histórico do chat em PDF.  

## Estrutura do Projeto  
```  
comparador de bulas/  
├── Comparador.py        # Código principal da aplicação  
├── requirements.txt     # Dependências do projeto  
├── packages.txt/        # Bibliotecas do projeto  
└── README.md            # Documentação do projeto  
```  

## Recursos Utilizados  
- **Streamlit**: Framework para criação de aplicações web interativas em Python.  
- **Google Generative AI**: API para processamento e comparação de texto.  
- **PyMuPDF**: Extração de texto de arquivos PDF.  
- **WeasyPrint**: Geração de PDF a partir de HTML e CSS.  
