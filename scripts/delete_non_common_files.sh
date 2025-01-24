#!/bin/bash

# Define directories
pdf_dir="/data/pdf"
xml_dir="/data/xml"
txt_dir="/data/txt"

# Get the list of filenames (without paths) in each directory
pdf_files=$(ls "$pdf_dir")
xml_files=$(ls "$xml_dir")
txt_files=$(ls "$txt_dir")

# Loop through PDF files and delete them if they are not in all three directories
for pdf_file in $pdf_files; do
    if [[ ! -f "$xml_dir/$pdf_file" || ! -f "$txt_dir/$pdf_file" ]]; then
        # If the file is not found in either the XML or TXT directory, delete from all directories
        rm -f "$pdf_dir/$pdf_file"
    fi
done

# Loop through XML files and delete them if they are not in all three directories
for xml_file in $xml_files; do
    if [[ ! -f "$pdf_dir/$xml_file" || ! -f "$txt_dir/$xml_file" ]]; then
        # If the file is not found in either the PDF or TXT directory, delete from all directories
        rm -f "$xml_dir/$xml_file"
    fi
done

# Loop through TXT files and delete them if they are not in all three directories
for txt_file in $txt_files; do
    if [[ ! -f "$pdf_dir/$txt_file" || ! -f "$xml_dir/$txt_file" ]]; then
        # If the file is not found in either the PDF or XML directory, delete from all directories
        rm -f "$txt_dir/$txt_file"
    fi
done

# Print the number of remaining files in each directory
echo "Remaining files in PDF directory: $(ls -1q "$pdf_dir" | wc -l)"
echo "Remaining files in XML directory: $(ls -1q "$xml_dir" | wc -l)"
echo "Remaining files in TXT directory: $(ls -1q "$txt_dir" | wc -l)"
