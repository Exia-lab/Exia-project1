from fpdf import FPDF
from PIL import Image

pdf = FPDF()
pdf.add_page()

img = Image.open("image.jpg")
pdf.image("image.jpg")

pdf.output("image_output.pdf")
