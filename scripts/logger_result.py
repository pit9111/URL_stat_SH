import logging
import pandas as pd

# Load CSV files into DataFrames
urls_found_xml = pd.read_csv("result/urls_found_xml.csv")
urls_found_txt = pd.read_csv("result/urls_found_txt.csv")
urls_forge_found_xml = pd.read_csv("result/urls_forge_found_xml.csv")
urls_forge_found_txt = pd.read_csv("result/urls_forge_found_txt.csv")
swhid_xml = pd.read_csv("result/swhid_xml.csv")
swhid_txt = pd.read_csv("result/swhid_txt.csv")
forge_count_xml = pd.read_csv("result/forge_count_xml.csv")
forge_count_txt = pd.read_csv("result/forge_count_txt.csv")

# Set up logging
logging.basicConfig(filename='app.log', filemode="w", level=logging.INFO, format='%(message)s')

# Function to log results
def log_result(message):
    logging.info(message)
    print(message)

# Count the number of lines in urls_found
num_lines_xml = len(urls_found_xml)
num_lines_txt = len(urls_found_txt)
log_result(f"Number of lines: {num_lines_xml} (XML) | {num_lines_txt} (TXT)")

# Count the number of lines in urls_forge_found
num_lines_forge_xml = len(urls_forge_found_xml)
num_lines_forge_txt = len(urls_forge_found_txt)
log_result(f"Number of lines: {num_lines_forge_xml} (XML) | {num_lines_forge_txt} (TXT)")

# Count the number of False responses
false_count_xml = (urls_forge_found_xml['response'] == False).sum()
false_count_txt = (urls_forge_found_txt['response'] == False).sum()
log_result(f"Number of False responses: {false_count_xml}/{num_lines_forge_xml} (XML) | {false_count_txt}/{num_lines_forge_txt} (TXT)")

# Get top 3 forges based on 'Link Count'
top_3_forges_xml = forge_count_xml.sort_values(by="Link Count", ascending=False).head(3)
top_3_forges_txt = forge_count_txt.sort_values(by="Link Count", ascending=False).head(3)
log_result("Top 3 forges (XML):")
log_result(top_3_forges_xml[['Forge', 'Link Count']].to_string(index=False))
log_result("Top 3 forges (TXT):")
log_result(top_3_forges_txt[['Forge', 'Link Count']].to_string(index=False))

# Count the number of lines in swhid
num_lines_swhid_xml = len(swhid_xml)
num_lines_swhid_txt = len(swhid_txt)
log_result(f"Number of SWHID: {num_lines_swhid_xml} (XML) | {num_lines_swhid_txt} (TXT)")

