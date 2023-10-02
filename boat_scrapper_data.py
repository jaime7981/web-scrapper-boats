from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint
import time, pandas

def read_boats_urls(data_url):
    df = pandas.read_csv(data_url)
    urls = df['url'].tolist()
    return urls


def wait():
    time.sleep(randint(2, 4))

    
def get_boat_data(driver, url):
    driver.get(url)
    wait()
    boat_data_div = driver.find_elements(By.CLASS_NAME, 'table-light')

    boat_data = {}

    for table in boat_data_div:
        boat_data_rows = table.text.split('\n')

        for row in boat_data_rows:
            row_data = row.split(':')

            if len(row_data) == 2:
                boat_data[row_data[0]] = row_data[1]

        df_boat_data = pandas.DataFrame(boat_data, index=[0])

    return df_boat_data


def main():
    firefox_options  = webdriver.FirefoxOptions()
    firefox_options.set_preference("javascript.enabled", True)
    driver = webdriver.Firefox(options=firefox_options)

    boat_urls = read_boats_urls('boats_urls.csv')

    dataframe_list = []
    counter = 0

    for url in boat_urls:
        print(f'Boat number: {counter}')
        boat_df = get_boat_data(driver, url)
        dataframe_list.append(boat_df)

    df = pandas.concat(dataframe_list, ignore_index=True)
    
    # print(df)
    df.to_csv('all_boats_data.csv', index=False)

if __name__ == '__main__':
    main()