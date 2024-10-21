import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_service = Service('C:/chromedriver-win64/chromedriver.exe')

driver = webdriver.Chrome(service=chrome_service)

def login(driver, email, password):
    driver.get('http://localhost:8000/users/logovanje/')
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'btn-danger').click()

def contact_user(ad_title):
    time.sleep(2)
    login(driver, 'korisnik1@gmail.com', 'testnalog1')  

    driver.get('http://localhost:8000/') 
    ad_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//h5[contains(text(), '{ad_title}')]/ancestor::div[@name='kartica']//a"))
    )
    time.sleep(1)
    driver.execute_script("arguments[0].click();", ad_element)
    time.sleep(1)
    kontaktiraj_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='proizvod']//a[@class='link-secondary']"))
    )
    kontaktiraj_button.click()
    time.sleep(2)
    
    chat_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "chat_message_form"))
    )

    chat_input_field = chat_form.find_element(By.CLASS_NAME, "form-control")
    chat_input_field.send_keys("CAOOO")
    chat_input_field.submit()

    time.sleep(2)

    print("Uspesan test.")


def inbox():
    time.sleep(2)
    login(driver, 'korisnik1@gmail.com', 'testnalog1')  

    driver.get('http://localhost:8000/') 
    profile_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'profileDropdown'))
    )
    profile_icon.click()
    time.sleep(1)
    inbox_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'slovaVeca')]"))
    )
    inbox_link.click()
    time.sleep(1)
    current_url = driver.current_url

    assert 'http://localhost:8000/inbox/' == current_url
    time.sleep(2)
    print('test prosao')

try:
    driver.get('http://localhost:8000/')
    ad_title = "Muske teksas pantalone"  

    print("Unesite broj testa")
    print("1. Kontaktiranje korisnika preko oglasa")
    print("2. Inbox")
    x = int(input())
    if (x == 1):
        contact_user(ad_title)
    elif x ==2:
        inbox()


    
finally:
    driver.quit()