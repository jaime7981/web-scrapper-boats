from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint
import time, pandas

def read_boats_urls(data_url):
    df = pandas.read_csv(data_url)
    #df = pandas.read_excel(data_url)
    urls = df['url'].tolist()
    return urls


def wait():
    time.sleep(randint(2, 4))

    
def get_boat_data(driver, url):
    driver.get(url)
    wait()
    boat_data_div = driver.find_element(By.CLASS_NAME, 'table-light')
    boat_data_rows = boat_data_div.text.split('\n')

    for row in boat_data_rows:
        row_data = row.split(':')
        print(row_data)


def main():
    firefox_options  = webdriver.FirefoxOptions()
    firefox_options.set_preference("javascript.enabled", True)
    driver = webdriver.Firefox(options=firefox_options)

    boat_urls = read_boats_urls('boats_urls.csv')

    for url in boat_urls:
        get_boat_data(driver, url)


if __name__ == '__main__':
    main()