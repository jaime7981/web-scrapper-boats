from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint
import time, pandas

#CHROME_DRIVER_PATH = "C:\Users\jaime\Downloads\chromedriver_win32\chromedriver.exe"
URL = 'https://sailboatdata.com/'
MAX_PAGE_NUMBER = 1000

urls = []

def save_urls_into_csv(url_list):
    df = pandas.DataFrame(url_list, columns=['url'])
    df.to_csv('boats_urls.csv', index=False)

def wait():
    time.sleep(randint(2, 4))

def change_max_show_number(driver):
    wait()
    driver.execute_script("window.scrollBy(0, 500);")
    wait()
    filter_button = driver.find_element(By.CLASS_NAME, 'teble-btn')
    driver.execute_script("arguments[0].scrollIntoView();", filter_button)
    filter_button.click()
    wait()
    number_of_elements = driver.find_element(By.ID, 'sailboats-per-page')
    options = number_of_elements.find_elements(By.TAG_NAME, 'option')

    for option in options:
        value = option.get_attribute('value')
        if value == '50':
            driver.execute_script('arguments[0].value = "1000";', option)
    
    execute_filter = driver.find_element(By.CLASS_NAME, 'sailboat-search')
    driver.execute_script("window.scrollBy(0, 500);")
    wait()
    driver.execute_script("arguments[0].scrollIntoView();", execute_filter)
    execute_filter.click()
    wait()

def main():
    firefox_options  = webdriver.FirefoxOptions()
    firefox_options.set_preference("javascript.enabled", True)
    driver = webdriver.Firefox(options=firefox_options)
    
    driver.get(URL)
    
    change_max_show_number(driver)
    wait()
    sailboats_table = driver.find_element(By.CLASS_NAME, 'sailboats-table')
    table_body = sailboats_table.find_element(By.TAG_NAME, 'tbody')
    table_elements = table_body.find_elements(By.TAG_NAME, 'tr')

    for element in table_elements:
        element_data = element.find_elements(By.TAG_NAME, 'td')
        first_element = element_data[0]
        url = first_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        print(url)
        urls.append(url)

    save_urls_into_csv(urls)

    driver.quit()


if __name__ == '__main__':
    main()