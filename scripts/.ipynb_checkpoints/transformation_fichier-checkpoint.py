import bz2
import pandas as pd
import pdfplumber
import os

def extract_csv(bz2_filename, output_csv):
    """Extrait un fichier CSV compressé en BZ2 et le charge en DataFrame."""
    with bz2.BZ2File(bz2_filename, 'rb') as file:
        data = file.read()
    
    temp_csv = os.path.splitext(bz2_filename)[0] + ".csv"
    with open(temp_csv, 'wb') as output:
        output.write(data)
    
    df = pd.read_csv(temp_csv)
    df.to_csv(output_csv, index=False)
    print(f"Fichier CSV extrait et sauvegardé sous {output_csv}")
    return df

def pdf_to_text(pdf_folder, output_folder):
    """Extrait le texte des fichiers PDF et les enregistre en fichiers texte."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            output_txt_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            
            with open(output_txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)
            
            print(f"Texte extrait et enregistré dans {output_txt_path}")

# Exemple d'utilisation
csv_df = extract_csv("base-origins-forges-2024-05-16_at_least_2.csv.bz2", "output.csv")
pdf_to_text("pdf", "pdftotext")
