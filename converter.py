from fpdf import FPDF
from PIL import Image
import streamlit as st
import io
import os

st.title("Images to PDF Converter")
st.write("This app converts all kinds of images to a pdf file.")

uploaded_files = st.file_uploader(
    "Choose image files", 
    accept_multiple_files=True, 
    type=['jpg', 'jpeg', 'png', 'bmp', 'tiff']
)
combine = st.checkbox("Combine all images into a single PDF", value=False)

if uploaded_files and st.button("Convert to PDF"):
    if combine:
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        for file in uploaded_files:
            try:
                img = Image.open(file)
                width_px, height_px = img.size

                pdf.add_page()
                max_w = 190
                max_h = 277
                ratio = min(max_w / width_px, max_h / height_px)
                new_w = width_px * ratio
                new_h = height_px * ratio
                x = (210 - new_w) / 2

                
                file.seek(0)
                pdf.image(file, x=x, y=10, w=new_w, h=new_h)
            except Exception as e:
                st.error(f"Error with {file.name}: {e}")

        output = io.BytesIO()
        pdf.output(output)

        if len(uploaded_files) == 1:
            combined_name = os.path.splitext(uploaded_files[0].name)[0] + ".pdf"
        else : 
            combined_name = "combined_images.pdf"

        st.download_button(
            "Download combined PDF",
            output.getvalue(),
            file_name = combined_name,
            mime="application/pdf"
        )
    else :
        for file in uploaded_files:
            try:
                img = Image.open(file)
                width_px, height_px = img.size

                pdf = FPDF(orientation='P', unit='mm', format='A4')
                pdf.add_page()

                
                max_w = 190 #leave 10mm margin on each side
                max_h = 277 #leave 10mm margin on top and bottom
                ratio = min(max_w / width_px, max_h / height_px)
                new_w = width_px * ratio
                new_h = height_px * ratio
                x = (210 - new_w) / 2

                file.seek(0)
                pdf.image(file, x=x, y=10, w=new_w, h=new_h)
                
                output = io.BytesIO()
                pdf.output(output)

                st.download_button(
                    f"Download PDF for {file.name}",
                    output.getvalue(),
                    file_name=f'{os.path.splitext(file.name)[0]}.pdf',
                    mime="application/pdf",
                    key=file.name
                )
                
            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")
    





