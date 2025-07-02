from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

# --- Config ---
download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
start_from_page = 15

# --- Chrome setup ---
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
driver.get("https://pradan1.issdc.gov.in/al1/protected/browse.xhtml?id=swis")

# --- Login ---
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("Anti")
driver.find_element(By.ID, "password").send_keys("_ad2jdQty856H$f")
driver.find_element(By.ID, "kc-login").click()

WebDriverWait(driver, 20).until(EC.url_contains("browse.xhtml"))
time.sleep(2)

# --- Set Rows Per Page to 10 ---
dropdown = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//select[contains(@class,'ui-paginator-rpp-options')]"))
)
Select(dropdown).select_by_visible_text("100")
time.sleep(2)

# --- Skip to page 15 ---
for _ in range(start_from_page - 1):
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next Page']"))
        )
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2)
    except Exception as e:
        print(f"❌ Couldn't reach page {start_from_page}: {e}")
        driver.quit()
        exit()

# --- Start processing pages ---
while True:
    try:
        # ✅ Wait for table to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table[contains(@class,'ui-datatable')]//a"))
        )

        # ✅ Get only _L2_ links
        l2_links = driver.find_elements(By.XPATH, "//a[contains(@href, '_L2_') and contains(@href, '.cdf')]")
        print(f"Found {len(l2_links)} L2 links")

        for link in l2_links:
            href = link.get_attribute("href")
            if href:
                print(f"Downloading: {href}")
                driver.execute_script("window.open(arguments[0]);", href)
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(5)  # Let download start
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        # ✅ Try to go to next page
        next_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Next Page']"))
        )
        if "ui-state-disabled" in next_btn.get_attribute("class"):
            print("✅ Reached last page.")
            break

        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2)

    except Exception as e:
        print(f"⚠️ Error while processing page: {e}")
        break

input("✅ All pages processed. Press Enter to exit...")
driver.quit()
