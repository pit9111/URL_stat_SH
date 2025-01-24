import os
import re

def find_urls_in_text(text):
    """
    Find all URLs in the given text using a regex pattern.
    """
    url_pattern = re.compile(
        r'https?://(?:www\.)?[-\w@:%._\+~#=]{1,256}\.[a-zA-Z]{2,6}\b(?:[-\w@:%_\+.~#?&/=]*)'
    )
    return url_pattern.findall(text)

def process_txt_files(input_dir, type):
    """
    Process all .txt files in the given directory to extract URLs and save them to an output file.
    """
    urls = set()
    output_file = f"result/urls_regex_{type}.txt"
    input_dir = f'{input_dir}/{type}'
    # Process each .txt file in the directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(f".{type}"):
            file_path = os.path.join(input_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
                    found_urls = find_urls_in_text(text)
                    urls.update(found_urls)  # Avoid duplicate URLs
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    # Write all URLs to the output file
    try:
        with open(output_file, "w", encoding="utf-8") as out_file:
            for url in sorted(urls):
                out_file.write(url + "\n")
        print(f"Extracted URLs saved to {output_file}")
    except Exception as e:
        print(f"Failed to write output file: {e}")

# Set the input directory and output file paths
input_directory = "data/"  # Replace with your directory path  # Replace with your desired output file path

# Run the URL extraction
process_txt_files(input_directory, 'xml')
process_txt_files(input_directory, 'txt')
