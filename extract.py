import time
import datetime

# ! Get the package to create dialog boxes
import easygui

# ! Get the package to visually print results
import matplotlib.pyplot as plt

# ! Get the package to control the web
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

master_job_link = "https://www.indeed.com/jobs?q=Software+Engineer&l=Boston"
link2 = "https://www.indeed.com/jobs?q=Software%20Engineer&l=Boston&vjk=2826852a029ff8f6"


def headless_options():
    """
    Sets the configurations for the driver. In our case, we add the headless settings because we want the program to crawl in the background

    Returns:
        options -- the options configurations to be used in the Google Chrome driver
    """
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    return options


def main():
    """
    Run everything
    :return: nothing
    """
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(driver_path, options=headless_options())
    # driver.get(master_job_link)
    #
    # ids = driver.find_elements_by_xpath('//*[@data-jk]')
    # print("AAAAAAA")
    # job_id = ids[0].get_attribute("data-jk")
    # print(job_id)
    # driver.get(master_job_link + "&vjk" + job_id)
    # text = driver.find_element_by_css_selector("#vjs-desc div div")
    # print(text)

    driver.get(link2)
    elements = driver.find_elements_by_xpath('//div[@id="vjs-desc"]//li')
    print("AAAAAAA")
    print(elements)
    print(len(elements))

    # text = driver.find_element_by_css_selector("#vjs-desc div div div ul")
    # print(text.text)

    # ids1 = map(lambda id: id.get_attributes("data-jk"), ids)
    # print("BBBBBBB", ids1, sep="\n")

    driver.quit()


if __name__ == "__main__":
    main()