from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from datetime import datetime

def save_table_to_csv(driver, xpath, filename):
    # Wait for the table to load
    time.sleep(2)
    
    # Get the table element
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    
    # Get all rows from the table
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    # Save to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write each row to the CSV
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells]
            if row_data:  # Only write if there's data
                csv_writer.writerow(row_data)
    
    print(f"\nDados salvos com sucesso em: {filename}")


def process_cnpj(driver,cnpj):
    # Navigate directly to the search page
    driver.get("https://www.vadu.com.br/vadu.dll/Consulta/Pesquisar")
    
    # Wait for the search page to load
    time.sleep(2)
    
    # Find and fill the search input with CNPJ using exact XPath
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div[2]/form/div/div[1]/input"))
    )
    search_input.clear()
    search_input.send_keys(cnpj)
    time.sleep(1)
    
    # Find and click the search button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-default"))
    )
    search_button.click()
    
    # Wait for search results to load
    time.sleep(10)  # Increased wait time as in main2.py
    
    # Click on the first link (Estadual)
    first_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendarios']"))
    )
    first_link.click()
    time.sleep(3)
    
    # Click on the second link
    second_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabInstanciasProcessosLendarios']"))
    )
    second_link.click()
    time.sleep(3)
    
    # Click on the third link
    third_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosEstaduais']"))
    )
    third_link.click()
    time.sleep(3)
    
    # Select the dropdown option for Estadual
    select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "tabelaProcessosEstaduais_length"))
    )
    select_element.click()
    time.sleep(1)
    
    # Select the 4th option
    option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@name='tabelaProcessosEstaduais_length']/option[4]"))
    )
    option.click()
    time.sleep(5)
    
    # Save first table (Estadual)
    save_table_to_csv(
        driver,
        "//table[@id='tabelaProcessosEstaduais']",
        "estadual.csv"
    )
    time.sleep(5)
    
    # Click on the fourth link (Trabalhista)
    fourth_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosInstanciaTrabalhista']"))
    )
    fourth_link.click()
    time.sleep(5)
    
    # Click on the fifth link
    fifth_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosTrabalhista']"))
    )
    fifth_link.click()
    time.sleep(5)
    
    # Select the dropdown option for Trabalhista
    select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "tabelaProcessosTrabalhistas_length"))
    )
    select_element.click()
    time.sleep(1)
    
    # Select the 4th option
    option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@name='tabelaProcessosTrabalhistas_length']/option[4]"))
    )
    option.click()
    time.sleep(5)
    
    # Save second table (Trabalhista)
    save_table_to_csv(
        driver,
        "//table[@id='tabelaProcessosTrabalhistas']",
        "trabalhista.csv"
    )
    time.sleep(5)
    
    # Click on the sixth link (Federal)
    sixth_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosInstanciaFederal']"))
    )
    sixth_link.click()
    time.sleep(5)
    
    # Click on the seventh link
    seventh_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosFederal']"))
    )
    seventh_link.click()
    time.sleep(5)
    
    # Select the dropdown option for Federal
    select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "tabelaProcessosFederais_length"))
    )
    select_element.click()
    time.sleep(1)
    
    # Select the 4th option
    option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@name='tabelaProcessosFederais_length']/option[4]"))
    )
    option.click()
    time.sleep(5)
    
    # Save third table (Federal)
    save_table_to_csv(
        driver,
        "//table[@id='tabelaProcessosFederais']",
        "federais.csv"
    )
    time.sleep(5)
    
    # Click on the eighth link (Eleitoral)
    eighth_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosInstanciaEleitoral']"))
    )
    eighth_link.click()
    time.sleep(5)
    
    # Click on the ninth link
    ninth_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosEleitoral']"))
    )
    ninth_link.click()
    time.sleep(5)
    
    # Select the dropdown option for Eleitoral
    select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "tabelaProcessosEleitorais_length"))
    )
    select_element.click()
    time.sleep(1)
    
    # Select the 4th option
    option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@name='tabelaProcessosEleitorais_length']/option[4]"))
    )
    option.click()
    time.sleep(5)
    
    # Save fourth table (Eleitoral)
    save_table_to_csv(
        driver,
        "//table[@id='tabelaProcessosEleitorais']",
        "eleitorais.csv"
    )
    time.sleep(5)
    
    # Click on the tenth link (Militar)
    tenth_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosInstanciaMilitar']"))
    )
    tenth_link.click()
    time.sleep(5)
    
    # Click on the eleventh link
    eleventh_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosMilitar']"))
    )
    eleventh_link.click()
    time.sleep(5)
    
    # Select the dropdown option for Militar
    select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "tabelaProcessosMilitares_length"))
    )
    select_element.click()
    time.sleep(1)
    
    # Select the 4th option
    option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@name='tabelaProcessosMilitares_length']/option[4]"))
    )
    option.click()
    time.sleep(5)
    
    # Save fifth table (Militar)
    save_table_to_csv(
        driver,
        "//table[@id='tabelaProcessosMilitares']",
        "militar.csv"
    )
    time.sleep(5)
        

    
def login_vadu():
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    options.add_argument('--log-level=3')  # Suppress console logs
    options.add_argument('--silent')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Disable logging
    
    # Initialize the Chrome WebDriver with updated setup
    service = Service()
    driver = webdriver.Chrome(options=options, service=service)
    
    try:
        
        # Navigate to the login page
        driver.get("https://www.vadu.com.br/vadu.dll/Autenticacao/Entrar/")
        
        # Wait for the page to load completely
        time.sleep(2)
        
        # Wait for the email field to be present and enter the email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Codigo"))
        )
        email_field.clear()  # Clear any existing text
        email_field.send_keys("pt@setepartners.com")
        time.sleep(1)  # Wait after entering email
        
        # Find and fill the password field
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Senha"))
        )
        password_field.clear()  # Clear any existing text
        password_field.send_keys("@vaduTorres2000")  # Updated password with @ symbol
        time.sleep(1)  # Wait after entering password
        
        # Find and click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.btn-block"))
        )
        login_button.click()
        
        # Wait for the first modal to appear and close it
        time.sleep(2)  # Wait for modal to appear
        first_modal_close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recusaAoInformativoSuporte"))
        )
        first_modal_close.click()
        
        # Wait for the second modal to appear and close it
        time.sleep(1)  # Wait for second modal to appear
        second_modal_close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recusaAoInformativoTelefones"))
        )
        second_modal_close.click()
        
        # Wait for the page to stabilize after closing modals
        time.sleep(2)
        cnpjs = ["17.713.930/0001-95","51.414.521/0001-26"]
        for cnpj in cnpjs:
            process_cnpj(driver,cnpj)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Browser will remain open for inspection...")
        time.sleep(300)  # Keep browser open for 5 minutes in case of error
    
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    login_vadu()