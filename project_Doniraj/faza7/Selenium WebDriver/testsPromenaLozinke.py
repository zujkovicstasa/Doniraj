import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestChangePassword(unittest.TestCase):
    promenjena = 0;
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/users/logovanje")

        username_input = self.driver.find_element(By.NAME, 'email')
        username_input.send_keys("korisnik3@gmail.com") 

        password_input = self.driver.find_element(By.NAME, 'password')
        if(self.promenjena): password_input.send_keys("testnalog33")  
        else:  password_input.send_keys("testnalog3")

        time.sleep(2)

        login_button = self.driver.find_element(By.CLASS_NAME, 'logBtn')
        login_button.click()
        time.sleep(2)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'don'))
            )
        except Exception as e:
            self.fail("greška: {}".format(e))

        self.driver.get("http://127.0.0.1:8000/users/promenaLozinke")
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

    def test_change_password01_wrong_old(self):
        print("Test pogresna stara lozinka.")

        old_password_input = self.driver.find_element(By.NAME, 'old_password')
        old_password_input.send_keys("testnalog")

        new_password_input = self.driver.find_element(By.NAME, 'new_password1')
        new_password_input.send_keys("testnalog")

        confirm_new_password_input = self.driver.find_element(By.NAME, 'new_password2')
        confirm_new_password_input.send_keys("testnalog")

        change_button = self.driver.find_element(By.ID, 'prihvati')
        change_button.click()

        time.sleep(2)
        try:
            error_message = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'text-danger')))
            self.assertTrue("Your old password was entered incorrectly." in error_message.text, "error poruka nije ispravna")
        except AssertionError as e:
            print("Greška:", e)
        except Exception as e:
            print("Greška:", e)

    def test_change_password02_does_not_match(self):
        print("Test ne podudaraju se nova lozinka i njena potvrda.")

        old_password_input = self.driver.find_element(By.NAME, 'old_password')
        if(self.promenjena): old_password_input.send_keys("testnalog33")  
        else:  old_password_input.send_keys("testnalog3")

        new_password_input = self.driver.find_element(By.NAME, 'new_password1')
        new_password_input.send_keys("testnalog")

        confirm_new_password_input = self.driver.find_element(By.NAME, 'new_password2')
        confirm_new_password_input.send_keys("testnalo")

        change_button = self.driver.find_element(By.ID, 'prihvati')
        change_button.click()

        time.sleep(2)
        try:
            error_message = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'text-danger')))
            self.assertTrue("The two password fields didn’t match." in error_message.text, "error poruka neispravna")
        except AssertionError as e:
            print("Greška:", e)
        except Exception as e:
            print("Greška:", e)

    def test_change_password03_correct(self):
        print("Test uspesno")
        TestChangePassword.promenjena = 1;
        old_password_input = self.driver.find_element(By.NAME, 'old_password')
        old_password_input.send_keys("testnalog3")

        new_password_input = self.driver.find_element(By.NAME, 'new_password1')
        new_password_input.send_keys("testnalog33")

        confirm_new_password_input = self.driver.find_element(By.NAME, 'new_password2')
        confirm_new_password_input.send_keys("testnalog33")

        change_button = self.driver.find_element(By.ID, 'prihvati')
        change_button.click()

        time.sleep(2)
        try:
            success_message = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
            )
            self.assertTrue("Vaša lozinka je uspešno promenjena!" in success_message.text, "Tekst u success message nije ispravan.")
        except AssertionError as e:
            print("Greška:", e)
        except Exception as e:
            print("Greška:", e)


if __name__ == "__main__":
    unittest.main()
