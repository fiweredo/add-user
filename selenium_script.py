from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def agregar_usuario_en_plataforma(username, password):
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        driver.get("https://tusitio.com/login")

        driver.find_element(By.NAME, "usuario").send_keys("TU_USUARIO_ADMIN")
        driver.find_element(By.NAME, "clave").send_keys("TU_PASSWORD_ADMIN")
        driver.find_element(By.ID, "btnLogin").click()
        time.sleep(2)

        driver.get("https://tusitio.com/admin/usuarios")

        driver.find_element(By.NAME, "nuevo_user").send_keys(username)
        driver.find_element(By.NAME, "nuevo_pass").send_keys(password)
        driver.find_element(By.ID, "btnCrear").click()
        time.sleep(1)

        driver.quit()
        return True
    except Exception as e:
        print("Error:", e)
        return False
