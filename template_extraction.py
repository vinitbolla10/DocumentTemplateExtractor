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

def process_html_file(html_content):
    
        # Clean the HTML content
        cleaned_html_content = clean_html_content(html_content)
        output_file_path = 'empty_templates/test.html'
        # Save the cleaned HTML template to the output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(cleaned_html_content)
        print(f"Processed and saved: {output_file_path}")
        return output_file_path
        

