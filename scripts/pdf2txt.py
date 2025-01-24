import os
from pdfminer.high_level import extract_text

# Directory containing the PDF files
input_dir = "data/pdf"
output_dir = "data/txt"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each PDF file in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):  # Check for PDF files
        input_path = os.path.join(input_dir, filename)
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_dir, output_filename)

        try:
            # Extract text from the PDF
            text = extract_text(input_path)

            # Save the extracted text to a .txt file
            with open(output_path, "w", encoding="utf-8") as text_file:
                text_file.write(text)

            print(f"Processed: {filename}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

print("Processing complete!")
