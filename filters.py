from PIL import Image, ImageFilter, ImageOps

# Open an image
image = Image.open('input.jpg')

# Convert the image to grayscale
gray_image = ImageOps.grayscale(image)

# Apply a sepia tone effect
sepia_image = ImageOps.colorize(gray_image, "#704214", "#C0A080")

# Apply a vintage effect
vintage_image = sepia_image.filter(ImageFilter.SEPHIA)

# Add a vignette effect (darkening the edges)
vintage_image = ImageOps.vignette(vintage_image, scale=2.0)

# Apply a mosaic effect
mosaic_image = vintage_image.filter(ImageFilter.MedianFilter(size=7))

# Save the final image with multiple effects
mosaic_image.save('output_photobooth.jpg')
