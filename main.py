from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from datetime import datetime

def save_table_to_csv(driver, xpath, table_type, filename):
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

def check_table_exists(driver, table_id):
    try:
        # Tenta encontrar a tabela
        table = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, table_id))
        )
        return True
    except:
        return False

def process_table(driver, table_id, table_type, filename):
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

def process_cnpj(driver, cnpj):
    try:
        # Create filename by removing special characters from CNPJ
        clean_cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        filename = f"{clean_cnpj}_dados.csv"
        
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
        
    except Exception as e:
        print(f"Erro ao processar CNPJ {cnpj}: {str(e)}")
        raise  # Re-lança a exceção para ser capturada pelo loop principal


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
        
        # Ler CNPJs do arquivo CSV
        cnpjs = []
        try:
            with open('cnpjs.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Pula o cabeçalho
                for row in csv_reader:
                    if row and row[0].strip():  # Verifica se a linha não está vazia
                        cnpjs.append(row[0].strip())
        except Exception as e:
            print(f"Erro ao ler arquivo cnpjs.csv: {str(e)}")
            return
        
        if not cnpjs:
            print("Nenhum CNPJ encontrado no arquivo cnpjs.csv")
            return
        
        print(f"Total de CNPJs encontrados: {len(cnpjs)}")
        
        # Lista para armazenar os CNPJs que falharam
        failed_cnpjs = []
        
        for cnpj in cnpjs:
            try:
                print(f"\nIniciando processamento do CNPJ: {cnpj}")
                process_cnpj(driver, cnpj)
                print(f"Processamento do CNPJ {cnpj} concluído com sucesso!")
            except Exception as e:
                error_msg = f"Erro ao processar CNPJ {cnpj}: {str(e)}"
                print(f"\n{'='*50}")
                print(error_msg)
                print(f"{'='*50}\n")
                failed_cnpjs.append((cnpj, str(e)))
                continue
        
        # Relatório final
        print("\n" + "="*50)
        print("RELATÓRIO DE PROCESSAMENTO")
        print("="*50)
        print(f"Total de CNPJs processados: {len(cnpjs)}")
        print(f"CNPJs processados com sucesso: {len(cnpjs) - len(failed_cnpjs)}")
        print(f"CNPJs com falha: {len(failed_cnpjs)}")
        
        if failed_cnpjs:
            print("\nDetalhes das falhas:")
            for cnpj, error in failed_cnpjs:
                print(f"\nCNPJ: {cnpj}")
                print(f"Erro: {error}")
        
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"Erro crítico durante a execução: {str(e)}")
        print("Browser will remain open for inspection...")
        time.sleep(300)  # Keep browser open for 5 minutes in case of error
    
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    login_vadu()