import io
from PIL import Image
import rembg

# Define the input JPG file path
input_jpg_path = 'input.jpg'

# Define the output PNG file path for the background-removed image
output_removed_bg_path = 'output_removed_bg.png'

# Open the JPG image
jpg_image = Image.open(input_jpg_path)

# Convert the image to PNG format with a transparent background
png_image = jpg_image.convert('RGBA')

# Convert the PNG image to a byte-like object
with io.BytesIO() as byte_io:
    png_image.save(byte_io, 'PNG')
    byte_io.seek(0)
    byte_image = byte_io.read()

# Remove the background using "rembg" and the byte-like object
rembg_output = rembg.remove(byte_image)

# Save the background-removed image as a PNG file
with open(output_removed_bg_path, 'wb') as output_file:
    output_file.write(rembg_output)

print(f'JPG image converted to PNG with transparent background and saved as {output_removed_bg_path}')
