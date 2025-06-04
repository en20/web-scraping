from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import csv

def login_vadu():
    """
    Logs into the VADU system and returns a configured Chrome WebDriver instance.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
    """
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
        password_field.send_keys("@vaduChaib2000")  # Updated password with @ symbol
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
        
        return driver
        
    except Exception as e:
        print(f"Erro crítico durante o login: {str(e)}")
        if driver:
            driver.quit()
        raise

def check_table_exists(driver, table_id):
    """
    Checks if a table exists in the current page.
    
    Args:
        driver: WebDriver instance
        table_id: ID of the table to check
        
    Returns:
        bool: True if table exists, False otherwise
    """
    try:
        table = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, table_id))
        )
        return True
    except:
        return False

def process_table(driver, table_id, table_type, filename):
    """
    Processes a table and saves its data to a CSV file.
    
    Args:
        driver: WebDriver instance
        table_id: ID of the table to process
        table_type: Type of the table (e.g., "Estadual", "Federal")
        filename: Name of the CSV file to save the data
    """
    try:
        # Verifica se a tabela existe
        if not check_table_exists(driver, table_id):
            print(f"Tabela {table_type} não encontrada ou sem registros")
            return
        
        # Select the dropdown option
        select_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, f"{table_id}_length"))
        )
        select_element.click()
        time.sleep(3)
        
        # Select the 4th option (100 entries)
        option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//select[@name='{table_id}_length']/option[4]"))
        )
        option.click()
        time.sleep(5)
        
        # Save table
        save_table_to_csv(
            driver,
            f"//table[@id='{table_id}']",
            table_type,
            filename
        )
        time.sleep(3)
    except Exception as e:
        print(f"Erro ao processar tabela {table_type}: {str(e)}")

def save_table_to_csv(driver, xpath, table_type, filename):
    """
    Saves table data to a CSV file.
    
    Args:
        driver: WebDriver instance
        xpath: XPath of the table
        table_type: Type of the table
        filename: Name of the CSV file to save the data
    """
    try:
        # Wait for the table to load with increased timeout
        time.sleep(5)
        
        # Get the table element with explicit wait
        try:
            table = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            print(f"Nenhum dado encontrado para a tabela {table_type}")
            return
        
        # Get all rows from the table
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        if not rows:
            print(f"Nenhum dado encontrado para a tabela {table_type}")
            return
        
        # Save to CSV
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write each row to the CSV with the table type
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text for cell in cells]
                if row_data:  # Only write if there's data
                    csv_writer.writerow([table_type] + row_data)
        
        print(f"\nDados da tabela {table_type} salvos com sucesso em: {filename}")
    except Exception as e:
        print(f"Erro ao salvar tabela {table_type}: {str(e)}")

def process_all_tables(driver, filename):
    """
    Processes all tables in the current page.
    
    Args:
        driver: WebDriver instance
        filename: Name of the CSV file to save the data
    """
    # Processar tabela Estadual
    try:
        first_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendarios']"))
        )
        first_link.click()
        time.sleep(3)
        
        second_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabInstanciasProcessosLendarios']"))
        )
        second_link.click()
        time.sleep(3)
        
        third_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosEstaduais']"))
        )
        third_link.click()
        time.sleep(3)
        
        process_table(driver, "tabelaProcessosEstaduais", "Estadual", filename)
    except Exception as e:
        print(f"Erro ao acessar aba Estadual: {str(e)}")
    
    # Processar tabela Trabalhista
    try:
        fourth_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosInstanciaTrabalhista']"))
        )
        fourth_link.click()
        time.sleep(3)
        
        fifth_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosTrabalhista']"))
        )
        fifth_link.click()
        time.sleep(3)
        
        process_table(driver, "tabelaProcessosTrabalhistas", "Trabalhista", filename)
    except Exception as e:
        print(f"Erro ao acessar aba Trabalhista: {str(e)}")
    
    # Processar tabela Federal
    try:
        sixth_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosInstanciaFederal']"))
        )
        sixth_link.click()
        time.sleep(3)
        
        seventh_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosFederal']"))
        )
        seventh_link.click()
        time.sleep(3)
        
        process_table(driver, "tabelaProcessosFederais", "Federal", filename)
    except Exception as e:
        print(f"Erro ao acessar aba Federal: {str(e)}")
    
    # Processar tabela Eleitoral
    try:
        eighth_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosInstanciaEleitoral']"))
        )
        eighth_link.click()
        time.sleep(3)
        
        ninth_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosEleitoral']"))
        )
        ninth_link.click()
        time.sleep(3)
        
        process_table(driver, "tabelaProcessosEleitorais", "Eleitoral", filename)
    except Exception as e:
        print(f"Erro ao acessar aba Eleitoral: {str(e)}")
    
    # Processar tabela Militar
    try:
        tenth_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosInstanciaMilitar']"))
        )
        tenth_link.click()
        time.sleep(3)
        
        eleventh_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabProcessosLendariosMilitar']"))
        )
        eleventh_link.click()
        time.sleep(3)
        
        process_table(driver, "tabelaProcessosMilitares", "Militar", filename)
    except Exception as e:
        print(f"Erro ao acessar aba Militar: {str(e)}")
