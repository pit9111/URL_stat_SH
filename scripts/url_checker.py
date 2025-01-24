import csv
import os
import re
import pandas as pd

def load_forges(csv_file):
    """
    Load the forge keywords from a CSV file, ignoring unnecessary columns.
    """
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Skip the header and return the first column as a list
            forges = [row[0] for row in reader if row]  # Ensure row is not empty
        return forges
    except Exception as e:
        print(f"Failed to load forges from {csv_file}: {e}")
        return []

def extract_urls_from_files(input_dir, file_extension):
    """
    Extract unique URLs from text files in the specified directory with a given extension.
    Also track the filename for each URL.
    """
    urls_with_files = []
    url_pattern = re.compile(
        r'https?://(?:www\.)?[-\w@:%._\+~#=]{1,256}\.[a-zA-Z]{2,6}\b(?:[-\w@:%_\+.~#?&/=]*)'
    )

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(f".{file_extension}"):
            file_path = os.path.join(input_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read().replace('\r', '').replace('\n', '')
                    found_urls = url_pattern.findall(text)
                    for url in found_urls:
                        urls_with_files.append({'url': url, 'filename': filename})  # Track URL and file
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

    return urls_with_files

def filter_urls_by_forges(urls_with_files, forges):
    """
    Filter URLs that belong to one of the specified forges and exclude:
      - Unwanted domains (e.g., "doi.org", "kermitt2/grobid").
      - URLs already present in the registered_urls list or set.
    """
    filtered = [
        url_file
        for url_file in urls_with_files
        if (
            any(forge in url_file['url'] for forge in forges) and  # Check forge match
            "doi.org" not in url_file['url'] and                  # Exclude unwanted domains
            "kermitt2/grobid" not in url_file['url'] and         # Exclude specific URL pattern
            "XMLSchema-instance" not in url_file['url'] and        # Exclude specific URL pattern
            "xlink" not in url_file['url']         # Exclude specific URL pattern
        )
    ]
    return filtered


def save_urls_to_csv(urls_with_files, output_file):
    """
    Save the filtered URLs and filenames to a CSV file.
    """
    try:
        # Create a DataFrame with URL and filename columns
        df = pd.DataFrame(urls_with_files)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Saved results to {output_file}")
    except Exception as e:
        print(f"Failed to save URLs to {output_file}: {e}")

def checker_by_type(file_type):
    """
    Main function to process files of a given type and extract relevant URLs.
    """
    # Paths and settings
    csv_file = "./data/SH/SH_forge.csv"
    input_dir = f"data/{file_type}"
    output_file = f'./result/url_forge_founded_{file_type}.csv'

    # Load forge keywords
    forges = load_forges(csv_file)
    if not forges:
        print("No forge keywords loaded. Exiting...")
        return

    # Extract URLs and their source filenames
    urls_with_files = extract_urls_from_files(input_dir, file_type)

    # Filter URLs based on forges
    filtered_urls_with_files = filter_urls_by_forges(urls_with_files, forges)

    # Save results to CSV
    save_urls_to_csv(filtered_urls_with_files, output_file)

# Run for 'xml' and 'txt' file types
checker_by_type('xml')
checker_by_type('txt')


# Define the more detailed regex
swh_regexp = re.compile(
    r"swh:1:(cnt|dir|rel|rev|snp):[0-9a-f]{40}"
    r"(;(origin|visit|anchor|path|lines)=\S+)*$"
)

def find_swhids_in_text(text):
    """
    Find all Software Heritage Identifiers (SWHIDs) in the given text using a detailed regex.
    """
    return swh_regexp.findall(text)


def extract_swhids_from_files(input_dir, type):
    """
    Extract all SWHIDs from .txt and .pdf files in the specified directory
    and save the results to a CSV file.
    """
    output_csv = f"./result/swhid_{type}.csv"
    swhid_results = []

    # Iterate through all files in the directory
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if filename.lower().endswith(f".{type}"):
            # Process text files
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read().replace('\r', '').replace('\n', '')
                    swhids = find_swhids_in_text(text)
                    for swhid in swhids:
                        swhid_results.append({"file": filename, "swhid": swhid})
                    swhid_results.append({"file": filename, "swhid": None})
            except Exception as e:
                print(f"Error reading TXT {file_path}: {e}")

    # Write results to CSV
    try:
        with open(output_csv, mode="w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["file", "swhid"])
            writer.writeheader()
            writer.writerows(swhid_results)
        print(f"SWHID extraction complete. Results saved to {output_csv}")
    except Exception as e:
        print(f"Error writing CSV {output_csv}: {e}")


# Example usage
extract_swhids_from_files("./data/txt","txt")
extract_swhids_from_files("./data/xml","xml")