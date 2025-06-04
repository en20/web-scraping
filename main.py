import time
import csv
import os
from utils.utils import login_vadu
from cpf_scraper.scraper import process_cpf
from cnpj_scraper.scraper import process_cnpj


def main():
    try:
        driver = login_vadu()
        
        # Ask user for search type
        while True:
            search_type = input("Digite 1 para pesquisa de CPF ou 2 para pesquisa de CNPJ: ").strip()
            if search_type in ['1', '2']:
                break
            print("Opção inválida. Por favor, digite 1 para CPF ou 2 para CNPJ.")
        
        # Read the appropriate file based on search type
        if search_type == '1':
            filename = 'input/cpfs.csv'
            search_type_name = 'CPF'
            process_func = process_cpf
        else:
            filename = 'input/cnpjs.csv'
            search_type_name = 'CNPJ'
            process_func = process_cnpj
        
        # Ensure input directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Read the file
        items = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header
                for row in csv_reader:
                    if row and row[0].strip():  # Check if row is not empty
                        items.append(row[0].strip())
        except Exception as e:
            print(f"Erro ao ler arquivo {filename}: {str(e)}")
            return
        
        if not items:
            print(f"Nenhum {search_type_name} encontrado no arquivo {filename}")
            return
        
        print(f"Total de {search_type_name}s encontrados: {len(items)}")
        
        # List to store failed items
        failed_items = []
        
        # Process each item
        for item in items:
            try:
                print(f"\nIniciando processamento do {search_type_name}: {item}")
                process_func(driver, item)
                print(f"Processamento do {search_type_name} {item} concluído com sucesso!")
            except Exception as e:
                error_msg = f"Erro ao processar {search_type_name} {item}: {str(e)}"
                print(f"\n{'='*50}")
                print(error_msg)
                print(f"{'='*50}\n")
                failed_items.append((item, str(e)))
                continue
        
        # Final report
        print("\n" + "="*50)
        print("RELATÓRIO DE PROCESSAMENTO")
        print("="*50)
        print(f"Total de {search_type_name}s processados: {len(items)}")
        print(f"{search_type_name}s processados com sucesso: {len(items) - len(failed_items)}")
        print(f"{search_type_name}s com falha: {len(failed_items)}")
        
        if failed_items:
            print("\nDetalhes das falhas:")
            for item, error in failed_items:
                print(f"\n{search_type_name}: {item}")
                print(f"Erro: {error}")
        
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"Erro crítico durante a execução: {str(e)}")
        print("Browser will remain open for inspection...")
        time.sleep(300)  # Keep browser open for 5 minutes in case of error
    
    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()