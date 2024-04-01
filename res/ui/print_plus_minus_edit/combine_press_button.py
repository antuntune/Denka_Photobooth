from PIL import Image

def paste_image(foreground_image_path, background_image_path, output_image_path, position):
    """
    Paste a foreground image onto a background image and save the final image.

    Parameters:
    foreground_image_path (str): The path to the foreground image file.
    background_image_path (str): The path to the background image file.
    output_image_path (str): The path to save the final image.
    position (tuple): The position (x, y) where the foreground image will be pasted onto the background image.
    """
    foreground_image = Image.open(foreground_image_path)
    background_image = Image.open(background_image_path)

    # Convert background image to RGBA mode to support transparency
    background_image = background_image.convert("RGBA")

    # Paste the foreground image onto the background image at the specified position
    background_image.paste(foreground_image, position, mask=foreground_image)

    # Save the final image
    background_image.save(output_image_path)


# Example usage:
foreground_image_path = "minus_button_resized.png"
background_image_path = "bg_final_red.png"
output_image_path = "final_image_red.png"
position = (0, 0)  # Position where you want to paste the foreground image

paste_image(foreground_image_path, background_image_path, output_image_path, position)
