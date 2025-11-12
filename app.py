import streamlit as st
import tempfile
import os
import zipfile
from pdf2image import convert_from_path

# --------------------------------------------------
# CONFIGURAÇÃO POPPLER
# --------------------------------------------------
# Caminho relativo (funciona no Streamlit Cloud se adicionado em packages.txt)
POPPLER_PATH = os.path.join(os.getcwd(), "poppler-25.07.0", "Library", "bin")

# --------------------------------------------------
# ESTILO E CORES
# --------------------------------------------------
from PIL import Image

# Carregar a logo
logo = Image.open("logo.png")

st.set_page_config(
    page_title="Conversor Ecardio - PDF para JPEG",
    page_icon=logo,  # ícone personalizado com a logo
    layout="centered"
)

# CSS personalizado
st.markdown("""
    <style>
        body {
            background-color: #F5F9FF;
        }
        .main {
            background-color: #F5F9FF;
            color: #003366;
        }
        h1, h2, h3, h4 {
            color: #003366;
            text-align: center;
        }
        .stButton>button {
            background-color: #00AEEF;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: bold;
            padding: 0.6em 1.2em;
        }
        .stButton>button:hover {
            background-color: #0095cc;
            color: white;
        }
        footer {
            text-align: center;
            color: #003366;
            font-size: 14px;
            margin-top: 2em;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------
st.title("Conversor de PDF para JPEG")
st.subheader("Converta até 5 arquivos PDF em imagens JPEG (300 DPI)")

# --------------------------------------------------
# UPLOAD
# --------------------------------------------------
uploaded_files = st.file_uploader(
    "Selecione até 5 arquivos PDF",
    type=["pdf"],
    accept_multiple_files=True
)

# --------------------------------------------------
# PROCESSAMENTO
# --------------------------------------------------
if uploaded_files:
    if len(uploaded_files) > 5:
        st.warning("⚠️ Por favor, selecione no máximo 5 arquivos PDF.")
    else:
        if st.button("Converter e Baixar"):
            with st.spinner("Convertendo arquivos, aguarde..."):
                temp_dir = tempfile.mkdtemp()
                zip_path = os.path.join(temp_dir, "imagens_convertidas.zip")

                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for pdf in uploaded_files:
                        pdf_temp = os.path.join(temp_dir, pdf.name)
                        with open(pdf_temp, "wb") as f:
                            f.write(pdf.read())

                        # Converter PDF → JPEG
                        pages = convert_from_path(pdf_temp, dpi=300, poppler_path=POPPLER_PATH)
                        base_name = os.path.splitext(pdf.name)[0]

                        for i, page in enumerate(pages, start=1):
                            img_name = f"{base_name}_pagina_{i}.jpg"
                            img_path = os.path.join(temp_dir, img_name)
                            page.save(img_path, "JPEG", quality=95)
                            zipf.write(img_path, arcname=img_name)

                with open(zip_path, "rb") as f:
                    st.download_button(
                        label="📦 Baixar imagens convertidas (ZIP)",
                        data=f,
                        file_name="imagens_convertidas.zip",
                        mime="application/zip"
                    )

            st.success("✅ Conversão concluída com sucesso!")

# --------------------------------------------------
# RODAPÉ
# --------------------------------------------------
st.markdown("<footer>© 2025 Ecardio — Conversor interno</footer>", unsafe_allow_html=True)
