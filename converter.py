from fpdf import FPDF
from PIL import Image
import streamlit as st
import io
import os
import tempfile

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
                #create temp file with original extension
                suffix = os.path.splitext(file.name)[1] or '.jpg'
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(file.getvalue())  #write bytes
                    tmp_path = tmp.name

                # now open with PIL to get dimensions
                with Image.open(tmp_path) as img:
                    width_px, height_px = img.size
            

                pdf.add_page()
                max_w = 190
                max_h = 277
                ratio = min(max_w / width_px, max_h / height_px)
                new_w = width_px * ratio
                new_h = height_px * ratio
                x = (210 - new_w) / 2

                
                # insert using the temp filename
                pdf.image(tmp_path, x=x, y=10, w=new_w, h=new_h)

                #clearn up temp file immediately after use
                os.unlink(tmp_path)

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
                suffix = os.path.splitext(file.name)[1] or '.jpg'
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(file.getvalue())
                    tmp_path = tmp.name

                with Image.open(tmp_path) as img:
                    width_px, height_px = img.size

                pdf = FPDF(orientation='P', unit='mm', format='A4')
                pdf.add_page()

                
                max_w = 190 #leave 10mm margin on each side
                max_h = 277 #leave 10mm margin on top and bottom
                ratio = min(max_w / width_px, max_h / height_px)
                new_w = width_px * ratio
                new_h = height_px * ratio
                x = (210 - new_w) / 2
                
                pdf.image(tmp_path, x=x, y=10, w=new_w, h=new_h)
                
                output = io.BytesIO()
                pdf.output(output)
                pdf_name = os.path.splitext(file.name)[0] + ".pdf"

                st.download_button(
                    f"Download PDF for {file.name}",
                    output.getvalue(),
                    file_name=pdf_name,
                    mime="application/pdf",
                    key=f'btn_{file.name}'
                )

                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")
    





