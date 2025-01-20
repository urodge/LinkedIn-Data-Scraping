from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

# Function to initialize the WebDriver
def init_driver():
    chrome_options = webdriver.ChromeOptions()
    # Add your custom options here if necessary
    
    # Set the ChromeDriver path using Service
    service = Service(ChromeDriverManager().install())
    
    # Pass the service and options to the Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Then call the init_driver function
driver = init_driver()
# Function to login to LinkedIn
def linkedin_login(driver, username, password):
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    
    # Locate and fill the login form
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    
    time.sleep(3)  # Wait for login to complete

# Function to scrape LinkedIn profiles
def scrape_profile(driver, profile_url):
    driver.get(profile_url)
    time.sleep(3)

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extract Job Title
    job_title = soup.find('h2', {'class': 'mt1'}).text.strip() if soup.find('h2', {'class': 'mt1'}) else 'N/A'
    
    # Extract Current Company & Industry
    company = soup.find('span', {'class': 'text-body-medium'}).text.strip() if soup.find('span', {'class': 'text-body-medium'}) else 'N/A'
    industry = soup.find('div', {'class': 'text-body-small'}).text.strip() if soup.find('div', {'class': 'text-body-small'}) else 'N/A'
    
    return job_title, company, industry

# Function to save data to CSV
def save_to_csv(data, filename='linkedin_profiles.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Job Title', 'Company', 'Industry'])  # Write header
        writer.writerows(data)

# Main function to drive the script
def main():
    username = 'Uddhav Rodge'  # Provide your LinkedIn username
    password = '@Urodge22'  # Provide your LinkedIn password
    
    # List of LinkedIn profile URLs (example URLs of IIT graduates)
    profile_urls = [
        'https://www.linkedin.com/in/uditagoswami/',
        'https://www.linkedin.com/in/prathamesh0902/',
        # Add more profile URLs as needed
    ]
    
    driver = init_driver()
    
    try:
        linkedin_login(driver, username, password)
        scraped_data = []
        
        for profile_url in profile_urls:
            try:
                job_title, company, industry = scrape_profile(driver, profile_url)
                scraped_data.append([job_title, company, industry])
                print(f"Scraped: {job_title}, {company}, {industry}")
            except Exception as e:
                print(f"Error scraping profile {profile_url}: {e}")
        
        save_to_csv(scraped_data)
        print("Data saved to CSV.")
    
    except Exception as e:
        print(f"Error during scraping process: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
