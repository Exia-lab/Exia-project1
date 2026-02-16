from fpdf import FPDF
from PIL import Image
import glob
import os

pdf = FPDF()
pdf.add_page()

for file in glob.glob("*.jpg"):
    img = Image.open(file)
    base = os.path.splitext(file)[0]


pdf.image(file, x=10, y=10, w=img.width / 5, h=img.height / 5)
pdf.output(base + '.pdf')
