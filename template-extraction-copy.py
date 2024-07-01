import os
from bs4 import BeautifulSoup

def clean_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Iterate through all <td> elements
    for td in soup.find_all('td'):
        # Check if the <td> contains a <b> tag
        if td.find('b'):
            for content in td.contents:
                if not content.name and content.strip():  # Check if content is not a tag and has text
                    content.extract()  # Remove non-tag (text) content
        else:
            td.string = ""  # If no <b> tag, clear the text content

    # Do not alter the <div class="footer">; keep it intact

    return str(soup)

def process_html_file(input_filepath, output_filepath):
    with open(input_filepath, 'r', encoding='utf-8') as file:
        html_content = file.read()
        
        # Clean the HTML content
        cleaned_html_content = clean_html_content(html_content)
        
        # Save the cleaned HTML template to the output file
        with open(output_filepath, 'w', encoding='utf-8') as output_file:
            output_file.write(cleaned_html_content)
        print(f"Processed and saved: {output_filepath}")

def process_html_directory(input_directory, output_directory):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # List all files in the input directory
    for filename in os.listdir(input_directory):
        input_filepath = os.path.join(input_directory, filename)
        
        # Ensure it's a file (not a directory) and ends with .html
        if os.path.isfile(input_filepath) and filename.endswith('.html'):
            output_filepath = os.path.join(output_directory, filename)
            
            # Process and save the cleaned HTML file
            process_html_file(input_filepath, output_filepath)

# Paths for input and output directories
input_directory = 'demofile'
output_directory = 'empty_templates'

# Process all HTML files in the input directory and save cleaned templates in the output directory
process_html_directory(input_directory, output_directory)

print(f"All templates saved to {output_directory}")









