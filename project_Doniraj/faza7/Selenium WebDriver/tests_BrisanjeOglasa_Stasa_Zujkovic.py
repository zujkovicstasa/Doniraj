import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Specify the path to the ChromeDriver executable
chrome_service = Service('C:/chromedriver-win64/chromedriver.exe')

# Initialize WebDriver with the Service object
driver = webdriver.Chrome(service=chrome_service)

def login(driver, email, password):
    driver.get('http://localhost:8000/users/logovanje/')
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'btn-danger').click()

def test_delete_specific_oglas_as_user(ad_title):
    login(driver, 'korisnik1@gmail.com', 'testnalog1')  

    profile_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'profileDropdown'))
    )
    profile_icon.click()

    ad_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//h5[contains(text(), '{ad_title}')]/../..//button[@class='btn btn-light obrisi delete-button-oglas']"))
    )
    ad_element.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()


    WebDriverWait(driver, 10).until(EC.alert_is_present())
    print("Uspesan test.")


def test_delete_specific_oglas_as_admin(ad_title):
    login(driver, 'stasa@gmail.com', '1234')  

    driver.get('http://localhost:8000/') 
    ad_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//h5[contains(text(), '{ad_title}')]/ancestor::div[@name='kartica']//a"))
    )
    time.sleep(1)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", ad_element)
    driver.execute_script("arguments[0].click();", ad_element)

    profile_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[contains(@class, 'manjaProfilna')]"))
    )
    profile_element.click()

    ad_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//h5[contains(text(), '{ad_title}')]/../..//button[@class='btn btn-light obrisi delete-button-oglas']"))
    )
    ad_element.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    print("prosao test")

try:
    driver.get('http://localhost:8000/')
    ad_title_to_delete = "zelena majica"  
    print("Unesite broj testa")
    print("1. Brisanje sopstvenog oglasa")
    print("2. Brisanje oglasa kao administrator")
    x = int(input())
    if (x == 1):
        test_delete_specific_oglas_as_user(ad_title_to_delete)
    elif x ==2:
        test_delete_specific_oglas_as_admin(ad_title_to_delete)
finally:
    driver.quit()