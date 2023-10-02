from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint
import time, pandas

#CHROME_DRIVER_PATH = "C:\Users\jaime\Downloads\chromedriver_win32\chromedriver.exe"
URL = 'https://sailboatdata.com/'
MAX_PAGE_NUMBER = 1000

urls = []
TOTAL_PAGES = 9

scroll_into_view_script = """
    var element = arguments[0];
    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
"""

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

def remove_coockies(driver):
    coockies_button = driver.find_element(By.CLASS_NAME, 'mgbutton')
    #driver.execute_script("arguments[0].scrollIntoView();", coockies_button)
    coockies_button.click()


def go_next_page(driver, page_number):
    page_number += 1
    wait()
    next_page_buttons = driver.find_elements(By.CLASS_NAME, 'page-link')

    next_page_button = None

    for button in next_page_buttons:
        button_href = button.get_attribute('href')

        next_page_reference = button_href.split('#')[-1]

        if next_page_reference == f'page-{page_number}':
            next_page_button = button
            print('Next page button found')
            break

    if next_page_button == None:
        print('Next page button not found')
        return None
    
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    wait()
    driver.execute_script(scroll_into_view_script, next_page_button)
    
    next_page_button.click()
    print('Page number: ', page_number)
    wait()
    return page_number

def extract_urls_from_page(driver):
    print('extracting urls from page')
    wait()
    sailboats_table = driver.find_element(By.CLASS_NAME, 'sailboats-table')
    table_body = sailboats_table.find_element(By.TAG_NAME, 'tbody')
    table_elements = table_body.find_elements(By.TAG_NAME, 'tr')

    for element in table_elements:
        try:
            element_data = element.find_elements(By.TAG_NAME, 'td')
            first_element = element_data[0]
            url = first_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            print(url)
            urls.append(url)
        except Exception as e:
            print('No url found')
            print(e)
            continue

def main():
    actual_page = 1

    firefox_options  = webdriver.FirefoxOptions()
    firefox_options.set_preference("javascript.enabled", True)
    driver = webdriver.Firefox(options=firefox_options)
    
    driver.get(URL)
    
    change_max_show_number(driver)
    
    while actual_page <= TOTAL_PAGES:
        extract_urls_from_page(driver)
        
        if actual_page == 1:
            remove_coockies(driver)
        
        actual_page = go_next_page(driver, actual_page)

        if actual_page == None:
            print('No more pages to go')
            break
        else:
            print(f'Page {actual_page} of {TOTAL_PAGES}')

    save_urls_into_csv(urls)

    driver.quit()


if __name__ == '__main__':
    main()