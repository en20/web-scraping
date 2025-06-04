from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

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
