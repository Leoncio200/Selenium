import re
import json
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def scrape_dynamic_page(url, search_term, selectors):
    service = Service('C:/Users/Leoncio Pimentel/Documents/chromeDriver/chromedriver-win64/chromedriver-win64/chromedriver.exe')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)  # Aumentar el tiempo de espera

        matching_input = None
        time.sleep(5)  # Mejorar esto con WebDriverWait en producción
        inputs = driver.find_elements(By.CSS_SELECTOR, 'input[placeholder]')
        for input_elem in inputs:
            placeholder_text = input_elem.get_attribute('placeholder')
            if re.search(r'\b(?:buscar|search)\b', placeholder_text, re.IGNORECASE):
                matching_input = input_elem
                break

        if matching_input:
            time.sleep(5)  # Mejorar esto con WebDriverWait en producción
            matching_input.clear()
            matching_input.send_keys(search_term)
            matching_input.send_keys(Keys.RETURN)

            # Esperar a que la página cargue
            titles = driver.find_elements(By.CSS_SELECTOR, selectors['title'])
            prices = driver.find_elements(By.CSS_SELECTOR, selectors['price'])

            product_titles = [title.text for title in titles]
            product_prices = [price.text for price in prices]
            data = {'Título': product_titles, 'Precio': product_prices}
            df = pd.DataFrame(data)

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            file_name = f'productos_amazon_{timestamp}.xlsx'
            df.to_excel(file_name, index=False)

            return df

    except Exception as e:
        print(f"Error al extraer datos: {e}")
    finally:
        driver.quit()

def compare_prices(json_input):
    with open(json_input, 'r') as file:
        data = json.load(file)
    
    comparison_df = pd.DataFrame(columns=['Product', 'Website', 'Title', 'Price'])

    for item in data['products']:
        product = item['name']
        for entry in item['urls']:
            url = entry['url']
            selectors = entry['selectors']
            df = scrape_dynamic_page(url, product, selectors)
            if df is not None:
                for _, row in df.iterrows():
                    comparison_df = comparison_df.append({
                        'Product': product,
                        'Website': url,
                        'Title': row['Título'],
                        'Price': row['Precio']
                    }, ignore_index=True)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    comparison_df.to_excel(f'comparacion_precios_{timestamp}.xlsx', index=False)
            
# Ejemplo de uso
json_input = "C:/Users/Leoncio Pimentel/Bull/selenium/busqueda_precios.json"
compare_prices(json_input)
