import requests
from bs4 import BeautifulSoup
import csv
import re
import os
import json
from urllib.parse import urljoin
import time

class JasmineFatSecretScraper:
    def __init__(self):
        self.base_url = "https://www.fatsecret.com.br"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.output_file = "dados/jasmine_nutricional.csv"
        self.urls_file = "dados/jasmine_urls.json"
        
    def get_page_content(self, url):
        """Faz a requisição HTTP e retorna o conteúdo da página"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Erro ao acessar {url}: {e}")
            return None
    
    def extract_product_name(self, soup):
        """Extrai o nome do produto combinando marca e nome"""
        try:
            # Busca a marca (Bob's)
            brand_element = soup.find('h2', class_='manufacturer')
            brand = ""
            if brand_element and brand_element.find('a'):
                brand = brand_element.find('a').get_text(strip=True)
            
            # Busca o nome do produto
            product_name_element = soup.find('h1', style='text-transform:none')
            product_name = ""
            if product_name_element:
                product_name = product_name_element.get_text(strip=True)
            
            # Combina marca + nome do produto
            full_name = f"{brand} {product_name}".strip()
            return full_name
        except Exception as e:
            print(f"Erro ao extrair nome do produto: {e}")
            return "Nome não encontrado"
    
    def extract_category(self, soup):
        """Extrai a categoria do produto (pode ser expandido no futuro)"""
        return "Produto Jasmine Alimentos"
    
    def extract_portion(self, soup):
        """Extrai a porção do produto"""
        try:
            serving_size_element = soup.find('div', class_='serving_size_value')
            if serving_size_element:
                portion_text = serving_size_element.get_text(strip=True)
                # Extrai números da string (ex: "1 porção (700 ml)" -> 700)
                numbers = re.findall(r'\d+', portion_text)
                if numbers:
                    return int(numbers[-1])  # Pega o último número (700)
            return 0
        except Exception as e:
            print(f"Erro ao extrair porção: {e}")
            return 0
    
    def extract_nutritional_data(self, soup):
        """Extrai todos os dados nutricionais da tabela"""
        nutritional_data = {
            'calorias': 0,
            'carboidratos': 0.0,
            'proteinas': 0.0,
            'gorduras_totais': 0.0,
            'gorduras_saturadas': 0.0,
            'fibras': 0.0,
            'acucares': 0.0,
            'sodio': 0
        }
        
        try:
            nutrition_table = soup.find('div', class_='nutrition_facts')
            if not nutrition_table:
                print("Tabela nutricional não encontrada")
                return nutritional_data
            
            # Busca por todos os nutrientes
            nutrients = nutrition_table.find_all('div', class_='nutrient')
            
            for i in range(len(nutrients)):
                nutrient_text = nutrients[i].get_text(strip=True)
                
                # Energia (kcal) - procura em múltiplas linhas
                if nutrient_text == "Energia":
                    # Procura nas próximas linhas por kcal
                    for j in range(1, 4):  # Verifica até 3 linhas à frente
                        if i + j < len(nutrients):
                            kcal_text = nutrients[i + j].get_text(strip=True)
                            if "kcal" in kcal_text:
                                kcal_value = re.findall(r'\d+', kcal_text)
                                if kcal_value:
                                    nutritional_data['calorias'] = int(kcal_value[0])
                                    break
                
                # Carboidratos
                elif nutrient_text == "Carboidratos":
                    if i + 1 < len(nutrients):
                        carbs_text = nutrients[i + 1].get_text(strip=True)
                        carbs_value = re.findall(r'[\d,]+', carbs_text)
                        if carbs_value:
                            nutritional_data['carboidratos'] = float(carbs_value[0].replace(',', '.'))
                
                # Açúcar (subnutriente de carboidratos)
                elif nutrient_text == "Açúcar":
                    if i + 1 < len(nutrients):
                        sugar_text = nutrients[i + 1].get_text(strip=True)
                        sugar_value = re.findall(r'[\d,]+', sugar_text)
                        if sugar_value:
                            nutritional_data['acucares'] = float(sugar_value[0].replace(',', '.'))
                
                # Proteínas
                elif nutrient_text == "Proteínas":
                    if i + 1 < len(nutrients):
                        protein_text = nutrients[i + 1].get_text(strip=True)
                        protein_value = re.findall(r'[\d,]+', protein_text)
                        if protein_value:
                            nutritional_data['proteinas'] = float(protein_value[0].replace(',', '.'))
                
                # Gorduras
                elif nutrient_text == "Gorduras":
                    if i + 1 < len(nutrients):
                        fat_text = nutrients[i + 1].get_text(strip=True)
                        fat_value = re.findall(r'[\d,]+', fat_text)
                        if fat_value:
                            nutritional_data['gorduras_totais'] = float(fat_value[0].replace(',', '.'))
                
                # Gordura Saturada
                elif nutrient_text == "Gordura Saturada":
                    if i + 1 < len(nutrients):
                        sat_fat_text = nutrients[i + 1].get_text(strip=True)
                        sat_fat_value = re.findall(r'[\d,]+', sat_fat_text)
                        if sat_fat_value:
                            nutritional_data['gorduras_saturadas'] = float(sat_fat_value[0].replace(',', '.'))
                
                # Fibras
                elif nutrient_text == "Fibras":
                    if i + 1 < len(nutrients):
                        fiber_text = nutrients[i + 1].get_text(strip=True)
                        fiber_value = re.findall(r'[\d,]+', fiber_text)
                        if fiber_value:
                            nutritional_data['fibras'] = float(fiber_value[0].replace(',', '.'))
                
                # Sódio
                elif nutrient_text == "Sódio":
                    if i + 1 < len(nutrients):
                        sodium_text = nutrients[i + 1].get_text(strip=True)
                        sodium_value = re.findall(r'\d+', sodium_text)
                        if sodium_value:
                            nutritional_data['sodio'] = int(sodium_value[0])
        
        except Exception as e:
            print(f"Erro ao extrair dados nutricionais: {e}")
        
        return nutritional_data
    
    def scrape_product(self, url):
        """Faz o scraping de um produto específico"""
        print(f"Fazendo scraping de: {url}")
        
        # Obtém o conteúdo da página
        content = self.get_page_content(url)
        if not content:
            return None
        
        # Parse do HTML
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extrai os dados
        product_data = {
            'nome_produto': self.extract_product_name(soup),
            'url': url,
            'categoria': self.extract_category(soup),
            'porcao': self.extract_portion(soup)
        }
        
        # Extrai dados nutricionais
        nutritional_data = self.extract_nutritional_data(soup)
        product_data.update(nutritional_data)
        
        return product_data
    
    def save_to_csv(self, data_list):
        """Salva os dados em um arquivo CSV"""
        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Define as colunas
        columns = [
            'NOME_PRODUTO', 'URL', 'CATEGORIA', 'PORCAO', 
            'CALORIAS (kcal)', 'CARBOIDRATOS (g)', 'PROTEINAS (g)', 
            'GORDURAS_TOTAIS (g)', 'GORDURAS_SATURADAS (g)', 
            'FIBRAS (g)', 'ACUCARES (g)', 'SODIO (mg)'
        ]
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            
            for data in data_list:
                row = {
                    'NOME_PRODUTO': data['nome_produto'],
                    'URL': data['url'],
                    'CATEGORIA': data['categoria'],
                    'PORCAO': data['porcao'],
                    'CALORIAS (kcal)': data['calorias'],
                    'CARBOIDRATOS (g)': data['carboidratos'],
                    'PROTEINAS (g)': data['proteinas'],
                    'GORDURAS_TOTAIS (g)': data['gorduras_totais'],
                    'GORDURAS_SATURADAS (g)': data['gorduras_saturadas'],
                    'FIBRAS (g)': data['fibras'],
                    'ACUCARES (g)': data['acucares'],
                    'SODIO (mg)': data['sodio']
                }
                writer.writerow(row)
        
        print(f"Dados salvos em: {self.output_file}")
    
    def load_urls_from_json(self):
        """Carrega URLs do arquivo JSON"""
        try:
            if not os.path.exists(self.urls_file):
                print(f"❌ Arquivo de URLs não encontrado: {self.urls_file}")
                print("💡 Execute primeiro o url_collector.py para coletar as URLs")
                return []
            
            with open(self.urls_file, 'r', encoding='utf-8') as jsonfile:
                urls = json.load(jsonfile)
            
            print(f"📋 Carregadas {len(urls)} URLs do arquivo JSON")
            return urls
        except Exception as e:
            print(f"❌ Erro ao carregar URLs: {e}")
            return []

def main():
    """Função principal para testar o scraper Jasmine Alimentos"""
    scraper = JasmineFatSecretScraper()
    
    # Carrega URLs do arquivo JSON
    url_lista = scraper.load_urls_from_json()
    
    if not url_lista:
        print("❌ Nenhuma URL foi carregada. Encerrando...")
        return
    
    all_products_data = []
    
    print(f"🚀 Iniciando scraping de {len(url_lista)} produtos da Jasmine Alimentos...")
    
    for i, url in enumerate(url_lista, 1):
        print(f"\n--- Processando produto {i}/{len(url_lista)} ---")
        
        # Faz o scraping do produto
        product_data = scraper.scrape_product(url)
        
        if product_data:
            all_products_data.append(product_data)
            print(f"✓ Produto processado com sucesso: {product_data['nome_produto']}")
        else:
            print(f"✗ Erro ao processar produto: {url}")
        
        # Pausa entre requisições para não sobrecarregar o servidor
        time.sleep(2)
    
    if all_products_data:
        # Salva todos os dados no CSV
        scraper.save_to_csv(all_products_data)
        print(f"\n🎉 Scraping concluído! {len(all_products_data)} produtos processados.")
        print(f"📁 Dados salvos em: {scraper.output_file}")
        
        # Mostra resumo dos dados coletados
        print("\n📊 Resumo dos dados coletados:")
        for product in all_products_data:
            print(f"  • {product['nome_produto']}: {product['calorias']} kcal")
    else:
        print("❌ Nenhum produto foi processado com sucesso.")

if __name__ == "__main__":
    main() 