import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
import pytest
import subprocess
import time

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test(setup):
    driver = setup

    driver.get("http://localhost:3000") 

    event_generator_process = subprocess.Popen(["python", "event_simulator.py"])

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "event-row"))
        )

        initial_event_count = len(driver.find_elements(By.CLASS_NAME, "event-row"))
        print(f"Initial event count: {initial_event_count}")

        incremented_event_count = initial_event_count
        for i in range(3):  
            time.sleep(5) 
            new_event_count = len(driver.find_elements(By.CLASS_NAME, "event-row"))
            
            # Step 3: Check if the event count has increased
            print(f"Event count after {5 * (i + 1)} seconds: {new_event_count}")
            assert new_event_count > incremented_event_count, f"Event list did not increase after {5 * (i + 1)} seconds"
            
            incremented_event_count = new_event_count


    finally:
        event_generator_process.terminate() 
        conn = sqlite3.connect('./python-api/app/alchem.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM events")
        conn.commit()
        conn.close()


