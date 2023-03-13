from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

options = Options()
options.add_argument("--headless")
links_url = 'https://lambic.ru/sitemap'
adresses_url = 'https://lambic.ru/address'


def confirm_age(browser: webdriver.Chrome) -> None:
    """Подтверждение возраста."""
    try:
        browser.find_element(By.CLASS_NAME, 'age-confirm-btn').click()
    except NoSuchElementException:
        pass


with webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
) as browser:
    
    browser.get(links_url)
    browser.implicitly_wait(7)
    confirm_age(browser=browser)

    links = browser.find_elements(By.CSS_SELECTOR, 'a')
    with open('links.txt', 'w', encoding='utf-8') as file:
        for link in links:
            clean_link = link.get_attribute("href")
            if '/beer/' in clean_link:
                file.write(f'{clean_link}\n')

    browser.get(adresses_url)
    browser.implicitly_wait(7)
    confirm_age(browser=browser)

    adresses_info = browser.find_elements(By.XPATH, "//*[contains(@class,'AddressCard_cardInfo')]")

    with open('adresses.txt', 'w', encoding='utf-8') as file:
        for card in adresses_info:
            try:
                adresses = card.find_elements(By.XPATH, ".//*[contains(@class,'AddressCard_title')]")
                for adress in adresses:
                    file.write(f'Адрес:{adress.text}\n')
                try:
                    subway_stantions = card.find_elements(By.XPATH, ".//*[contains(@class,'AddressCard_metroName')]")
                except AttributeError:
                    continue
                for subway in subway_stantions:
                    file.write(f'    Метро:{subway.text}\n')
            except AttributeError:
                continue
        
