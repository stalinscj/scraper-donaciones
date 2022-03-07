import os
import copy
import shutil
from scraper import Scraper
from selenium import webdriver


def test_setup_download_folder():
    scraper = Scraper('', '', '', '')

    scraper.setup_download_folder()

    assert os.path.isdir(scraper.download_path)

    assert len(os.listdir(scraper.download_path)) == 0


def test_setup_driver():
    scraper = Scraper('', '', '', '')
    scraper.setup_download_folder()

    scraper.setup_driver()

    assert isinstance(scraper.driver, webdriver.Chrome)


# End to End test
def tes_download_report():
    scraper = Scraper(
        content_type='Dataset',
        category='Economía y Finanzas',
        format='csv',
        report_name='donaciones',
        quiet=True
    )
    scraper.setup_download_folder()
    scraper.setup_driver()

    scraper.download_report()

    filenames = [x for x in os.listdir(scraper.download_path) if x.endswith('.zip')]

    assert len(filenames) != 0


def test_extract_file():
    scraper = Scraper('', '', '', '', True)
    scraper.setup_download_folder()

    os.makedirs(scraper.download_path, exist_ok=True)
    source = os.path.join(
        scraper.download_path.replace('downloads', 'samples'),
        'pcm_donaciones_sample.zip'
    )
    destiny = source.replace('samples', 'downloads')
    shutil.copyfile(source, destiny)

    filename = scraper.extract_file()

    assert os.path.exists(filename)

    os.remove(filename)


def test_finish_driver(mocker):
    scraper = Scraper('', '', '', '')
    scraper.setup_download_folder()
    scraper.setup_driver()

    driver = copy.copy(scraper.driver)
    stop_client_mock = mocker.patch.object(scraper.driver, 'stop_client')
    close_mock = mocker.patch.object(scraper.driver, 'close')

    scraper.finish_driver()

    stop_client_mock.assert_called_once()
    close_mock.assert_called_once()

    driver.stop_client()
    driver.close()
