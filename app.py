import streamlit as st
import tempfile
import os
import zipfile
from PIL import Image
import fitz  # PyMuPDF

# --------------------------------------------------
# ESTILO E CORES
# --------------------------------------------------
# Carregar a logo
logo = Image.open("logo.png")

st.set_page_config(
    page_title="Conversor Ecardio - PDF para JPEG",
    page_icon=logo,
    layout="centered"
)

# CSS personalizado
st.markdown("""
    <style>
        body {
            background-color: #FFFFFF;
        }
        .main {
            background-color: #FFFFFF;
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

                        # --------------------------------------------------
                        # Conversão usando PyMuPDF
                        # --------------------------------------------------
                        doc = fitz.open(pdf_temp)
                        base_name = os.path.splitext(pdf.name)[0]

                        for i, page in enumerate(doc, start=1):
                            pix = page.get_pixmap(dpi=300)
                            img_name = f"{base_name}_pagina_{i}.jpg"
                            img_path = os.path.join(temp_dir, img_name)
                            pix.save(img_path, "JPEG")
                            zipf.write(img_path, arcname=img_name)

                        doc.close()

                # --------------------------------------------------
                # Botão de download
                # --------------------------------------------------
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
