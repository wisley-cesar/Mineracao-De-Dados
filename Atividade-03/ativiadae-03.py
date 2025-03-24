import requests
from bs4 import BeautifulSoup
import csv

# URL da página de celulares no Zoom
url = 'https://www.zoom.com.br/celular'

# Cabeçalhos para simular um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fazendo a requisição para a página
response = requests.get(url, headers=headers)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    page_content = response.text
else:
    print(f'Erro ao acessar a página: {response.status_code}')
    exit()

# Parseando o HTML com BeautifulSoup
soup = BeautifulSoup(page_content, 'html.parser')

# Lista para armazenar os produtos
products = []

# Encontrar os containers de produtos (inspecione a página para ajustar os seletores)
product_containers = soup.find_all('div', class_='product-card')

# Extração dos nomes e preços
for container in product_containers:
    name_tag = container.find('h2', class_='product-name')  # Ajuste a classe conforme necessário
    price_tag = container.find('span', class_='product-price')  # Ajuste a classe conforme necessário

    if name_tag and price_tag:
        product_name = name_tag.text.strip()
        product_price = price_tag.text.strip()
        products.append((product_name, product_price))

    if len(products) >= 5:  # Pegando apenas os primeiros 5 produtos
        break

# Exibir os produtos no terminal
for idx, (name, price) in enumerate(products, start=1):
    print(f'{idx}. {name} - {price}')

# Salvar os produtos em um arquivo CSV
csv_filename = 'smartphones_zoom.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Nome do Produto', 'Preço'])
    writer.writerows(products)

print(f'Dados salvos em {csv_filename}')
