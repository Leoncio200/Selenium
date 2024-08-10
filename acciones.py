import re
import json
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import xlsxwriter
import os

# Métodos definidos
def seleccionar(driver, wait, action, name_page):
    try:
        time.sleep(7)
        select_element = driver.find_element(by=getattr(By, action['element']['by'].upper()), value=action['element']['value'])
        select = Select(select_element)
        select.select_by_visible_text(action['element']['text-select'])

    except Exception as e:
        print(f"Error en seleccionar: {e}")

def click(driver, wait, action, name_page):
    try:
        time.sleep(5)
        driver.find_element(by=getattr(By, action['element']['by'].upper()), value=action['element']['value']).click()

    except Exception as e:
        print(f"Error en click: {e}")

def send_keys(driver, wait, action, name_page):
    try:
        time.sleep(5)
        # Clear field to empty it from any previous data
        driver.find_element(by=getattr(By, action['element']['by'].upper()), value=action['element']['value']).clear()

        # Enter Text
        driver.find_element(by=getattr(By, action['element']['by'].upper()), value=action['element']['value']).send_keys(action['element']['search-term'])
    
    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as e:
        print(f"Error en send_keys: {e}")

def exctract_info(driver, wait, action, name_page):
    try:
        time.sleep(10)
        titles = driver.find_elements(by=getattr(By, action['element']['tittle']['by'].upper()), value=action['element']['tittle']['value'])
        prices = driver.find_elements(by=getattr(By, action['element']['price']['by'].upper()), value=action['element']['price']['value'])

        # Preparar listas para almacenar los textos de los elementos
        title_texts = [title.text for title in titles]
        price_texts = [price.text for price in prices]

        if len(title_texts) != len(price_texts):
            max_length = max(len(title_texts), len(price_texts))
            title_texts += [None] * (max_length - len(title_texts))
            price_texts += [None] * (max_length - len(price_texts))

        # Guardar los datos en un archivo Excel
        save_info_to_excel(title_texts, price_texts, name_page)

    except Exception as e:
        print(f"Error en exctract_info: {e}")

def extract_table(driver, wait, action, name_page):
    try:
        time.sleep(10)
        table = driver.find_element(by=getattr(By, action['element']['by'].upper()), value=action['element']['value'])
        header = table.find_element(by=getattr(By, action['element']['header']['by'].upper()), value=action['element']['header']['value'])
        headers = header.find_elements(By.TAG_NAME, "th")
        
        header_texts = [header.text for header in headers]
        #print(" | ".join(header_texts))  # Imprimir encabezados
        
        cuerpo = table.find_element(By.TAG_NAME, "tbody")
        elementos = cuerpo.find_elements(By.TAG_NAME, "tr")

        # Preparar lista para almacenar los datos de la tabla
        table_data = []

        for elemento in elementos:
            cells = elemento.find_elements(By.TAG_NAME, "td")
            cell_texts = [cell.text for cell in cells]
            #print(" | ".join(cell_texts))
            
            # Agregar la fila extraída a la lista de datos
            table_data.append(cell_texts)

        save_table_to_excel(header_texts, table_data, action['element']['name_arch'])

    except Exception as e:
        print(f"Error en extract_table: {e}")

def save_table_to_excel(headers, data, name_arch):
    # Crear un DataFrame con los encabezados y datos extraídos
    df = pd.DataFrame(data, columns=headers)
    
    # Nombre del archivo Excel basado en name_page
    excel_filename = f"{name_arch}.xlsx"
    
    # Guardar el DataFrame en un archivo Excel con formato
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Tabla")

        # Formatear el archivo Excel (por ejemplo, ajustar el ancho de las columnas)
        workbook = writer.book
        worksheet = writer.sheets["Tabla"]
        
        for i, column in enumerate(df.columns):
            column_length = max(df[column].astype(str).map(len).max(), len(column)) + 2
            worksheet.set_column(i, i, column_length)
    
    print(f"Tabla guardada en {excel_filename}")

def save_info_to_excel(titles, prices, name_page):
    # Crear un DataFrame con los títulos y precios extraídos
    df = pd.DataFrame({
        'Título': titles,
        'Precio': prices
    })
    
    # Nombre del archivo Excel basado en name_page
    excel_filename = f"{name_page}.xlsx"
    
    # Guardar el DataFrame en un archivo Excel con formato
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Información")

        # Formatear el archivo Excel (por ejemplo, ajustar el ancho de las columnas)
        workbook = writer.book
        worksheet = writer.sheets["Información"]
        
        for i, column in enumerate(df.columns):
            column_length = max(df[column].astype(str).map(len).max(), len(column)) + 2
            worksheet.set_column(i, i, column_length)
    
    print(f"Información guardada en {excel_filename}")

