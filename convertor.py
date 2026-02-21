import streamlit as st
from PIL import Image
import io
import tempfile
import os

from reportlab.platypus import SimpleDocTemplate, Image as RLImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from docx import Document
from docx.shared import Inches
from pdf2docx import Converter

st.title("📸 Smart Document Converter (Cloud Version)")

option = st.sidebar.selectbox(
    "Choose Function",
    ["Camera to PDF/DOCX", "PDF to DOCX"]
)

# ---------------------------------------------------
# 📸 CAMERA SECTION
# ---------------------------------------------------
if option == "Camera to PDF/DOCX":

    image_file = st.camera_input("Capture your document")

    if image_file is not None:

        image = Image.open(image_file)
        st.image(image, caption="Captured Image", use_column_width=True)

        col1, col2 = st.columns(2)

        # IMAGE → PDF
        with col1:
            if st.button("Convert to PDF"):

                pdf_buffer = io.BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
                elements = []

                temp_image_path = "temp_image.jpg"
                image.save(temp_image_path)

                elements.append(RLImage(temp_image_path, width=5*inch, height=7*inch))
                doc.build(elements)

                st.download_button(
                    "Download PDF",
                    data=pdf_buffer.getvalue(),
                    file_name="document.pdf",
                    mime="application/pdf"
                )

        # IMAGE → DOCX
        with col2:
            if st.button("Convert to DOCX"):

                document = Document()
                document.add_picture(image_file, width=Inches(4))

                docx_buffer = io.BytesIO()
                document.save(docx_buffer)

                st.download_button(
                    "Download DOCX",
                    data=docx_buffer.getvalue(),
                    file_name="document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

# ---------------------------------------------------
# PDF → DOCX
# ---------------------------------------------------
elif option == "PDF to DOCX":

    uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"])

    if uploaded_pdf:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(uploaded_pdf.read())
            tmp_pdf_path = tmp_pdf.name

        output_docx_path = tmp_pdf_path.replace(".pdf", ".docx")

        cv = Converter(tmp_pdf_path)
        cv.convert(output_docx_path)
        cv.close()

        with open(output_docx_path, "rb") as f:
            st.download_button(
                "Download DOCX",
                f,
                file_name="converted.docx"
            )
