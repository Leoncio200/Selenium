import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_dynamic_page(url, search_term):
    # Configurar el servicio del controlador del navegador (Chrome)
    service = Service('C:/Users/Leoncio Pimentel/Documents/chromeDriver/chromedriver-win64/chromedriver-win64/chromedriver.exe')

    # Configurar las opciones del navegador para ignorar los errores de certificado
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Abrir la página web
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        # Encontrar el elemento que contiene las palabras "buscar" o "search" en el placeholder
        matching_input = None
        inputs = driver.find_elements(By.CSS_SELECTOR, 'input[placeholder]')
        for input_elem in inputs:
            placeholder_text = input_elem.get_attribute('placeholder')
            if re.search(r'\b(?:buscar|search)\b', placeholder_text, re.IGNORECASE):
                matching_input = input_elem
                break

        if matching_input:
            # Limpiar el campo de búsqueda y enviar el término de búsqueda
            matching_input.clear()
            matching_input.send_keys(search_term)
            matching_input.send_keys(Keys.RETURN)  # Presionar Enter para enviar la búsqueda

            # Esperar a que los resultados se carguen (ajusta según la página)
            time.sleep(5)  # Ejemplo de espera, ajusta según la velocidad de carga de la página

            # Esperar hasta que los resultados de búsqueda estén presentes
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot.s-result-list")))

            # Obtener los títulos de los resultados
            results = driver.find_elements(By.CSS_SELECTOR, "span.a-size-medium.a-color-base.a-text-normal")
            prices = driver.find_elements(By.CSS_SELECTOR, "span.a-price")

            # Crear listas para almacenar los datos
            product_titles = []
            product_prices = []

            for result in results:
                product_titles.append(result.text)
            
            for price in prices:
                product_prices.append(price.text)
            
            # Asegurarse de que ambas listas tengan la misma longitud
            min_length = min(len(product_titles), len(product_prices))
            product_titles = product_titles[:min_length]
            product_prices = product_prices[:min_length]

            # Crear un DataFrame con los resultados
            data = {'Title': product_titles, 'Price': product_prices}
            df = pd.DataFrame(data)

            # Guardar el DataFrame en un archivo de Excel
            df.to_excel('amazon_results.xlsx', index=False)

    finally:
        # Cerrar el navegador al finalizar
        driver.quit()

# Ejemplo de uso
url = input("Introduce la URL: ")
search_term = input("Introduce el término de búsqueda: ")
scrape_dynamic_page(url, search_term)