from scrapper import Scrapper

if __name__ == "__main__":
    scraper = Scrapper('scrapper_final.json')
    scraper.setup_driver()
    scraper.ejecutar()
    scraper.close()