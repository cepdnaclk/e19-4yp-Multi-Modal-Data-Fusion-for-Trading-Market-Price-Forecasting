from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Set up Selenium WebDriver (make sure to have the correct driver for your browser)
driver = webdriver.Chrome()  # Replace with your browser driver (ChromeDriver, GeckoDriver, etc.)

# Open the Investing.com Economic Calendar page
url = "https://www.investing.com/economic-calendar/cpi-733"
driver.get(url)

# Allow time for page to load (adjust as necessary)
time.sleep(10)

# Locate the table containing CPI data
rows = driver.find_elements(By.CSS_SELECTOR, 'table.calendar-table tr')

# Store the data
data = []
for row in rows:
    cols = row.find_elements(By.CSS_SELECTOR, 'td')
    if len(cols) >= 5:  # Ensure row has enough data
        release_date = cols[0].text.strip()
        time_ = cols[1].text.strip()
        actual = cols[2].text.strip()
        forecast = cols[3].text.strip()
        previous = cols[4].text.strip()

        # Append to data list
        data.append({
            "Release Date": release_date,
            "Time": time_,
            "Actual": actual,
            "Forecast": forecast,
            "Previous": previous
        })

# Close the browser
driver.quit()

# Save data to CSV
df = pd.DataFrame(data)
df.to_csv('cpi_data.csv', index=False)
print("Data saved to cpi_data.csv")
