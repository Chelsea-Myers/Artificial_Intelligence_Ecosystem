import requests
from bs4 import BeautifulSoup
import re
from PyPDF2 import PdfReader

def fetch_and_extract(url):
    """
    Fetches a webpage from the given URL, parses it with BeautifulSoup,
    extracts all <p> tags, joins their text with blank lines,
    writes the result to Selected_Document.txt (UTF-8), and returns the extracted text.
    """
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find the main content area (different sites use different classes)
            content_div = (soup.find('div', class_='mw-parser-output') or 
                          soup.find('article') or 
                          soup.find('div', class_='entry-content') or
                          soup.find('main') or
                          soup.body)
            
            if not content_div:
                print("Could not find content container. Extracting all paragraphs from page.")
                content_div = soup
            
            paragraphs = content_div.find_all('p')
            print(f"Found {len(paragraphs)} paragraphs")
            extracted_text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            if not extracted_text or len(extracted_text) < 100:
                print("Not enough paragraph text found. Extracting all visible text from content area.")
                # Remove script and style elements
                for script in content_div(["script", "style"]):
                    script.decompose()
                extracted_text = content_div.get_text()
                # Clean up whitespace
                lines = (line.strip() for line in extracted_text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                extracted_text = '\n'.join(chunk for chunk in chunks if chunk)

            with open('Selected_Document.txt', 'w', encoding='utf-8') as file:
                file.write(extracted_text)

            print(f"Page successfully retrieved and content saved to 'Selected_Document.txt'. Extracted {len(extracted_text)} characters.")
            return extracted_text
        else:
            print(f"Failed to retrieve the page. HTTP Status Code: {response.status_code}")
            return ""
    except requests.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return ""

def extract_text_from_pdf(pdf_path):
    """
    Opens a PDF file at the given path, extracts text from all pages,
    collapses extra whitespace, writes the combined text to Selected_Document.txt (UTF-8),
    and returns the full document text.
    """
    try:
        reader = PdfReader(pdf_path)
        extracted_text = ""
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n\n"
        
        # Collapse extra whitespace
        extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
        extracted_text = re.sub(r'\n\s*\n', '\n\n', extracted_text)
        
        with open('Selected_Document.txt', 'w', encoding='utf-8') as file:
            file.write(extracted_text)
        
        print(f"PDF successfully processed. Text extracted and saved to 'Selected_Document.txt'.")
        return extracted_text
        
    except FileNotFoundError:
        print(f"Error: PDF file not found at path: {pdf_path}")
        return ""
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")
        return ""

def main():
    # Choose extraction method:
    # Option 1: Web scraper
    # Using a working Wikipedia article since the original site blocks automated requests
    url = "https://en.wikipedia.org/wiki/Fungus"  
    fetch_and_extract(url)
    
    # Original fungi article URL (blocked by the site):
    # url = "https://sempervirens.org/news/fungi-of-the-forest/?gad_source=1&gad_campaignid=344052870&gbraid=0AAAAADnymdoD8G5xXygjnnJWqSALKPdkC&gclid=CjwKCAiA24XJBhBXEiwAXElO3-N55tzfpO5eTmxRde0TVuz-eXs6WdsO4HRSRW8ggmdaMquWCXVZGhoCgIwQAvD_BwE"
    
    # Option 2: PDF extractor
    # Uncomment the lines below and replace with your PDF path to use PDF extraction instead
    # pdf_path = "path/to/your/document.pdf"
    # extract_text_from_pdf(pdf_path)

if __name__ == '__main__':
    main()


