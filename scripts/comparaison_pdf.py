import csv
import os
import re

def extract_domains_from_csv(csv_path):
    domains = set()
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            if len(row) > 1:
                domains.add(row[1].strip())  # Extract domain from second column
    return domains

def search_domains_in_texts(pdf_text_folder, domains, output_txt_path):
    domain_pattern = re.compile(r'\b(' + '|'.join(re.escape(domain) for domain in domains) + r')\b')
    url_pattern = re.compile(r'https?://\S+')  # Regex to extract URLs
    matches = {}
    
    for filename in os.listdir(pdf_text_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(pdf_text_folder, filename)
            with open(file_path, "r", encoding="utf-8") as txt_file:
                text = txt_file.read().splitlines()
                
                for line in text:
                    found = domain_pattern.findall(line)
                    if found:
                        urls = url_pattern.findall(line)  
                        if filename not in matches:
                            matches[filename] = []
                        for url in urls:
                            matches[filename].append((found[0], url))  
    
    with open(output_txt_path, "w", encoding="utf-8") as output_file:
        for file, found_domains in matches.items():
            for domain, url in found_domains:
                output_file.write(f"{file}: {domain} (match: {url})\n")
    
    print(f"Correspondances enregistrées dans {output_txt_path}")

# Exemple d'utilisation
domains = extract_domains_from_csv("base-origins-forges-2024-05-16.csv")
search_domains_in_texts("pdftotext", domains, "matched_domains.txt")
