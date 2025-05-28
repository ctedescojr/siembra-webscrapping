from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

# Caminho para o ChromeDriver
service = Service("C:/DEV/B+P/Siembra/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# URL da loja de artigos elétricos
url = "https://www.dimensional.com.br/material-eletrico"
driver.get(url)

# Timeout máximo para carregamento dos elementos
wait = WebDriverWait(driver, 20)

# Scroll para carregar todos os produtos em pequenos blocos
produtos_anteriores = 0
tentativas_sem_novos = 0
scroll_height = 500
pagina = 1

while True:
    # Loop interno para rolar a página até carregar todos os produtos visíveis
    while tentativas_sem_novos < 3:
        driver.execute_script(f"window.scrollBy(0, {scroll_height});")
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        produtos_atual = len(
            soup.find_all("span", class_="vtex-product-summary-2-x-productBrand")
        )

        if produtos_atual == produtos_anteriores:
            tentativas_sem_novos += 1
        else:
            tentativas_sem_novos = 0

        produtos_anteriores = produtos_atual
        print(f"Produtos carregados até agora: {produtos_atual}", flush=True)

    # Verifica se o botão "Mostrar mais" está presente
    try:
        print("Achando botão 'Mostrar mais'...", flush=True)
        botao_mostrar_mais = driver.find_element(
            By.XPATH, "//div[contains(text(), 'Mostrar mais')]"
        )
        botao_mostrar_mais.click()
        print(
            f"[Clique] Página {pagina} carregada, carregando mais produtos...",
            flush=True,
        )
        pagina += 1
        tentativas_sem_novos = 0  # Reseta para o próximo loop interno
        time.sleep(5)
    except NoSuchElementException:
        print("Nenhum botão 'Mostrar mais' encontrado. Finalizando.", flush=True)
        break


print(f"Total de páginas carregadas: {pagina}", flush=True)

# Coleta do HTML final
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Extração dos produtos e preços
produtos = [
    item.text.strip()
    for item in soup.find_all("span", class_="vtex-product-summary-2-x-productBrand")
]
precos = []
for price in soup.find_all("span", class_="vtex-product-price-1-x-spotPrice"):
    valor = price.find("span", class_="vtex-product-price-1-x-currencyContainer")
    if valor:
        precos.append(valor.text.strip())

# Criação de DataFrame para organização
dados = pd.DataFrame({"Produto": produtos, "Preço": precos})

# Exibindo os dados coletados
print(dados)

# Gerar nome de arquivo com a data atual
data_hoje = datetime.today().strftime("%Y-%m-%d")
nome_arquivo = f"dimensional_{data_hoje}.xlsx"

# Salvando em Excel
dados.to_excel(nome_arquivo, index=False)
print(f"Dados salvos em {nome_arquivo}", flush=True)
