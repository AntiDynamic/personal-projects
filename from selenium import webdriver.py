from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

# === Setup ===
download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
base_url = "https://pradan1.issdc.gov.in"

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(options=options)
driver.get(base_url + "/al1/protected/browse.xhtml")

# === Login ===
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("Anti")
driver.find_element(By.ID, "password").send_keys("_ad2jdQty856H$f")
driver.find_element(By.ID, "kc-login").click()

# === Wait for date filter ===
WebDriverWait(driver, 20).until(EC.url_contains("browse.xhtml"))
print("🕒 Waiting 30 seconds for you to set date filters manually...")
time.sleep(30)

# === Set 100 rows per page ===
try:
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@class,'ui-paginator-rpp-options')]"))
    )
    Select(dropdown).select_by_visible_text("100")
    time.sleep(2)
except Exception as e:
    print("⚠️ Could not set rows per page")

# === Click download links ===
while True:
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//tbody[contains(@id,'data')]/tr"))
        )

        links = driver.find_elements(By.XPATH, "//td[@class='state_hover']/a[contains(@href, '.fits')]")
        print(f"🔗 Found {len(links)} .fits links")

        for i in range(len(links)):
            try:
                # refetch the link every time to avoid stale reference
                link = driver.find_elements(By.XPATH, "//td[@class='state_hover']/a[contains(@href, '.fits')]")[i]
                driver.execute_script("arguments[0].click();", link)
                print(f"⬇️ Triggered download for: {link.get_attribute('href')}")
                time.sleep(3)
            except Exception as e:
                print(f"⚠️ Could not click link: {e}")

        # Next page
        next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
        if "ui-state-disabled" in next_btn.get_attribute("class"):
            print("✅ Reached last page.")
            break
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2)

    except Exception as e:
        print(f"❌ Page error: {e}")
        break

print("🎉 Done downloading.")
