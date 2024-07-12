import fitz  # PyMuPDF
import re
import sys
import argparse
def extract_installation_section(type, pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    end = re.compile(r'\bEBX® application start\b')
    pass1 = False
    exit = False


    # Define a regex pattern to search for the Tomcat installation section
    if type == "tomcat":
        c = 5
        pattern = re.compile(r'Chapter 5', re.IGNORECASE)

    if type == "jboss":
        c = 3
        pattern = re.compile(r'\bChapter 3', re.IGNORECASE)
    
    if type == "websphere":
        c = 4
        pattern = re.compile(r'\bChapter 4', re.IGNORECASE)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        if pattern.search(text):
            toc_keyword_pattern = re.compile(r'This chapter contains the following topics:', re.IGNORECASE)
            toc_section_pattern = re.compile(r'\d+\.\s*(?!.*\.jar)[a-zA-Z\s]+', re.MULTILINE)   # Pattern for sections like "1. Overview", excluding ".jar"
            if toc_keyword_pattern.search(text):
                print(f"{type} Installation chapter found on page {page_num + 1}:\n")
            
                # Extract the table of contents section
                toc_start = toc_keyword_pattern.search(text).end()
                toc_text = text[toc_start:]

                toc_lines = toc_text.split('\n')
                filtered_toc_lines = [line for line in toc_lines if '4.jar' not in line]
                toc_text = '\n'.join(filtered_toc_lines)
            
                # Find and count the sections within the extracted TOC text
                toc_sections = toc_section_pattern.findall(toc_text)
                num_sections = len(toc_sections)
                print(f"Number of sections in the table of contents: {num_sections}")

        
            while not exit:
                page = pdf_document.load_page(page_num)
                text = page.get_text()
                print(text)
                if end.search(text):
                    if not pass1:
                        pass1 = True
                    else:
                        exit = True
                page_num += 1
            break
    else:
        print(f"{type} Installation section not found in the PDF.")

# Example usage


def main():
    parser = argparse.ArgumentParser(description='Extract specified section from a PDF.')
    parser.add_argument('section_type', type=str, help='Type of section to extract. Types include \'tomcat\', \'jboss\', or \'websphere\'.')
    parser.add_argument('file_path', type=str, help='Path to the PDF file')
    
    args = parser.parse_args()
    extract_installation_section(args.section_type, args.file_path)

if __name__ == "__main__":
    main()

    # if len(sys.argv) != 3:
    #     print("Usage: python scraper-script.py <type> <path_to_pdf>. Types include \'tomcat\', \'jboss\', or \'websphere\'.")
    #     sys.exit(1)
    # type = sys.argv[1]
    # pdf_path = sys.argv[2]
    # extract_installation_section(type, pdf_path)
