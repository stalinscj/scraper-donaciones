import os
import time
import shutil
import argparse
from zipfile import ZipFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper(object):
    """
    Scraper object that is composed of the content_type, category, format and report_name
    To initialize:
    :param content_type: Content type to select
    :param category: Category name to select
    :param format: Format name to select
    :param report_name: Report name to search
    :param quiet: Do not output any message

    USAGE:
        >>> scraper = Scraper(content_type='Dataset', category='Economía y Finanzas', format='csv', report_name='donaciones')
        >>> scraper.run()
    """
    def __init__(
        self,
        content_type: str,
        category: str,
        format: str,
        report_name: str,
        quiet: bool = False
    ):
        self.content_type = content_type
        self.category     = category
        self.format       = format
        self.report_name  = report_name
        self.quiet        = quiet

        self.url = 'https://www.datosabiertos.gob.pe'

    def setup_download_folder(self):
        self.download_path = os.path.join(os.getcwd(), 'downloads')

        if os.path.exists(self.download_path):
            shutil.rmtree(self.download_path)

        os.mkdir(self.download_path)

    def setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': self.download_path}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)

        self.driver = driver

    def wait_for_download(self, timeout=10):
        for i in range(timeout):
            filenames = os.listdir(self.download_path)

            if (filenames and not filenames[0].endswith('.crdownload')) or i == timeout-1:
                break

            time.sleep(1)

    def download_report(self):
        if not self.quiet:
            print('Descargando archivo...')

        self.driver.get(self.url)

        wait = WebDriverWait(self.driver, 10)

        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, f'{self.content_type} ('))).click()
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, f'{self.category} ('))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h2[text()="Formato"]'))).click()
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, f'{self.format} ('))).click()

        self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Buscar"]').send_keys(self.report_name)
        self.driver.find_element(By.CSS_SELECTOR, 'input[value="Consultar"]').click()

        article_name = 'Donaciones COVID-19 - [Ministerio de Economía y Finanzas - MEF]'
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, article_name))).click()

        xpath_download = '//p[text()="Data - Donaciones Covid-19"]/following-sibling::span/a[contains(text(),"Descargar")]'
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_download))).click()

        self.wait_for_download()

    def extract_file(self) -> str:
        filenames_zip = [x for x in os.listdir(self.download_path) if x.endswith('.zip')]

        if not filenames_zip:
            return ''

        filename_zip = os.path.join(self.download_path, filenames_zip[0])

        with ZipFile(filename_zip) as zip:
            filenames_csv = [x for x in zip.namelist() if x.endswith('.csv')]
            zip.extractall()
            zip.close()

        if not self.quiet:
            if filenames_csv:
                print(f'{filenames_csv[0]} extraído con éxito.')
            else:
                print('No se ha podido extraer el archivo')

        return filenames_csv[0] if filenames_csv else ''

    def finish_driver(self):
        self.driver.stop_client()
        self.driver.close()


    def run(self):
        self.setup_download_folder()

        self.setup_driver()

        self.download_report()

        self.extract_file()

    def __del__(self):
        if hasattr(self, 'driver'):
            self.finish_driver()

        if hasattr(self, 'download_path'):
            if os.path.exists(self.download_path):
                shutil.rmtree(self.download_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Busca y descarga un archivo')
    parser.add_argument('-ct', '--content_type', help='Tipo de Contenido')
    parser.add_argument('-c', '--category', help='Categoría')
    parser.add_argument('-f', '--format', help='Formato')
    parser.add_argument('-r', '--report_name', help='Nombre del reporte')
    parser.add_argument('-q', '--quiet', action='store_true', required=False)

    args = parser.parse_args()

    scraper = Scraper(
        content_type=args.content_type,
        category=args.category,
        format=args.format,
        report_name=args.report_name,
        quiet=args.quiet
    )

    scraper.run()
