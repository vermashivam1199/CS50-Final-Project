import csv
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from typing import Generator, Tuple, Optional
from selenium.webdriver.chrome.webdriver import WebDriver


AMAZON_SMARTPHONES_LINK = "https://www.amazon.in/s?rh=n%3A1805560031&fs=true&ref=lp_1805560031_sar"
LIST_OF_PHONES = "/html/body/div[1]/div[2]/div[1]/div[1]/div/span[1]/div[1]/div[@class='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20']/div/div/div/div/div[@class='a-section a-spacing-small puis-padding-left-small puis-padding-right-small']/div/h2/a"
NEXT_BUTTON = "/html/body/div[1]/div[2]/div[1]/div[1]/div/span[1]/div[1]/div[@class='a-section a-spacing-none s-result-item s-flex-full-width s-widget s-widget-spacing-large']/div/div/span/a[3]"

MODEL_NAME = "//table[@class='a-normal a-spacing-micro']/tbody/tr[@class='a-spacing-small po-model_name']/td[@class='a-span9']/span"
MODEL_PRICE = "//span[@class='a-offscreen'][1]"
MODEL_RAM = "//table[@id='productDetails_techSpec_section_1']/tbody/tr/td[contains(text(),'GB')]"
MODEL_BATTERY = "//table[@id='productDetails_techSpec_section_1']/tbody/tr/td[contains(text(),'batteries')]"
MODEL_DIMENSIONS = "//table[@id='productDetails_detailBullets_sections1']/tbody/tr/td[contains(text(),'meters')]"
MODEL_SERVICE_PROVIDER = "//table[@class='a-normal a-spacing-micro']/tbody/tr[@class='a-spacing-small po-wireless_provider']/td[@class='a-span9']/span"
MODEL_BRAND_NAME = "//table[@class='a-normal a-spacing-micro']/tbody/tr[@class='a-spacing-small po-brand']/td[@class='a-span9']/span"
MODEL_STORAGE = "//table[@class='a-normal a-spacing-micro']/tbody/tr[@class='a-spacing-small po-memory_storage_capacity']/td[@class='a-span9']/span"


def setup() -> WebDriver:
    """This function returns a WebDriver object"""

    return webdriver.Chrome(ChromeDriverManager().install()) #this function automatically download or update chrome selenium drivers and set its path

def phones(link: str, driver: WebDriver, pages: Optional[int]=10) -> Generator[dict, Tuple[str, WebDriver, int], None]:
    """
    This function is yelding dict objects containing data extracted from a webpage

    This function itrates over amazon webpage containing phones and open its 
    phones on a new webpage then call data_extrator function to extract the 
    data on the phone's webpage and closes the phone's webpage and switches 
    back to the amazon webpage

    :param str link: link of the amazon webpage
    :param WebDriver driver: webdriver object
    :param int pages: number of pages to be itrated over
    :returns: yeild dict containing extracted data
    :rtype: generator object 
    """

    
    driver.maximize_window()
    driver.get(link)
    
    driver.implicitly_wait(10)

    # selecting number of pages to be itratred upon
    for _ in range(pages): #itraiting over amazon webpages

        time.sleep(2.5)
        # list of link of products in a page
        list_of_phones = driver.find_elements(By.XPATH,LIST_OF_PHONES)

        for phone in list_of_phones: #itrating over phones

            parent = driver.current_window_handle # parent window
            phone.click()
            windows = driver.window_handles # list of total windows open

            for child in windows:
                    if child != parent: # if current window is not equal to parent window
                        driver.switch_to.window(child)

            model_name, model_price, model_ram, model_battery, model_dimensions, model_service_provider, model_brand_name = data_extracter(driver)

            yield{
                "phone name":model_name,
                "phone price":model_price,
                "ram": model_ram, "battery":model_battery,
                "dimensions":model_dimensions,
                "service provider":model_service_provider,
                "brand name":model_brand_name,
            }

            driver.close()
            driver.switch_to.window(parent)

        # next button
        driver.find_element(By.XPATH, NEXT_BUTTON).click()



def data_extracter(driver: WebDriver) -> Tuple[str]:
    """
    This function extracts data from the phone's webpage and returns a Tuple of str, and if it dosen't
    find the desired data it sets '-' as default value

    :param WebDriver driver: WebDriver object
    :returns: extracted data
    :rtype: Tuple[str]
    """

    try:
        model_name = driver.find_element(By.XPATH,MODEL_NAME).text
    except NoSuchElementException:
        model_name = "-"

    try:
        model_price = driver.find_element(By.XPATH, MODEL_PRICE).get_attribute("innerText")
        final_price = re.search("(\d.+\d)",model_price)
        model_price = final_price.group(1)
    except NoSuchElementException:
        model_price = "-"

    try:
        model_ram = driver.find_element(By.XPATH, MODEL_RAM).text
    except NoSuchElementException:
        model_ram = "-"

    try:
        model_battery = driver.find_element(By.XPATH, MODEL_BATTERY).text
    except NoSuchElementException:
        model_battery = "-"

    try:
        model_dimensions = driver.find_element(By.XPATH,MODEL_DIMENSIONS).text
    except NoSuchElementException:
        model_dimensions = "-"

    try:
        model_service_provider = driver.find_element(By.XPATH, MODEL_SERVICE_PROVIDER).text
    except NoSuchElementException:
        model_service_provider = "-"

    try:
        model_brand_name = driver.find_element(By.XPATH, MODEL_BRAND_NAME).text
    except NoSuchElementException:
        model_brand_name = "-"

    
    return model_name, model_price, model_ram, model_battery, model_dimensions, model_service_provider, model_brand_name


def csv_maker(gen: Generator[dict, Tuple[str, WebDriver, int], None], name: str):
    """
    This function takes a Generator object containing dict and converts it into a csv file

    :param Generator[dict, Tuple[str, WebDriver, int]] gen: Generator object containing dict of data
    :param str name: name of the csv file
    :returnes: None
    """

    for i in gen:
        keys = i.keys()
        break

    with open(name, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(gen)

def extenction_cheker(n: str) -> str:
    """
    This function check if the inputed name has an extention(.csv) or not
    if the name has extenction(.csv) then it simply returns the name
    else it add the .csv extention and returns is

    :param str n: file name
    :returns: file name
    :rtype: str
    """
    n.strip()
    if n.endswith(".csv"):
        return n
    else:
        return n+".csv"

def main():
    """This is the main function it runs whole script"""

    file_name = extenction_cheker(input("File Name: "))
    pages = input("Pages to be scrapped: ")
    if pages:
        pages = int(pages)
        yeild_from_phone = phones(AMAZON_SMARTPHONES_LINK, setup(), pages)
    else:
        yeild_from_phone = phones(AMAZON_SMARTPHONES_LINK, setup())
    csv_maker(yeild_from_phone, file_name)


if __name__ == "__main__":
    main()
        

