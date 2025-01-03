import os
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import time
from urllib.parse import urlsplit

#add name of the novel or book between the '
name = input("\n >Enter the name of the novel or book: ")
#add the base URL of the website you are scraping. It should look like this 'https://website-name-here.com'
time.sleep(1)

#add the link of the first page you want to start scraping from. It should look like this 'https://website-name-here.com/novel-name/chapter-1.html'
time.sleep(1)
current_url = input("\n >Enter the link of the first page you want to start scraping from.It should look like this 'https://website-name-here.com/novel-name/chapter-1.html': ")

split_url = urlsplit(current_url)

base_url = f'{split_url.scheme}://{split_url.netloc}'

all_content = ''

#add number of web pages you want scraped
time.sleep(1)
num_pages = int(input("\n >Enter the number of web pages you want scraped: "))

session = requests.Session()

def scrape_page(url):
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    paragraphs = soup.find_all('p')
    return '\n\n'.join([p.get_text(strip=True) for p in paragraphs])

for i in range(num_pages):
    print(f'\n > Scraping page {i + 1}...')

    all_content += scrape_page(current_url) + f'\n\n --- {current_url.split("/")[-1].replace(".html", "")} --- \n\n'

    r = session.get(current_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #This is where mistakes can happen depending on the website structure. Some websites have different classes or ids for the 'Next Chapter' button. If the prexisting code doesnt work, you can right clock on the button to inspect element and change the script. If it still doesn't work, feel free to reach out and I'll see what I can do.
    next_page = soup.find('a', {'id': 'next_chap'})

    if next_page and 'href' in next_page.attrs:
        next_url = next_page['href']
        current_url = base_url.rstrip('/') + next_url
    else:
        print("\n > No 'Next' button found. Exiting.")
        break

#This saves it directly to your download folder. You should have python enabled to PATH for this to work (I think).

downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
output_filename = os.path.join(downloads_folder, f' {name}.txt')

with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(all_content)

print(f'\n\n > Webscraped content saved to {output_filename}.')

pdf = FPDF()

pdf.add_page()

pdf.set_left_margin(10)
pdf.set_right_margin(10)
pdf.set_top_margin(10)

                                    #you might need to fix the path found here
pdf.add_font('DejaVu', '', r"C:\Users\AppData\Local\Programs\Python\Python313\Lib\site-packages\fpdf\fonts\DejaVuSans.ttf", uni=True)

pdf.set_font('DejaVu', '', 16)

pdf.cell(200, 10, txt=f"{name}", ln=1, align='C')

pdf.set_font('DejaVu', '', 12)

if pdf.get_y() > 250:  
    pdf.add_page()

with open(output_filename, "r", encoding="utf-8") as f:

    for x in f:
        available_width = 190 
        
        pdf.multi_cell(available_width, 5, txt=x, align='L')

pdf_output_path = os.path.join(downloads_folder, f'{name}.pdf')
pdf.output(pdf_output_path)

print(f'\n\n > PDF saved to {pdf_output_path}.')
