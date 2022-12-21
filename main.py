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

# CONSTANT
WAIT_TIME = 10
DATA_PULL_WAIT_TIME = 1

def user_login(driver):
    print("> user_login() called...")
    
    email = "" #email goes here
    password = "" #password goes here

    # Find log in button
    try:
        log_in_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[7]/div/div/div/div[2]/div/div/p[2]/a"))
        ).click()
    except:
        print("> ERROR: Not able to find log in button")
        driver.quit()

    # Find log in with email button
    try:
        log_in_email_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[7]/div/div/div/div[2]/div/div/button[4]"))
        ).click()
    except:
        print("> ERROR: Not able to find 'Log in with Email' button")
        driver.quit()

    # Find user field
    try:
        user_field = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='email']"))
        ).send_keys(email)
        (driver.find_element(By.XPATH, "//*[@id='password']")).send_keys(password, Keys.RETURN)
    except:
        print("> ERROR: Not able to enter user details")
        driver.quit()
    
    print("> user_login() completed...")

def link_pull(driver):
    print("> link_pull() called...")

    # Get number of total listings
    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[7]/div/div/div/div[1]/div[1]/div[1]/div/span"))
        )
        total_listings = int(((element.text.split())[0]).replace(',', ''))
        print("> Total Listings Claimed: ", total_listings)
        WebDriverWait(driver,10)
    except:
        print("> ERROR: Timed out waiting for page to load")
        driver.close()
    
    # Keep scrolling until total listings = listings found, or listings found is close to total listings and page doesnt load any more
    SCROLL_PAUSE_TIME = 1
    last_cycle = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        elements = driver.find_elements(By.CLASS_NAME, "feed-item")
        loaded_listings = int(len(elements))
        if loaded_listings == total_listings:
            print("> Found all listings, stopping scroll")
            break
        if last_cycle == loaded_listings:
            print("> Almost found all listings, stopping scroll")
            break
        last_cycle = loaded_listings
    
    # Gather all href links to list and output into csv file
    elements = driver.find_elements(By.CLASS_NAME, "listing-item-link")
    links = []
    for element in elements:
        links.append(element.get_attribute('href'))
    with open('links.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])
    print("> links.csv file exported...")
    print("> Total Links Found: ", len(links))

    if total_listings != loaded_listings:
        print("> Total Listings != Loaded Listings...")
        if input("> Redo link_pull()? 'Y' or 'N: ") == 'Y':
            link_pull(driver)
        else:
            print("> link_pull() completed...")

def data_pull(driver):
    print("> data_pull() called...")

    # Open output file
    with open('data.csv', 'a', newline='') as outfile:
        fieldnames = ['designer', 'category', 'descript', 'size', 'color', 'condition', 'original_price', 'sold_price']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Open input file of links
        try:
            with open('links.csv', 'r', newline='') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    driver.get(row[0])
                    # Get designer info
                    try:
                        designer = WebDriverWait(driver, DATA_PULL_WAIT_TIME).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div[2]/nav/ol/li[1]/a"))
                        ).text
                    except:
                        print("> ERROR: could not get designer data")
                        designer = ''

                    # Get category info
                    try:
                        category = WebDriverWait(driver, DATA_PULL_WAIT_TIME).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div[2]/nav/ol/li[4]/a"))
                        ).text
                    except: 
                        print("> ERROR: could not get category data")
                        category = ''

                    # Get descript info
                    try:
                        descript = WebDriverWait(driver, DATA_PULL_WAIT_TIME).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div[2]/h1"))
                        ).text
                    except: 
                        print("> ERROR: could not get descript data")
                        category = ''

                    # Get size info
                    try:
                        size = WebDriverWait(driver, DATA_PULL_WAIT_TIME).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[2]/span"))
                        ).text
                    except: 
                        print("> ERROR: could not get size data")
                        size = ''

                    # Get color info
                    try:
                        color = WebDriverWait(driver, DATA_PULL_WAIT_TIME).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[3]/span"))
                        ).text
                    except: 
                        print("> ERROR: could not get color data")
                        color = ''

                    # Get condition info
                    try:
                        condition = WebDriverWait(driver, DATA_PULL_WAIT_TIME).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[4]/span"))
                        ).text
                    except: 
                        print("> ERROR: could not get condition data")
                        condition = ''
                    
                    # Get condition info
                    try:
                        original_price = WebDriverWait(driver, DATA_PULL_WAIT_TIME).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div[2]/div[1]/div[2]/div[1]/div[3]/span[2]"))
                        ).text
                    except: 
                        print("> ERROR: could not get original_price data")
                        original_price = ''

                    # Get condition info
                    try:
                        sold_price = WebDriverWait(driver, DATA_PULL_WAIT_TIME).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div[2]/div[1]/div[2]/div[1]/div[3]/span[1]"))
                        ).text
                    except: 
                        print("> ERROR: could not get sold_price data")
                        sold_price = ''
                    
                    # Write new row in output file
                    writer.writerow({'designer': designer, 'category': category, 'descript': descript, 'size': size, 'color': color, 'condition': condition, 'original_price': original_price, 'sold_price': sold_price})
        except:
            print("ERROR: links.csv could not be opened")

        print("> data_pull() completed...")

def main():
    url = "https://www.grailed.com/sold"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    
    #user_login(driver)
    #if input("> Pausing: Type 'Y' to continue: ") == 'Y':
        #print("> Resuming...")
        #link_pull(driver)
    data_pull(driver)

if __name__ == "__main__":
    main()