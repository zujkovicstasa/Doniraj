import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_service = Service('D:/chromedriver-win64/chromedriver.exe')

driver = webdriver.Chrome(service=chrome_service)

#driver_path = 'D:/chromedriver-win64/chromedriver.exe'


def login(driver, email, password):
    driver.get('http://localhost:8000/users/logovanje/')
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'btn-danger').click()



def pregledSopstvenogProfila():
    login(driver,'korisnik1@gmail.com', 'testnalog1')
    time.sleep(2)

    profile_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'profileDropdown'))
    )

    profile_icon.click()

    time.sleep(2)

    profile_page_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'inboxslika'))  #
    )
    assert profile_page_element is not None

    print("prosao test")


def pregledOrganizacija():
    time.sleep(2)
    organizacije_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Organizacije'))
    )
    organizacije_link.click()
    time.sleep(2)

    organizacije_page_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'kontaktirajDugme'))  
    )
    assert organizacije_page_element is not None

    print("Prosao test")


try:
    driver.get('http://localhost:8000/')
    

    print("Unesite broj testa")
    print("1. Pregled Sopstvenog Profila")
    print("2. Pregled Organizacija")
    x = int(input())
    if (x == 1):
        pregledSopstvenogProfila()
    elif x == 2:
        pregledOrganizacija()


    
finally:
    driver.quit()