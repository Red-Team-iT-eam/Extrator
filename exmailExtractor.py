from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import os

 
def print_banner():
    banner = """
     ______    ____    ____   ____  ____
 ___|\     \  |    |  |    | |    ||    |
|     \     \ |    |  |    | |    ||    |
|     ,_____/||    | /    // |    ||    |
|     \--'\_|/|    |/ _ _//  |    ||    |  ____
|     /___/|  |    |\    \'  |    ||    | |    |
|     \____|\ |    | \    \  |    ||    | |    |
|____ '     /||____|  \____\ |____||____|/____/|
|    /_____/ ||    |   |    ||    ||    |     ||
|____|     | /|____|   |____||____||____|_____|/
  \( |_____|/   \(       )/    \(    \(    )/
   '    )/       '       '      '     '    '
        '
    """
    print(banner)

 
def google_search(domain):
    query = f'intext:"@{domain}"'
    url = "https://www.google.com/search?q=" + query

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    input("Resolva o CAPTCHA no navegador e pressione Enter para continuar...")

    time.sleep(5)

    visited_links = set()
    page_counter = 1

    while True:
        time.sleep(5)

        with open(f'index{page_counter}.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

        print(f"Página {page_counter} salva como index{page_counter}.html")


        try:
            next_button = driver.find_element(By.XPATH, f'//a[@aria-label="Page {page_counter + 1}"]')
            next_button.click()
            page_counter += 1
            time.sleep(3)
        except Exception as e:
            print(f"Erro ao tentar acessar a próxima página ou não há mais páginas: {e}")
            break

    driver.quit()

 
def extract_emails_from_files():
    html_files = [f for f in os.listdir() if f.endswith(".html")]

    emails = set()


    for html_file in html_files:
        print(f"Buscando e-mails em {html_file}")
        with open(html_file, 'r', encoding='utf-8') as f:
            page_content = f.read()
            emails.update(extract_emails(page_content))

    return emails

 
def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

 
def main():
    print_banner()   
    domain = input("Digite o domínio (exemplo.com.br): ")
    google_search(domain)

    emails = extract_emails_from_files()

    if emails:
        print("\nE-mails encontrados:")
        for email in emails:
            print(email)
    else:
        print("Nenhum e-mail encontrado.")

if __name__ == "__main__":
    main()