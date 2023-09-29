import cups

# Create a CUPS connection
conn = cups.Connection()

# Get a list of all available printers
printers = conn.getPrinters()

# Iterate through the list of printers and check their attributes
for printer_name, _ in printers.items():
    print(f"Checking printer: {printer_name}")

    # Get the printer attributes
    printer_info = conn.getPrinterAttributes(printer_name)

    # Check for paper-related attributes
    if 'media' in printer_info:
        media_info = printer_info['media']

        # Iterate through media attributes
        for media_name, media_data in media_info.items():
            if 'type' in media_data and media_data['type'] == 'stationery':
                # Check if this media type represents paper
                if 'bottom-margin' in media_data and 'top-margin' in media_data:
                    # Retrieve margin values which might give paper usage information
                    bottom_margin = int(media_data['bottom-margin'])
                    top_margin = int(media_data['top-margin'])
                    # Calculate paper remaining based on margin values
                    paper_remaining = top_margin - bottom_margin
                    print(f"Paper Remaining in {media_name}: {paper_remaining} mm")

    # Add more checks for other paper-related attributes as needed

# Note: The specific keys and values to check for paper levels may vary based on your printer model and driver.
