from PIL import Image

img = Image.open('input.png')
img = img.convert('RGB')
img.save('output.pdf')
print('done')

