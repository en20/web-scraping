from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

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
        raise

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
