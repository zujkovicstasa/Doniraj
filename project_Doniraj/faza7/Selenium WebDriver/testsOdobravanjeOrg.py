import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestConfirmOrg(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/users/logovanje")

        username_input = self.driver.find_element(By.NAME, 'email')
        username_input.send_keys("sm210320d@student.etf.bg.ac.rs") 

        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.send_keys("marija123")

        time.sleep(2)

        login_button = self.driver.find_element(By.CLASS_NAME, 'logBtn')
        login_button.click()
        time.sleep(2)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'nalozi'))
            )
        except Exception as e:
            self.fail("greška: {}".format(e))

        self.driver.get("http://127.0.0.1:8000/users/zahtevi")
        time.sleep(2)

    def test01_prihvati_org(self):
        zahtevi = self.driver.find_elements(By.CSS_SELECTOR, ".list-group-item")

        prvi_zahtev = zahtevi[0]
        prvi_zahtev_text = prvi_zahtev.text
        prvi_zahtev.click()
        time.sleep(2)

        approve_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-success")))
        approve_button.click()
  
        time.sleep(2)

        odobreni_zahtevi = self.driver.find_elements(By.CSS_SELECTOR, ".list-group-item")
        odobreni_zahtevi_text = [zahtev.text for zahtev in odobreni_zahtevi]
        self.assertNotIn("Ime Organizacije: {{ zahtev.organization.name }}", odobreni_zahtevi_text)


    def tearDown(self):
        self.driver.quit()

    def test02ali_odbij_org(self):
        zahtevi = self.driver.find_elements(By.CSS_SELECTOR, ".list-group-item")

        prvi_zahtev = zahtevi[0]
        prvi_zahtev_text = prvi_zahtev.text
        prvi_zahtev.click()
        time.sleep(2)

        decline_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-danger")))
        decline_button.click()
  
        time.sleep(2)

        odobreni_zahtevi = self.driver.find_elements(By.CSS_SELECTOR, ".list-group-item")
        odobreni_zahtevi_text = [zahtev.text for zahtev in odobreni_zahtevi]
        self.assertNotIn("Ime Organizacije: {{ zahtev.organization.name }}", odobreni_zahtevi_text)


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
