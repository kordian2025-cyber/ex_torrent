# save_cookies_auto.py
import time
import random
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

class ExTorrentyCookieSaver:
    url = "https://ex-torrenty.org"
    login_url = url + "/login.php"

    # LOGIN I HASŁO W KODZIE
    username = "xxx"
    password = "xxx"

    def __init__(self, headless=False, driver_path=None, cookiefile="cookies.json", wait_timeout=15):
        self.headless = headless
        self.driver_path = driver_path
        self.cookiefile = cookiefile
        self.wait_timeout = wait_timeout
        self.driver = None

    def _make_driver(self):
        opts = Options()
        if self.headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        try:
            if self.driver_path:
                service = Service(self.driver_path)
                driver = webdriver.Chrome(service=service, options=opts)
            else:
                driver = webdriver.Chrome(options=opts)
            driver.set_page_load_timeout(60)
            return driver
        except WebDriverException as e:
            raise RuntimeError("Błąd uruchamiania Chromedrivera: " + str(e))

    def save_cookies_to_file(self):
        cookies = self.driver.get_cookies()
        cleaned = []
        for c in cookies:
            ck = {
                "name": c.get("name"),
                "value": c.get("value"),
                "domain": c.get("domain"),
                "path": c.get("path"),
                "expires": int(c["expiry"]) if "expiry" in c and c["expiry"] is not None else None,
                "httpOnly": c.get("httpOnly", False),
                "secure": c.get("secure", False),
            }
            if "sameSite" in c:
                ck["sameSite"] = c.get("sameSite")
            cleaned.append(ck)
        with open(self.cookiefile, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=2, ensure_ascii=False)
        print(f"[ok] Zapisano {len(cleaned)} ciasteczek do: {self.cookiefile}")

    def perform_login_and_save(self):
        self.driver = self._make_driver()
        try:
            self.driver.get(self.login_url)
            time.sleep(random.uniform(1.0, 2.0))

            # znajdź pola login/hasło
            user_el = self.driver.find_element(By.NAME, "username")
            pass_el = self.driver.find_element(By.NAME, "password")

            # imitacja pisania
            for ch in self.username:
                user_el.send_keys(ch)
                time.sleep(random.uniform(0.05, 0.15))
            time.sleep(random.uniform(0.2, 0.5))
            for ch in self.password:
                pass_el.send_keys(ch)
                time.sleep(random.uniform(0.05, 0.15))

            # kliknij przycisk submit lub naciśnij ENTER
            try:
                submit_btn = self.driver.find_element(By.ID, "submitButton")
                submit_btn.click()
            except:
                pass_el.send_keys("\n")

            # poczekaj na przeładowanie strony
            WebDriverWait(self.driver, self.wait_timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(random.uniform(1.0, 2.0))

            # zapis ciasteczek
            self.save_cookies_to_file()

        finally:
            try:
                self.driver.quit()
            except:
                pass


if __name__ == "__main__":
    saver = ExTorrentyCookieSaver(headless=False, cookiefile="cookies.json")
    saver.perform_login_and_save()
