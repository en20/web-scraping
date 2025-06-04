from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
from utils import process_all_tables

def process_cnpj(driver, cnpj):
    """
    Process a single CNPJ search and save results to CSV.
    
    Args:
        driver: WebDriver instance
        cnpj: CNPJ number to search
    """
    try:
        # Create filename by removing special characters from CNPJ
        clean_cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        filename = f"output/{clean_cnpj}_dados.csv"
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Create a new CSV file with headers
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Tipo', 'CNPJ', 'Processo', 'Data', 'Valor', 'Status'])
        
        # Navigate directly to the search page
        driver.get("https://www.vadu.com.br/vadu.dll/Consulta/Pesquisar")
        
        # Wait for the search page to load
        time.sleep(3)
        
        # Find and fill the search input with CNPJ using exact XPath
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div[2]/form/div/div[1]/input"))
        )
        search_input.clear()
        search_input.send_keys(cnpj)
        time.sleep(2)
        
        # Find and click the search button
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-default"))
        )
        search_button.click()
        
        # Wait for search results to load
        time.sleep(10)
        
        # Verificar se há mensagem de "Nenhum registro encontrado"
        try:
            no_records = driver.find_element(By.XPATH, "//div[contains(text(), 'Nenhum registro encontrado')]")
            if no_records.is_displayed():
                print(f"Nenhum registro encontrado para o CNPJ {cnpj}")
                return
        except:
            pass  # Se não encontrar a mensagem, continua normalmente
        
        # Process all tables
        process_all_tables(driver, filename)
        
    except Exception as e:
        print(f"Erro ao processar CNPJ {cnpj}: {str(e)}")
        raise 