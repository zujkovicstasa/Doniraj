import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class TestChromeDriver(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_delete_account_as_admin(self):
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
            self.fail("Greška pri učitavanju stranice: {}".format(e))

        time.sleep(2)
        nalozi = self.driver.find_element(By.CLASS_NAME, 'nalozi')
        nalozi.click()
        delete_buttons = self.driver.find_elements(By.CLASS_NAME, 'delete-button')

        delete_button = delete_buttons[0]
        user_id = delete_button.get_attribute('data-user-id')
        print("korisnik ID:", user_id)
            
        delete_button.click()
        time.sleep(2)
            
        confirm_button = self.driver.switch_to.alert
        confirm_button.accept()
        time.sleep(2) 

        confirm_button = self.driver.switch_to.alert
        confirm_button.accept()
        time.sleep(2) 
            
        is_button_present = self.is_element_present(By.CSS_SELECTOR, f'[data-user-id="{user_id}"]')
        self.assertTrue(not is_button_present, f"Dugme 'Obriši Nalog' za korisnika sa ID {user_id} je i dalje prisutno.")


    def is_element_present(self, by, value):
        try:
            self.driver.find_element(by, value)
        except NoSuchElementException:
            return False
        return True

if __name__ == "__main__":
    unittest.main()
