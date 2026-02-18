from fpdf import FPDF
from PIL import Image
import glob
import os

image_files = []
for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']:
    image_files.extend(glob.glob(ext))
    image_files.extend(glob.glob(ext.upper()))
image_files.sort()

for file in image_files:
    try:
            
        img = Image.open(file)
        width, height = img.size

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()

        #calculate scaling so the image fits nicely with some margin
        #option 1: scale to 90% of page width
        page_width = 190 #leave 10mm margin on each side
        page_height = 277 #leave 10mm margin on top and bottom
        scale = page_width / width
        new_width = page_width
        new_height = height * scale

        if new_height > page_height:
            scale = page_height / height
            new_width = width * scale
            new_height = page_height

        #center the image on the page
        x = (210 - new_width) / 2
        y = (297 - new_height) / 2

        pdf.image(file, x=x, y=y, w=new_width, h=new_height)
        base = os.path.splitext(file)[0]
        output_filename = base + ".pdf"
        pdf.output(output_filename)
        print(f"Converted {file} to {output_filename}")

    except Exception as e:
        print(f"Error processing {file}: {e}")
    





