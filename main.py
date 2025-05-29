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
        
        # Navigate directly to the search page
        driver.get("https://www.vadu.com.br/vadu.dll/Consulta/Pesquisar")
        
        # Wait for the search page to load
        time.sleep(2)
        
        # Find and fill the search input with CNPJ using exact XPath
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div[2]/form/div/div[1]/input"))
        )
        search_input.clear()
        search_input.send_keys("17.713.930/0001-95")
        time.sleep(1)
        
        # Find and click the search button
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-default"))
        )
        search_button.click()
        
        # Wait for search results to load
        time.sleep(3)
        
        # Click on the first link
        first_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div[3]/div/ul/li[6]/a"))
        )
        first_link.click()
        
        # Wait for the page to load
        time.sleep(2)
        
        # Click on the second link
        second_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div[3]/div/div/div[10]/div/div/div/ul/li[2]/a"))
        )
        second_link.click()
        
        # Wait for the page to load
        time.sleep(2)
        
        # Click on the third link
        third_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div[3]/div/div/div[10]/div/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/ul/li[2]/a"))
        )
        third_link.click()
        
        # Wait for the page to load
        time.sleep(2)
        
        # Click on the select element
        select_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div[3]/div/div/div[10]/div/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/label/select"))
        )
        select_element.click()
        
        # Wait a moment
        time.sleep(1)
        
        # Click on the option
        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div[3]/div/div/div[10]/div/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/label/select/option[4]"))
        )
        option.click()
        
        # Save first table (Estadual)
        save_table_to_csv(
            driver,
            "/html/body/div[2]/div[3]/div/div[4]/div[3]/div/div/div[10]/div/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/table",
            "estadual.csv"
        )
        
        # Click on the fourth link
        fourth_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div[3]/div/div/div[10]/div/div/div/div[3]/div[2]/div/div[1]/ul/li[2]/a"))
        )
        fourth_link.click()
        
        # Wait for the page to load
        time.sleep(2)
        
        # Click on the select element
        select_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div[3]/div/div/div[10]/div/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/label/select"))
        )
        select_element.click()
        
        # Wait a moment
        time.sleep(1)
        
        # Click on the option
        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div[3]/div/div/div[10]/div/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/label/select/option[4]"))
        )
        option.click()
        
        # Save second table (Trabalhista)
        save_table_to_csv(
            driver,
            "/html/body/div[2]/div[3]/div/div[4]/div[3]/div/div/div[10]/div/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/table",
            "trabalhista.csv"
        )
        
        # Wait for a moment to see the result
        time.sleep(5)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    login_vadu()
