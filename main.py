# Core Selenium Packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Libraries for locating elements and using common keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Libraries for waiting
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CSV Library
import csv
import time

def link_pull(driver):
    '''
    1. Get the total number of listings
    '''
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[7]/div/div/div/div[1]/div[1]/div[1]/div/span"))
        )
        total_listings = int(((element.text.split())[0]).replace(',', ''))
        print(total_listings)
        WebDriverWait(driver,10)
    except:
        print("ERROR: Timed out waiting for page to load")
        driver.close()
    
    '''
    2. Keep scrolling down until total elements with class "feed-item" == total_listings
    '''
    SCROLL_PAUSE_TIME = 1
    last_cycle = 0
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        elements = driver.find_elements(By.CLASS_NAME, "feed-item")
        loaded_listings = len(elements)
        if loaded_listings == total_listings:
            break
        if last_cycle == loaded_listings:
            break
        last_cycle = loaded_listings
    
    '''
    3. Gather all href links to list and output into csv file
    '''
    elements = driver.find_elements(By.CLASS_NAME, "listing-item-link")
    links = []
    for element in elements:
        links.append(element.get_attribute('href'))
    with open('links.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])

def data_pull(driver):
    items = []
    fieldnames = ['designer', 'descript', 'size', 'color', 'condition', 'original_price']
    
    '''
    1. Open csv file with all links, loop through and gather relevant data into list of dicts
    '''
    with open('links.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            driver.get(row[0])

            # Get designer info
            designer = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[1]"))
            ).text

            # Get descript info
            descript = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div[2]/h1"))
            ).text

            # Get size info
            size = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[2]/span"))
            ).text

            # Get color info
            color = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[3]/span"))
            ).text

            # Get condition info
            condition = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[4]/span"))
            ).text

            # Get condition info
            original_price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div[3]/span"))
            ).text
            items.append({'designer': designer, 'descript': descript, 'size': size, 'color': color, 'condition': condition, 'original_price': original_price})
    
    '''
    2. Open another csv file and write data into file
    '''
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)

def main():
    url = "https://www.grailed.com/sold"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    
    time.sleep(200)
    link_pull(driver)
    data_pull(driver)

if __name__ == "__main__":
    main()