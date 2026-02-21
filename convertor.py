import streamlit as st
from PIL import Image
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image as RLImage
from reportlab.platypus import Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate
from docx import Document
from pdf2docx import Converter
from docx2pdf import convert
import os
import tempfile

st.title("📸 Smart Document Converter App")

option = st.sidebar.selectbox(
    "Choose Function",
    ["Camera to PDF/DOCX", "DOCX to PDF", "PDF to DOCX"]
)

# ---------------------------------------------------
# 📸 CAMERA SECTION
# ---------------------------------------------------
if option == "Camera to PDF/DOCX":

    st.subheader("Take Photo")

    image_file = st.camera_input("Capture your document")

    if image_file is not None:

        image = Image.open(image_file)
        st.image(image, caption="Captured Image", use_column_width=True)

        col1, col2 = st.columns(2)

        # IMAGE TO PDF
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

        # IMAGE TO DOCX
        with col2:
            if st.button("Convert to DOCX"):

                document = Document()
                document.add_picture(image_file, width=docx.shared.Inches(4))

                docx_buffer = io.BytesIO()
                document.save(docx_buffer)

                st.download_button(
                    "Download DOCX",
                    data=docx_buffer.getvalue(),
                    file_name="document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

# ---------------------------------------------------
# DOCX TO PDF
# ---------------------------------------------------
elif option == "DOCX to PDF":

    uploaded_docx = st.file_uploader("Upload DOCX file", type=["docx"])

    if uploaded_docx:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
            tmp_docx.write(uploaded_docx.read())
            tmp_docx_path = tmp_docx.name

        output_pdf_path = tmp_docx_path.replace(".docx", ".pdf")
        convert(tmp_docx_path, output_pdf_path)

        with open(output_pdf_path, "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                file_name="converted.pdf"
            )

# ---------------------------------------------------
# PDF TO DOCX
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